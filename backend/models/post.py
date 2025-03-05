from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .base import Base
from ..utils.security import encrypt_data, decrypt_data

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    caption = Column(Text)
    image_path = Column(String(255), nullable=False)
    encrypted_image = Column(LargeBinary)  # For encrypted storage option
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_public = Column(Boolean, default=True)
    
    # Relationships
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='post', cascade='all, delete-orphan')
    
    def __init__(self, user_id, caption, image_path):
        self.public_id = str(uuid.uuid4())
        self.user_id = user_id
        self.caption = caption
        self.image_path = image_path
        
    def encrypt_image(self, image_data, encryption_key):
        """Encrypt image data before storing in database"""
        self.encrypted_image = encrypt_data(image_data, encryption_key)
        
    def decrypt_image(self, encryption_key):
        """Decrypt image data when retrieving"""
        if self.encrypted_image:
            return decrypt_data(self.encrypted_image, encryption_key)
        return None
    
    def like_count(self):
        return len(self.likes)
    
    def comment_count(self):
        return len(self.comments)
