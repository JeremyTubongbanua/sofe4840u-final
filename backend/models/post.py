from datetime import datetime
import uuid
from typing import Dict, List, Optional

posts_db = {}

class Post:
    def __init__(self, author_id: str, description: str, image_url: Optional[str] = None, post_id: Optional[str] = None):
        self.post_id = post_id if post_id else str(uuid.uuid4())
        self.author_id = author_id
        self.description = description
        self.image_url = image_url
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        self.likes = [] 
        self.comments = [] 

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

    @classmethod
    def from_dict(cls, data: Dict) -> 'Post':
        """Create a Post instance from a dictionary."""
        post = cls(
            author_id=data['author_id'],
            description=data['description'],
            image_url=data.get('image_url'),
            post_id=data.get('post_id')
        )
        post.likes = data.get('likes', [])
        post.comments = data.get('comments', [])
        post.created_at = datetime.fromisoformat(data['created_at'])
        post.updated_at = datetime.fromisoformat(data['updated_at'])
        return post

def add_new_post(author_id: str, description: str, image_url: Optional[str] = None) -> Post:
    """Add a new post to the database."""
    post = Post(author_id, description, image_url)
    posts_db[post.post_id] = post
    return post

def get_post_by_id(post_id: str) -> Optional[Post]:
    """Get a post by ID."""
    return posts_db.get(post_id)

def get_posts() -> List[Post]:
    """Get all posts."""
    return list(posts_db.values())
