import pyotp
import qrcode
import random
import string
import time

# Simulated database
users_db = {}
backup_codes_db = {}
failed_attempts = {}

# Rate limiting parameters
TIME_WINDOW = 300  # 5 minutes in seconds
MAX_ATTEMPTS = 3
BLOCK_DURATION = 600  # 10 minutes in seconds

def generate_secret_key():
    """Generate a unique secret key for a user."""
    return pyotp.random_base32()

def generate_backup_codes():
    """Generate a set of backup codes."""
    return [''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) for _ in range(5)]

def generate_qr_code(secret_key, user_email):
    """Generate a QR code based on the secret key."""
    totp = pyotp.TOTP(secret_key)
    provision_uri = totp.provisioning_uri(name=user_email, issuer_name="YourAppName")
    img = qrcode.make(provision_uri)
    img.show()

def register_user(email):
    """Register a new user."""
    if email in users_db:
        print("User already exists!")
        return
    secret_key = generate_secret_key()
    users_db[email] = secret_key
    backup_codes = generate_backup_codes()
    backup_codes_db[email] = backup_codes
    print(f"User {email} registered with secret key: {secret_key}")
    print("Backup Codes:")
    for code in backup_codes:
        print(code)
    print("Generating QR Code for 2FA setup...")
    generate_qr_code(secret_key, email)
    
    def verify_totp(email, provided_totp):
    """Verify the provided TOTP against the current TOTP for the secret key."""
    if email not in users_db:
        return False
    secret_key = users_db[email]
    totp = pyotp.TOTP(secret_key)
    return totp.verify(provided_totp)