import hashlib
import re
from flask import jsonify
from models.session import get_session_from_username

def hash_password(password):
    """Hash a password using a simple hash function."""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password(password):
    """Validate password complexity."""
    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters long"
        }), 400
    
    if not re.search(r'[A-Z]', password):
        return jsonify({
            "success": False,
            "message": "Password must contain at least one uppercase letter"
        }), 400
    
    if not re.search(r'[a-z]', password):
        return jsonify({
            "success": False,
            "message": "Password must contain at least one lowercase letter"
        }), 400
    
    if not re.search(r'[0-9]', password):
        return jsonify({
            "success": False,
            "message": "Password must contain at least one number"
        }), 400
    
    return None

def user_has_valid_session(username, password_hash, session_id):
    """Check if a user has a valid session."""
    # Get the session for this username
    session = get_session_from_username(username)
    if not session:
        print(f'Username: {username} does not have a session')
        return False
    
    # Check if the session ID matches
    if session.session_id != session_id:
        print(f'Session ID mismatch: expected {session.session_id}, got {session_id}')
        return False
    
    # Check if the session is still active (you'll need to implement this in your Session class)
    if hasattr(session, 'expires_at'):
        from datetime import datetime
        if datetime.utcnow() > session.expires_at:
            print(f'Session has expired')
            return False
    
    # For now, we'll just check if the session ID matches
    # In a real application, you would also validate the password hash

    
    
    return True