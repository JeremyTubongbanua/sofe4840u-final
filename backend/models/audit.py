from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from .base import Base

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # Nullable for system events
    event_type = Column(String(50), nullable=False)  # login, logout, post_create, etc.
    resource_type = Column(String(50))  # user, post, comment, etc.
    resource_id = Column(String(50))  # The ID of the affected resource
    ip_address = Column(String(45))
    user_agent = Column(String(200))
    details = Column(Text)  # JSON string with event details
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, event_type, user_id=None, resource_type=None, resource_id=None, 
                 ip_address=None, user_agent=None, details=None):
        self.user_id = user_id
        self.event_type = event_type
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.details = details
