from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid
import jwt
from .base import Base
from .associations import followers
from ..utils.security import hash_password, verify_password

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True, nullable=False)  # Public ID for API exposure
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    salt = Column(String(29), nullable=False)
    profile_picture = Column(String(200))
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(32))
    failed_login_attempts = Column(Integer, default=0)
    account_locked_until = Column(DateTime)
    
    # Relationships
    posts = relationship('Post', back_populates='user', cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='user', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='user', cascade='all, delete-orphan')
    sessions = relationship('Session', back_populates='user', cascade='all, delete-orphan')
    
    # Many-to-many relationship for followers
    followed = relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref='followers'
    )
    
    def __init__(self, username, email, password):
        self.public_id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.salt = hash_password.generate_salt()
        self.password_hash = hash_password(password, self.salt)
        
    def verify_password(self, password):
        return verify_password(password, self.password_hash, self.salt)
    
    def generate_auth_token(self, secret_key, expires_in=3600):
        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow(),
            'sub': self.public_id
        }
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    def follow(self, user):
        if not self.is_following(user) and self.id != user.id:
            self.followed.append(user)
            return True
        return False
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return True
        return False
    
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
