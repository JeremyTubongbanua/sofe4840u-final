from datetime import datetime
import uuid
import json
import os
from typing import Dict, Optional, List

# Initialize the global users list
users: List = []

def save_state():
    """Save the current state of users to a JSON file."""
    global users
    state = {
        'users': [user.to_dict() for user in users],
        'last_updated': datetime.utcnow().isoformat()
    }
    with open('users.json', 'w') as f:
        json.dump(state, f, indent=2)

def load_state(path: str = 'users.json'):
    """Load users from a JSON file into the global users list."""
    if not os.path.exists(path):
        return
    
    try:
        with open(path, 'r') as f:
            state = json.load(f)
        
        # Clear existing users and add loaded ones
        global users
        users.clear()  # Clear instead of reassigning to maintain any existing references
        
        for user_data in state.get('users', []):
            new_user = User.from_dict(user_data)
            users.append(new_user)
            
        print(f"{len(users)} users loaded from {path} (last updated: {state.get('last_updated', 'unknown')})")
    except Exception as e:
        print(f"Error loading users from {path}: {e}")

class User:
    def __init__(self, username: str, public_key: str, profile_picture_url: Optional[str] = None):
        self.username = username
        self.public_key = public_key
        self.profile_picture_url = profile_picture_url

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create a User instance from a dictionary."""
        user = cls(
            username=data['username'],
            public_key=data['public_key'],
            profile_picture_url=data.get('profile_picture_url')
        )
        return user

    def to_dict(self) -> Dict:
        """Convert user object to dictionary for serialization."""
        return {
            'username': self.username,
            'public_key': self.public_key,
            'profile_picture_url': self.profile_picture_url
        }

    def save(self):
        """Save user to the global users list and persist to disk."""
        global users
        # Check if user already exists
        existing_user = get_user_from_username(self.username)
        if existing_user:
            # Update existing user instead of adding a new one
            existing_user.public_key = self.public_key
            existing_user.profile_picture_url = self.profile_picture_url
        else:
            # Add new user to the global list
            users.append(self)
        
        # Save the updated state to disk
        save_state()

def get_user_from_username(username: str) -> Optional[User]:
    """Get user from the global users list by username."""
    global users
    for user in users:
        if user.username == username:
            return user
    return None