from datetime import datetime
import uuid
from typing import Dict, Optional

likes_db = {}

class Like:
    def __init__(self, post_id: str, user_id: str, like_id: Optional[str] = None):
        self.like_id = like_id if like_id else str(uuid.uuid4())
        self.post_id = post_id
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        
    def to_dict(self) -> Dict:
        """Convert like object to dictionary for serialization."""
        return {
            'like_id': self.like_id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Like':
        """Create a Like instance from a dictionary."""
        like = cls(
            post_id=data['post_id'],
            user_id=data['user_id'],
            like_id=data.get('like_id')
        )
        like.created_at = datetime.fromisoformat(data['created_at'])
        return like

def add_new_like(post_id: str, user_id: str) -> Like:
    """Add a new like to the database."""
    like = Like(post_id, user_id)
    likes_db[like.like_id] = like
    return like