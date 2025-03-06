from datetime import datetime, timedelta
import uuid
from typing import Dict, Optional

sessions = []

class Session:
    def __init__(self, username: str, expiry_minutes: int = 30, session_id: Optional[str] = None):
        self.username = username

        self.session_id = session_id if session_id else str(uuid.uuid4())

        self.created_at = datetime.utcnow()
        self.last_active = self.created_at
        self.expires_at = self.created_at + timedelta(minutes=expiry_minutes)

    def to_dict(self) -> Dict:
        """Convert session object to dictionary for serialization."""
        return {
            'session_id': self.session_id,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
            'last_active': self.last_active.isoformat(),
            'expires_at': self.expires_at.isoformat()
        }

    def save(self):
        """Save session to database."""
        sessions.append(self)