import hashlib
import re
from flask import jsonify
from models.user import get_user_by_username
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

def user_has_valid_session(username, password, session_id):
    """Check if a user has a valid session."""

    tup1 = (hash_password(password), session_id)

    potential_session = get_session_from_username(username)
    if not potential_session:
        return False

    potential_user = get_user_by_username(username)
    if not potential_user:
        return False

    potential_password = potential_user.password_hash

    tup2 = (potential_password, potential_session.session_id)

    return tup1 == tup2
