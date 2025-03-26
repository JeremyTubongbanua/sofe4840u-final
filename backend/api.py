from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from util import verify_signature
from models.user import get_user_from_username, User, users, load_state as load_users_state
from models.challenge import challenges, create_challenge, challenges, get_active_challenge, verify_challenge_response
from models.post import get_posts, get_post_by_id, load_state as load_posts_state
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_users_state('./users.json')
load_posts_state('./posts.json')

from models.challenge import create_challenge, get_active_challenge

@app.route('/create_challenge', methods=['POST'])
def create_challenge_endpoint():
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing request body'}), 400

    username = data['username']

    user = get_user_from_username(username)
    if not user:
        return jsonify({'status': 'unsuccessful', 'message': 'User does not exist'}), 400

    existing_challenge = get_active_challenge(username)
    if existing_challenge:
        existing_challenge.dispose()
        
    challenge = create_challenge(user.username)
    return jsonify({'status': 'successful', 'challenge': challenge.to_dict()}), 200


def verify_and_dispose_challenge(username, challenge_signature):
    user = get_user_from_username(username)
    if not user:
        return False, "User does not exist"
        
    challenge = get_active_challenge(username)
    if not challenge:
        return False, f"No active challenge found for user {username}"
        
    public_key_b64 = user.public_key
    if not public_key_b64:
        return False, "User public key not found"

    is_valid = verify_challenge_response(username, challenge_signature)
    
    if not is_valid:
        challenge.dispose()
        return False, "Invalid signature"
    
    challenge.dispose()
    return True, "Success"


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'status': 'unsuccessful', 'message': 'Missing request body'}), 400

        if 'username' not in data:
            return jsonify({'status': 'unsuccessful', 'message': 'Missing username'}), 400

        if 'challenge_signature' not in data:
            return jsonify({'status': 'unsuccessful', 'message': 'Missing challenge signature'}), 400

        username = data['username']
        challenge_signature = data['challenge_signature']

        user = get_user_from_username(username)
        if not user:
            return jsonify({'status': 'unsuccessful', 'message': 'User does not exist'}), 404

        challenge = get_active_challenge(username)
        if not challenge:
            return jsonify({'status': 'unsuccessful', 'message': f'No active challenge found for user {username}'}), 400

        public_key_b64 = user.public_key
        if not public_key_b64:
            return jsonify({'status': 'unsuccessful', 'message': 'User public key not found'}), 500

        challenge_string = challenge.challenge_string

        is_valid = verify_challenge_response(username, challenge_signature)

        challenge.dispose()

        if not is_valid:
            return jsonify({'status': 'unsuccessful', 'message': 'Invalid signature'}), 401
        
        print(f"Login successful for user {username}. They successfully signed {challenge_string} with their private key. Their public key is: \"{public_key_b64}\" and challenge signature they generated is {challenge_signature}")

        return jsonify({
            'status': 'successful',
            'message': 'Login successful',
            'user': {
                'username': user.username,
                'profile_picture_url': user.profile_picture_url
            }
        }), 200

    except Exception as e:
        if 'username' in locals() and username:
            challenge = get_active_challenge(username)
            if challenge:
                challenge.dispose()
        print(f"Login error: {str(e)}")
        return jsonify({'status': 'unsuccessful', 'message': 'An error occurred during login'}), 500


@app.route('/toggle_like', methods=['POST'])
def toggle_like():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing request body'}), 400

    if 'username' not in data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing username'}), 400

    if 'challenge_signature' not in data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing challenge signature'}), 400

    if 'post_id' not in data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing post ID'}), 400

    username = data['username']
    challenge_signature = data['challenge_signature']
    post_id = data['post_id']

    is_valid, message = verify_and_dispose_challenge(username, challenge_signature)
    if not is_valid:
        return jsonify({'status': 'unsuccessful', 'message': message}), 401

    post = get_post_by_id(post_id)
    if not post:
        return jsonify({'status': 'unsuccessful', 'message': 'Post not found'}), 404
    if username in post.likes:
        post.likes.remove(username)
    else:
        post.likes.append(username)
    return jsonify({'status': 'successful', 'message': 'Like toggled'}), 200


@app.route('/posts', methods=['POST'])
def get_posts_req():
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing request body'}), 400
        
    if 'username' not in data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing username'}), 400
        
    if 'challenge_signature' not in data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing challenge signature'}), 400
        
    username = data['username']
    challenge_signature = data['challenge_signature']
    
    is_valid, message = verify_and_dispose_challenge(username, challenge_signature)
    if not is_valid:
        return jsonify({'status': 'unsuccessful', 'message': message}), 401
    
    posts = get_posts()
    print(f'User {username} requested posts. Found {len(posts)} posts')
    
    return jsonify({'status': 'successful', 'posts': [post.to_dict() for post in posts]}), 200
    

@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing request body'}), 400
    
    if 'username' not in data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing username'}), 400
        
    if 'challenge_signature' not in data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing challenge signature'}), 400
        
    if 'post_id' not in data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing post ID'}), 400
        
    if 'comment' not in data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing comment'}), 400
        
    username = data['username']
    post_id = data['post_id']
    comment = data['comment']
    challenge_signature = data['challenge_signature']
    
    is_valid, message = verify_and_dispose_challenge(username, challenge_signature)
    if not is_valid:
        return jsonify({'status': 'unsuccessful', 'message': message}), 401
        
    post = get_post_by_id(post_id)
    if not post:
        return jsonify({'status': 'unsuccessful', 'message': 'Post not found'}), 404
        
    post.add_comment(username, comment)
    
    return jsonify({'status': 'successful', 'message': 'Comment added'}), 200
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)