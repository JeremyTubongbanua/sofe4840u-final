from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import json
from models.user import User, users_db, add_new_user, get_user_by_username
from models.session import Session, add_new_session
from util import hash_password

app = Flask(__name__)

def validate_password(password):
    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters long"
        }), 400
    if not any(char.isupper() for char in password):
        return jsonify({
            "success": False,
            "message": "Password must contain at least one uppercase letter"
        }), 400
    if not any(char in "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?`~" for char in password):
        return jsonify({
            "success": False,
            "message": "Password must contain at least one special character"
        }), 400
    return None

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

    return validate_password(password)

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
    if not user or user.hashed_password != User._hash_password(data['password']):
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        }), 401

    session = add_new_session(user.user_id)

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
def get_posts():
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
