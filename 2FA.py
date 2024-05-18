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

