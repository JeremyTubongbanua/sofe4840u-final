from uuid import uuid4
import json
import os
from .user import get_user_from_username
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_der_public_key, load_pem_public_key
from datetime import datetime
from typing import Optional, List

challenges = []

class Challenge():
    def __init__(self, username: str, expire_timestamp: int = None, challenge_string: str = None):
        self.username = username
        self.expire_timestamp = expire_timestamp if expire_timestamp else int(datetime.now().timestamp()) + 60
        self.challenge_string = challenge_string if challenge_string else f"{username}:{str(uuid4())}"

    def to_dict(self):
        return {
            'username': self.username,
            'expire_timestamp': self.expire_timestamp,
            'challenge_string': self.challenge_string
        }

    def save(self):
        global challenges
        existing_challenge = next((c for c in challenges if c.username == self.username), None)
        if existing_challenge:
            challenges.remove(existing_challenge)
        challenges.append(self)
        
    def dispose(self):
        global challenges
        if self in challenges:
            challenges.remove(self)

def create_challenge(username: str) -> Challenge:
    global challenges
    existing_challenge = get_active_challenge(username)
    if existing_challenge:
        challenges.remove(existing_challenge)
    challenge = Challenge(username)
    challenges.append(challenge)
    return challenge

def get_active_challenge(username: str) -> Optional[Challenge]:
    global challenges
    for challenge in challenges:
        if challenge.username == username:
            if challenge.expire_timestamp > int(datetime.now().timestamp()):
                return challenge
            else:
                challenges.remove(challenge)
                break
    return None

def verify_challenge_response(username: str, signed_challenge: str) -> bool:
    user = get_user_from_username(username)
    if not user:
        raise ValueError(f'User {username} not found')
        
    user_public_key_b64 = user.public_key
    
    challenge = get_active_challenge(username)
    if not challenge:
        raise ValueError(f'No active challenge found for user {username}')
    
    try:
        public_key_bytes = base64.b64decode(user_public_key_b64)
        
        try:
            public_key = load_der_public_key(public_key_bytes, backend=default_backend())
        except:
            try:
                public_key = load_pem_public_key(public_key_bytes, backend=default_backend())
            except:
                raise ValueError('Error loading public key')
        
        signature = base64.b64decode(signed_challenge)
    except Exception as e:
        raise ValueError(f'Error decoding base64: {str(e)}')
    
    try:
        public_key.verify(
            signature,
            challenge.challenge_string.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        raise ValueError(f'Error verifying signature: {str(e)}')
