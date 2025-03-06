from datetime import datetime
import uuid
import bcrypt
from typing import Dict, Optional

users = []

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
        """Save user to database."""
        users.append(self)

def get_user_from_username(username: str) -> Optional[User]:
    """Get user from database."""
    for user in users:
        if user.username == username:
            return user
    return None