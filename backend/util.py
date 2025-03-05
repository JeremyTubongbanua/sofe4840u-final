import hashlib
import os

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    hash_obj = hashlib.sha256()
    hash_obj.update(salt + password.encode('utf-8'))
    hashed_password = hash_obj.hexdigest()
    return salt.hex() + hashed_password
