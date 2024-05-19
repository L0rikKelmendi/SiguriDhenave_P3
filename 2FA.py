import pyotp
import qrcode
import json
import os
import hmac
import hashlib
from base64 import b64encode
from Crypto.Random import get_random_bytes
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime
from sms import email_alert  # Importing the email_alert function

# Emri i skedarit JSON për ruajtjen e të dhënave të përdoruesve
USER_DATA_FILE = 'users.json'
LOG_FILE = 'hardware_token_log.txt'

# Funksion për të lexuar të dhënat e përdoruesve nga skedari JSON
def read_user_data():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

# Funksion për të shkruar të dhënat e përdoruesve në skedarin JSON
def write_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Funksion për të regjistruar një përdorues të ri
def register_user(username, password, email):
    user_data = read_user_data()
    if username in user_data:
        messagebox.showerror("Error", f"User {username} already exists.")
        return
    
    totp_secret = pyotp.random_base32()
    hardware_token_secret = b64encode(get_random_bytes(32)).decode('utf-8')
    user_data[username] = {
        'password': password,
        'email': email,
        'totp_secret': totp_secret,
        'hardware_token_secret': hardware_token_secret
    }
    write_user_data(user_data)
    generate_totp_qr(username)
    messagebox.showinfo("Success", f"User {username} registered successfully. Scan the QR code for TOTP setup.")

# Funksion për të gjeneruar dhe verifikuar TOTP
def generate_totp_qr(username):
    user_data = read_user_data()
    if username not in user_data:
        messagebox.showerror("Error", f"User {username} not found.")
        return
    
    secret = user_data[username]['totp_secret']
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="YourApp")
    img = qrcode.make(totp_uri)
    img.save(f"{username}.png")
    messagebox.showinfo("Success", f"QR Code saved as {username}.png. Scan this QR code with your TOTP app.")

def verify_totp(username, otp):
    user_data = read_user_data()
    if username not in user_data:
        return False
    
    secret = user_data[username]['totp_secret']
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

# Funksion për të verifikuar dhe përditësuar token hardware (YubiKey)
def verify_and_update_hardware_token(username, token):
    user_data = read_user_data()
    if username not in user_data:
        return False
    
    secret = user_data[username]['hardware_token_secret']
    hmac_obj = hmac.new(secret.encode(), token.encode(), hashlib.sha256)
    if hmac.compare_digest(hmac_obj.hexdigest(), token):
        # Generate a new hardware token secret and update the user data
        new_hardware_token_secret = b64encode(get_random_bytes(32)).decode('utf-8')
        user_data[username]['hardware_token_secret'] = new_hardware_token_secret
        write_user_data(user_data)
        
        # Log the token update
        log_hardware_token_update(username, new_hardware_token_secret)
        return True
    return False

# Funksion për të bërë login dhe për të treguar një mesazh mirëseardhjeje
def login(username, password, otp=None, token=None):
    user_data = read_user_data()
    if username not in user_data or user_data[username]['password'] != password:
        messagebox.showerror("Error", "Invalid username or password.")
        return
    
    if otp and verify_totp(username, otp):
        show_welcome_message(username)
    elif token and verify_and_update_hardware_token(username, token):
        show_welcome_message(username)
    else:
        messagebox.showerror("Error", "Invalid OTP or hardware token.")

# Funksion për të treguar një mesazh mirëseardhjeje
def show_welcome_message(username):
    welcome_window = tk.Toplevel(root)
    welcome_window.title("Welcome")
    welcome_label = tk.Label(welcome_window, text=f"Welcome to Siguria e të Dhënave, {username}!", padx=20, pady=20)
    welcome_label.pack()
    close_button = tk.Button(welcome_window, text="Close", command=welcome_window.destroy)
    close_button.pack(pady=10)

# Funksionet për GUI
def register_user_gui():
    username = simpledialog.askstring("Register", "Enter username:")
    password = simpledialog.askstring("Register", "Enter password:", show='*')
    email = simpledialog.askstring("Register", "Enter email:")
    if username and password and email:
        register_user(username, password, email)

def login_gui():
    login_dialog = tk.Toplevel(root)
    login_dialog.title("Login")

    tk.Label(login_dialog, text="Enter username:").pack(pady=5)
    username_entry = tk.Entry(login_dialog)
    username_entry.pack(pady=5)

    tk.Label(login_dialog, text="Enter password:").pack(pady=5)
    password_entry = tk.Entry(login_dialog, show='*')
    password_entry.pack(pady=5)

    def on_login():
        username = username_entry.get()
        password = password_entry.get()

        if username and password:
            user_data = read_user_data()
            if username in user_data and user_data[username]['password'] == password:
                email = user_data[username]['email']
                email_subject = "Login Attempt"
                attachment_filename = f"{username}.png"
                attachments = [attachment_filename]
                email_alert(email_subject, "", email, attachments)  # Email body left empty
                login_dialog.destroy()
                show_authentication_choice(username, password)
            else:
                messagebox.showerror("Error", "Invalid username or password.")

    login_button = tk.Button(login_dialog, text="Login", command=on_login)
    login_button.pack(pady=10)

    login_dialog.mainloop()



def show_authentication_choice(username, password):
    auth_window = tk.Toplevel(root)
    auth_window.title("Choose Authentication Method")
    
    totp_button = tk.Button(auth_window, text="Use TOTP", 
                            command=lambda: authenticate_with_totp(auth_window, username, password))
    hardware_button = tk.Button(auth_window, text="Use Hardware Token", 
                                command=lambda: authenticate_with_hardware_token(auth_window, username, password))
    
    totp_button.pack(pady=10)
    hardware_button.pack(pady=10)

def authenticate_with_totp(auth_window, username, password):
    auth_window.destroy()
    otp = simpledialog.askstring("TOTP Authentication", "Enter TOTP:")
    if otp:
        login(username, password, otp=otp)

def authenticate_with_hardware_token(auth_window, username, password):
    auth_window.destroy()
    token = simpledialog.askstring("Hardware Token Authentication", "Enter hardware token:")
    if token:
        login(username, password, token=token)

# Funksion për të regjistruar përditësimet e hardware token
def log_hardware_token_update(username, new_token):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{datetime.now()}: {username} updated hardware token to {new_token}\n")

# Krijimi i dritares kryesore të GUI
root = tk.Tk()
root.title("2FA Authentication System")

register_button = tk.Button(root, text="Register", command=register_user_gui)
login_button = tk.Button(root, text="Login", command=login_gui)

register_button.pack(pady=10)
login_button.pack(pady=10)

root.mainloop()
