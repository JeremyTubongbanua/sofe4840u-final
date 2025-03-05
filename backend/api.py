from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import json
from models.user import User, users_db, add_new_user, get_user_by_username, get_user_by_id
from models.session import Session, add_new_session, get_session_from_username
from models.post import Post, get_posts, posts_db
from models import create_default_data
from util import hash_password, validate_password, user_has_valid_session

app = Flask(__name__)
create_default_data()

# Updated JSON encoder that handles all your custom classes
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, User):
            return {
                'user_id': obj.user_id,
                'username': obj.username,
                'profile_picture_url': obj.profile_picture_url
                # Deliberately omitting password_hash for security
            }
        elif isinstance(obj, Session):
            return {
                'session_id': obj.session_id,
                'username': obj.username,
                'created_at': obj.created_at.isoformat() if hasattr(obj, 'created_at') else None,
                'expires_at': obj.expires_at.isoformat() if hasattr(obj, 'expires_at') else None
            }
        elif isinstance(obj, Post):
            return obj.to_dict()
        return super().default(obj)

app.json_encoder = CustomJSONEncoder

@app.route('/register', methods=['POST'])
def register():
    """
    Register endpoint: Create a new user
    
    Expected JSON:
    {
        "username": "string",
        "password": "string"
    }
    
    Returns:
    {
        "success": boolean
    }
    """
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "success": False,
            "message": "Username and password are required"
        }), 400

    if any(u.username == data['username'] for u in users_db.values()):
        return jsonify({
            "success": False,
            "message": "Username already exists"
        }), 400

    username = data['username']
    password = data['password']

    validation_result = validate_password(password)
    if validation_result:
        return validation_result

    hashed_password = hash_password(password)
    profile_picture_url = data.get('profile_picture_url', None)

    user = add_new_user(username, hashed_password, profile_picture_url=profile_picture_url)

    return jsonify({
        "success": True,
        "message": "User created successfully",
        "user_id": user.user_id
    }), 201

@app.route('/login', methods=['POST'])
def login():
    """
    Login endpoint: Authenticate user and create a session
    
    Expected JSON:
    {
        "username": "string",
        "password": "string"
    }
    
    Returns:
    {
        "success": boolean,
        "message": "string",
        "session_id": "string" (only if successful)
    }
    """
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "success": False,
            "message": "Username and password are required"
        }), 400

    user = get_user_by_username(data['username'])
    
    # Make sure your password validation is correct
    hashed_input_password = hash_password(data['password'])
    if not user or user.password_hash != hashed_input_password:
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        }), 401

    # Use username instead of user_id if your session system now uses username
    session = add_new_session(user.username)

    return jsonify({
        "success": True,
        "message": "Login successful",
        "session_id": session.session_id
    }), 200

@app.route('/create_like', methods=['POST'])
def create_like():
    pass

@app.route('/create_comment', methods=['POST'])
def create_comment():
    pass

@app.route('/posts', methods=['GET'])
def posts_route():
    """
    Expecting a username, password_hash, and session_id
    """
    data = request.get_json()

    if not data or 'username' not in data or 'password_hash' not in data or 'session_id' not in data:
        return jsonify({
            "success": False,
            "message": "Username, password_hash, and session_id are required"
        }), 400

    if not user_has_valid_session(data['username'], data['password_hash'], data['session_id']):
        return jsonify({
            "success": False,
            "message": "Invalid session"
        }), 401

    # Get posts and enrich them with user data
    all_posts = get_posts()
    post_data = []
    
    for post in all_posts:
        post_dict = post.to_dict()
        
        author = get_user_by_id(post.author_id)
        if author:
            post_dict['author'] = {
                'user_id': author.user_id,
                'username': author.username,
                'profile_picture_url': author.profile_picture_url
            }
        
        post_data.append(post_dict)

    return jsonify({
        "success": True,
        "posts": post_data
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)