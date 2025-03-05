from datetime import datetime, timedelta
import uuid
from typing import Dict, Optional

sessions_db = {}

class Session:
    def __init__(self, user_id: str, expiry_minutes: int = 30, session_id: Optional[str] = None):
        self.session_id = session_id if session_id else str(uuid.uuid4())
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.last_active = self.created_at
        self.expires_at = self.created_at + timedelta(minutes=expiry_minutes)

    def to_dict(self) -> Dict:
        """Convert session object to dictionary for serialization."""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'last_active': self.last_active.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'active': self.active
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Session':
        """Create a Session instance from a dictionary."""
        session = cls(
            user_id=data['user_id'],
            session_id=data.get('session_id')
        )
        session.created_at = datetime.fromisoformat(data['created_at'])
        session.last_active = datetime.fromisoformat(data['last_active'])
        session.expires_at = datetime.fromisoformat(data['expires_at'])
        session.active = data['active']
        return session

def add_new_session(user_id: str, expiry_minutes: int = 30) -> Session:
    """Add a new session to the database."""
    existing_session = next((s for s in sessions_db.values() if s.user_id == user_id), None)
    if existing_session:
        del sessions_db[existing_session.session_id]

    session = Session(user_id, expiry_minutes)
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
    for session in sessions_db.values():
        if session.session_id == session_id:
            return session
    return None
