from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from util import verify_signature
from models.user import get_user_from_username, User, users, load_state as load_users_state
from models.challenge import challenges, create_challenge, challenges, get_active_challenge, load_state as load_challenges_state, verify_challenge_response
from models.post import posts, get_posts, get_post_by_id, load_state as load_posts_state
from models import create_default_data
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# create_default_data()

load_users_state('./users.json')
load_challenges_state('./challenges.json')
load_posts_state('./posts.json')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    """
    JSON will look something like this:
    {
        "username": "test",
        "public_key": "<RSA2048 Public Key>"
    }
    """

    username = data['username']
    public_key = data['public_key']

    potential_user = get_user_from_username(username)
    if potential_user:
        return jsonify({'status': 'unsuccessful', 'message': 'User already exists'}), 400

    user = User(username, public_key)
    user.save()

    return jsonify({'status': 'successful', 'message': 'User created'}), 201

@app.route('/create_challenge', methods=['POST'])
def create_challenge_endpoint():
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing request body'}), 400
    
    """
    JSON will look something like this:
    {
        "username": "test"
    }
    """

    username = data['username']

    user = get_user_from_username(username)
    if not user:
        return jsonify({'status': 'unsuccessful', 'message': 'User does not exist'}), 400

    challenge = create_challenge(user.username)
    print([challenge.to_dict() for challenge in challenges])
    return jsonify({'status': 'successful', 'challenge': challenge.to_dict()}), 200

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

        # Use the imported verify_challenge_response function instead of verify_signature
        is_valid = verify_challenge_response(username, challenge_signature)

        if not is_valid:
            return jsonify({'status': 'unsuccessful', 'message': 'Invalid signature'}), 401

        # Change dispose() to dispose()
        challenge.dispose()

        return jsonify({
            'status': 'successful',
            'message': 'Login successful',
            'user': {
                'username': user.username,
                'profile_picture_url': user.profile_picture_url
            }
        }), 200

    except Exception as e:
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
    is_valid = verify_signature(challenge_string, challenge_signature, public_key_b64)
    if not is_valid:
        return jsonify({'status': 'unsuccessful', 'message': 'Invalid signature'}), 401
    post = get_post_by_id(post_id)
    if not post:
        return jsonify({'status': 'unsuccessful', 'message': 'Post not found'}), 404
    if username in post.likes:
        post.likes.remove(username)
    else:
        post.likes.append(username)
    return jsonify({'status': 'successful', 'message': 'Like toggled'}), 200

@app.route('/posts', methods=['GET'])
def posts():
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
    is_valid = verify_signature(challenge_string, challenge_signature, public_key_b64)
    
    if not is_valid:
        return jsonify({'status': 'unsuccessful', 'message': 'Invalid signature'}), 401
        
    posts = get_posts()
    
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
    is_valid = verify_signature(challenge_string, challenge_signature, public_key_b64)
    
    if not is_valid:
        return jsonify({'status': 'unsuccessful', 'message': 'Invalid signature'}), 401
        
    post = get_post_by_id(post_id)
    if not post:
        return jsonify({'status': 'unsuccessful', 'message': 'Post not found'}), 404
        
    post.add_comment(username, comment)
    
    return jsonify({'status': 'successful', 'message': 'Comment added'}), 200
    
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)