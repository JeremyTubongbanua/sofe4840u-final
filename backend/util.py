import hashlib
import re
from flask import jsonify
from models.user import get_user_from_username

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

def verify_signature(challenge: str, signed_challenge: str, public_key_b64: str) -> bool:
    try:
        public_key_bytes = base64.b64decode(public_key_b64)

        try:
            public_key = load_der_public_key(
                public_key_bytes, 
                backend=default_backend()
            )
        except Exception:
            try:
                public_key = load_pem_public_key(
                    public_key_bytes, 
                    backend=default_backend()
                )
            except Exception as e:
                raise ValueError(f"Failed to load public key: {str(e)}")

        try:
            signature = base64.b64decode(signed_challenge)
        except Exception as e:
            raise ValueError(f"Failed to decode signature: {str(e)}")

        public_key.verify(
            signature,
            challenge.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except Exception:
        return False