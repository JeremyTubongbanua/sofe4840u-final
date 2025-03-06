from datetime import datetime
import uuid
from typing import Dict, List, Optional
from .user import User

posts = []

class Post:
    def __init__(self, author_username: str, description: str, image_url: Optional[str] = None, post_id: Optional[str] = None, likes: Optional[List[str]] = None, comments: Optional[List[str]] = None):
        self.author_username = author_username
        self.description = description
        self.author_id = author_username
        self.updated_at = datetime.utcnow()

        self.image_url = image_url
        self.post_id = post_id if post_id else str(uuid.uuid4())

        self.created_at = datetime.utcnow()

        self.likes = [] # list of usernames
        self.comments = [] # list of usernames

    def to_dict(self) -> Dict:
        """Convert post object to dictionary for serialization."""
        return {
            'post_id': self.post_id,
            'author_id': self.author_id,
            'description': self.description,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'likes': self.likes,
            'comments': self.comments
        }

    def save(self):
        """Save post to database."""
        posts.append(self)

