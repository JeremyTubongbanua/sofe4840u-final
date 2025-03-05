from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Like(Base):
    __tablename__ = 'likes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate likes
    __table_args__ = (
        # A user can only like a post once
        {'sqlite_autoincrement': True},
    )
    
    # Relationships
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')
    
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
