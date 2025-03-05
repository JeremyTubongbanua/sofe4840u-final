from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import json

# Import the models
from models.user import User, users_db, add_new_user, get_user_by_username
from models.post import Post, posts_db, add_new_post
from models.comment import Comment, add_new_comment, get_comment
from models.like import Like, add_new_like, get_like
from models.session import Session, add_new_session, get_session_from_username

app = Flask(__name__)

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
        "success": boolean,
        "message": "string",
        "user_id": "string" (only if successful)
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

    user = add_new_user(data['username'], data['password'])

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
    """
    Create like endpoint: Add a like to a post

    Expected JSON:
    {
        "session_id": "string",
        "post_id": "string"
    }

    Returns:
    {
        "success": boolean,
        "message": "string",
        "like_id": "string" (only if successful)
    }
    """
    data = request.get_json()

    if not data or 'session_id' not in data or 'post_id' not in data:
        return jsonify({
            "success": False,
            "message": "Session ID and post ID are required"
        }), 400

    session = get_session(data['session_id'])
    if not session or not session.is_valid():
        return jsonify({
            "success": False,
            "message": "Invalid or expired session"
        }), 401
    
    if data['post_id'] not in posts_db:
        return jsonify({
            "success": False,
            "message": "Post not found"
        }), 404
    
    post = posts_db[data['post_id']]
    session.last_active = datetime.utcnow()
    
    if post.add_like(session.user_id):
        like = add_new_like(post.post_id, session.user_id)
        return jsonify({
            "success": True,
            "message": "Like added successfully",
            "like_id": like.like_id
        }), 201
    else:
        return jsonify({
            "success": False,
            "message": "Post already liked by this user"
        }), 400

@app.route('/create_comment', methods=['POST'])
def create_comment():
    """
    Create comment endpoint: Add a comment to a post
    
    Expected JSON:
    {
        "session_id": "string",
        "post_id": "string",
        "content": "string"
    }
    
    Returns:
    {
        "success": boolean,
        "message": "string",
        "comment_id": "string" (only if successful)
    }
    """
    data = request.get_json()
    
    if not data or 'session_id' not in data or 'post_id' not in data or 'content' not in data:
        return jsonify({
            "success": False,
            "message": "Session ID, post ID, and content are required"
        }), 400
    
    session = get_session(data['session_id'])
    if not session or not session.is_valid():
        return jsonify({
            "success": False,
            "message": "Invalid or expired session"
        }), 401
    
    if data['post_id'] not in posts_db:
        return jsonify({
            "success": False,
            "message": "Post not found"
        }), 404
    
    post = posts_db[data['post_id']]
    session.last_active = datetime.utcnow()
    
    comment = add_new_comment(post.post_id, session.user_id, data['content'])
    post.add_comment(comment.comment_id)
    
    return jsonify({
        "success": True,
        "message": "Comment added successfully",
        "comment_id": comment.comment_id
    }), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    """
    Get all posts endpoint
    
    Returns:
    {
        "success": boolean,
        "posts": list of posts
    }
    """
    posts_list = []
    for post_id, post in posts_db.items():
        posts_list.append(post.to_dict())
    
    return jsonify({
        "success": True,
        "posts": posts_list
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
