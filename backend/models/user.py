from datetime import datetime
import uuid
import bcrypt
from typing import Dict, Optional

users_db = {}

class User:
    def __init__(self, username: str, password: str, profile_picture_url: Optional[str] = None, user_id: Optional[str] = None):
        self.user_id = user_id if user_id else str(uuid.uuid4())
        self.username = username
        self.hashed_password = self._hash_password(password)
        self.profile_picture_url = profile_picture_url
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def update_profile(self, profile_picture_url: Optional[str] = None) -> None:
        """Update user profile information."""
        if profile_picture_url:
            self.profile_picture_url = profile_picture_url
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict:
        """Convert user object to dictionary for serialization."""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'profile_picture_url': self.profile_picture_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create a User instance from a dictionary."""
        user = cls(
            username=data['username'],
            password="",
            profile_picture_url=data.get('profile_picture_url'),
            user_id=data.get('user_id')
        )
        user.hashed_password = data['hashed_password']
        user.created_at = datetime.fromisoformat(data['created_at'])
        user.updated_at = datetime.fromisoformat(data['updated_at'])
        return user

    def save():
        users_db[self.user_id] = self

def add_new_user(username: str, password: str, profile_picture_url: Optional[str] = None) -> User:
    """Add a new user to the database."""
    user = User(username, password, profile_picture_url)
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