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

# Initialize the global challenges list
challenges = []

def save_state():
    """Save the current state of challenges to a JSON file."""
    global challenges
    state = {
        'challenges': [challenge.to_dict() for challenge in challenges],
        'last_updated': datetime.utcnow().isoformat()
    }
    
    with open('challenges.json', 'w') as f:
        json.dump(state, f, indent=2)

def load_state(path='challenges.json'):
    """Load challenges from a JSON file into the global challenges list."""
    if not os.path.exists(path):
        return
    
    try:
        with open(path, 'r') as f:
            state = json.load(f)
        
        # Clear existing challenges and add loaded ones
        global challenges
        challenges.clear()  # Clear instead of reassigning to maintain any existing references
        
        for challenge_data in state.get('challenges', []):
            challenge = Challenge(
                username=challenge_data['username'],
                expire_timestamp=challenge_data['expire_timestamp'],
                challenge_string=challenge_data['challenge_string']
            )
            challenges.append(challenge)
            
        print(f"{len(challenges)} challenges loaded from {path} (last updated: {state.get('last_updated', 'unknown')})")
    except Exception as e:
        print(f"Error loading challenges from {path}: {e}")

class Challenge():
    def __init__(self, username: str, expire_timestamp: int = None, challenge_string: str = None):
        self.username = username
        self.expire_timestamp = expire_timestamp if expire_timestamp else int(datetime.now().timestamp()) + 60
        self.challenge_string = challenge_string if challenge_string else f"{username}:{str(uuid4())}"

    def to_dict(self):
        """Convert challenge object to dictionary for serialization."""
        return {
            'username': self.username,
            'expire_timestamp': self.expire_timestamp,
            'challenge_string': self.challenge_string
        }

    def save(self):
        """Save challenge to the global challenges list and persist to disk."""
        global challenges
        # Check if challenge for this user already exists
        existing_challenge = next((c for c in challenges if c.username == self.username), None)
        if existing_challenge:
            # Remove existing challenge
            challenges.remove(existing_challenge)
        # Add new challenge
        challenges.append(self)
        save_state()
        
    def dispose(self):
        """Remove challenge from the global challenges list and persist to disk."""
        global challenges
        if self in challenges:
            challenges.remove(self)
            save_state()

def create_challenge(username: str) -> Challenge:
    """Create a new challenge for a user, replacing any existing one."""
    global challenges
    existing_challenge = get_active_challenge(username)
    if existing_challenge:
        challenges.remove(existing_challenge)
        save_state()
    challenge = Challenge(username)
    challenges.append(challenge)
    save_state()
    return challenge

def get_active_challenge(username: str) -> Optional[Challenge]:
    """Get active challenge for a user, removing expired ones."""
    global challenges
    for challenge in challenges:
        if challenge.username == username:
            if challenge.expire_timestamp > int(datetime.now().timestamp()):
                return challenge
            else:
                challenges.remove(challenge)
                save_state()
                break
    return None

def verify_challenge_response(username: str, signed_challenge: str) -> bool:
    """Verify a signed challenge response against a user's public key."""
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
        raise ValueError('Invalid signature')
    except Exception as e:
        raise ValueError(f'Error verifying signature: {str(e)}')
