from datetime import datetime, timedelta
import uuid
from typing import Dict, Optional

sessions_db = {}

class Session:
    def __init__(self, username: str, expiry_minutes: int = 30, session_id: Optional[str] = None):
        self.session_id = session_id if session_id else str(uuid.uuid4())
        self.username = username
        self.created_at = datetime.utcnow()
        self.last_active = self.created_at
        self.expires_at = self.created_at + timedelta(minutes=expiry_minutes)
    
    @property
    def active(self) -> bool:
        """Check if the session is still active."""
        return datetime.utcnow() < self.expires_at

    def to_dict(self) -> Dict:
        """Convert session object to dictionary for serialization."""
        return {
            'session_id': self.session_id,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
            'last_active': self.last_active.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'active': self.active
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Session':
        """Create a Session instance from a dictionary."""
        session = cls(
            username=data['username'],  # Changed from user_id to username
            session_id=data.get('session_id')
        )
        session.created_at = datetime.fromisoformat(data['created_at'])
        session.last_active = datetime.fromisoformat(data['last_active'])
        session.expires_at = datetime.fromisoformat(data['expires_at'])
        return session

    def update_last_active(self):
        """Update the last active timestamp."""
        self.last_active = datetime.utcnow()

def add_new_session(username: str, expiry_minutes: int = 30, session_id=None) -> Session:
    """
    Create a new session for a username or return an existing active session.
    
    Args:
        username: The username to create a session for
        expiry_minutes: Minutes until the session expires
        
    Returns:
        A new or existing Session object
    """
    existing_session = get_session_from_username(username)
    if existing_session and existing_session.active:
        existing_session.update_last_active()
        return existing_session

    # Create a new session if no active session exists
    session = Session(username, expiry_minutes, session_id)
    sessions_db[session.session_id] = session
    return session

def get_session_from_username(username: str) -> Optional[Session]:
    """Retrieve a session from the database by username."""
    for session in sessions_db.values():
        if session.username == username:
            return session
    return None

def get_session(session_id: str) -> Optional[Session]:
    """Retrieve a session from the database by session ID."""
    return sessions_db.get(session_id)

def remove_session(session_id: str) -> bool:
    """Remove a session from the database."""
    if session_id in sessions_db:
        del sessions_db[session_id]
        return True
    return False

def cleanup_expired_sessions():
    """Remove all expired sessions from the database."""
    current_time = datetime.utcnow()
    expired_sessions = [
        session_id for session_id, session in sessions_db.items()
        if session.expires_at < current_time
    ]
    
    for session_id in expired_sessions:
        del sessions_db[session_id]
    
    return len(expired_sessions)