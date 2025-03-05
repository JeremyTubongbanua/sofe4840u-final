from datetime import datetime
import uuid
import bcrypt
from typing import Dict, Optional

users_db = {}

class User:
    def __init__(self, username: str, password_hash: str, profile_picture_url: Optional[str] = None, user_id: Optional[str] = None):
        self.user_id = user_id if user_id else str(uuid.uuid4())
        self.username = username
        self.password_hash = password_hash
        self.profile_picture_url = profile_picture_url

    def to_dict(self) -> Dict:
        """Convert user object to dictionary for serialization."""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password_hash': self.password_hash,
            'profile_picture_url': self.profile_picture_url
        }

def add_new_user(username: str, password_hash: str, profile_picture_url: Optional[str] = None, user_id: Optional[str] = None) -> User:
    """Add a new user to the database."""
    user = User(username, password_hash, profile_picture_url, user_id)
    users_db[user.user_id] = user
    return user

def save_user(user: User) -> None:
    """Save a user to the database."""
    users_db[user.user_id] = user

def get_user_by_username(username: str) -> Optional[User]:
    """Get a user by username."""
    for user in users_db.values():
        if user.username == username:
            return user
    return None

def get_user_by_id(user_id: str) -> Optional[User]:
    """Get a user by ID."""
    return users_db.get(user_id)