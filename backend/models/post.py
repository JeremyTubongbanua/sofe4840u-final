from datetime import datetime
import uuid
from typing import Dict, List, Optional
from .user import User, get_user_from_username
from .comment import Comment

posts = []

class Post:
    def __init__(self, author_username: str, title: str, description: str, image_url: Optional[str] = None, post_id: Optional[str] = None, likes: Optional[List[str]] = None, comments: Optional[List[str]] = None):
        self.author_username = author_username
        self.title = title
        self.description = description
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
        existing_post = next((post for post in posts if post.post_id == self.post_id), None)
        if existing_post:
            existing_post.author_username = self.author_username
            existing_post.title = self.title
            existing_post.description = self.description
            existing_post.image_url = self.image_url
            existing_post.updated_at = datetime.utcnow()
            existing_post.likes = self.likes
            existing_post.comments = self.comments
        else:
            posts.append(self)

    def add_comment(self, username: str, description: str):
        """Add comment to post."""
        user = get_user_from_username(username)
        if not user:
            raise ValueError(f'User {username} not found')
        self.comments.append(Comment(username, description, profile_picture_url=user.profile_picture_url))

def get_posts():
    """Get all posts from database."""
    return posts