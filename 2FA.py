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
def register_user(username, password, phone_number):
    user_data = read_user_data()
    if username in user_data:
        messagebox.showerror("Error", f"User {username} already exists.")
        return
    
    totp_secret = pyotp.random_base32()
    hardware_token_secret = b64encode(get_random_bytes(32)).decode('utf-8')
    user_data[username] = {
        'password': password,
        'phone_number': phone_number,
        'totp_secret': totp_secret,
        'hardware_token_secret': hardware_token_secret
    }
    write_user_data(user_data)
    generate_totp_qr(username)
    messagebox.showinfo("Success", f"User {username} registered successfully. Scan the QR code for TOTP setup.")
