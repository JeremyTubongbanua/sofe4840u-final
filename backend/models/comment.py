from datetime import datetime
import uuid
from typing import Dict, Optional

comments_db = {}

class Comment:
    def __init__(self, post_id: str, author_id: str, content: str, comment_id: Optional[str] = None):
        self.comment_id = comment_id if comment_id else str(uuid.uuid4())
        self.post_id = post_id
        self.author_id = author_id
        self.content = content
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def to_dict(self) -> Dict:
        """Convert comment object to dictionary for serialization."""
        return {
            'comment_id': self.comment_id,
            'post_id': self.post_id,
            'author_id': self.author_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Comment':
        """Create a Comment instance from a dictionary."""
        comment = cls(
            post_id=data['post_id'],
            author_id=data['author_id'],
            content=data['content'],
            comment_id=data.get('comment_id')
        )
        comment.created_at = datetime.fromisoformat(data['created_at'])
        comment.updated_at = datetime.fromisoformat(data['updated_at'])
        return comment

def get_comment(comment_id: str) -> Optional[Comment]:
    """Get a comment by ID."""
    return comments_db.get(comment_id)

def add_new_comment(post_id: str, author_id: str, content: str) -> Comment:
    """Add a new comment to the database."""
    comment = Comment(post_id, author_id, content)
    comments_db[comment.comment_id] = comment
    return comment