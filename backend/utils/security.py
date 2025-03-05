import bcrypt
from cryptography.fernet import Fernet
import os

def generate_salt():
    """Generate a random salt for password hashing"""
    return bcrypt.gensalt().decode('utf-8')

def hash_password(password, salt):
    """Hash a password with the given salt"""
    return bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

def verify_password(password, password_hash, salt):
    """Verify a password against a stored hash"""
    return bcrypt.checkpw(
        password.encode('utf-8'), 
        password_hash.encode('utf-8')
    )

def generate_encryption_key():
    """Generate a new encryption key for data encryption"""
    return Fernet.generate_key()

def encrypt_data(data, key):
    """Encrypt binary data using Fernet symmetric encryption"""
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(encrypted_data, key):
    """Decrypt binary data using Fernet symmetric encryption"""
    f = Fernet(key)
    return f.decrypt(encrypted_data)

def generate_device_fingerprint(request_data):
    """
    Generate a device fingerprint from request data
    
    Parameters:
    request_data (dict): Dictionary containing user-agent, ip, screen resolution, etc.
    
    Returns:
    str: A unique fingerprint for the device
    """
    # Implementation depends on what data you collect
    # This is a simplified example
    import hashlib
    
    fingerprint_data = (
        request_data.get('user_agent', '') +
        request_data.get('ip', '') +
        request_data.get('screen_resolution', '') +
        request_data.get('platform', '')
    )
    
    return hashlib.sha256(fingerprint_data.encode()).hexdigest()
