from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Session(Base):
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    token = Column(String(500), nullable=False)
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(String(200), nullable=False)
    device_fingerprint = Column(String(64), nullable=False)
    is_valid = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship('User', back_populates='sessions')
    
    def __init__(self, user_id, token, ip_address, user_agent, device_fingerprint, expires_at):
        self.user_id = user_id
        self.token = token
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.device_fingerprint = device_fingerprint
        self.expires_at = expires_at
    
    def is_expired(self):
        return datetime.utcnow() > self.expires_at
    
    def invalidate(self):
        self.is_valid = False
    
    def update_activity(self):
        self.last_activity = datetime.utcnow()
