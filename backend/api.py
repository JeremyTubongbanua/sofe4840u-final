from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from models.user import get_user_from_username, User, users, load_state as load_users_state
from models.challenge import challenges, create_challenge, challenges, get_active_challenge, verify_challenge_response
from models.post import get_posts, get_post_by_id, load_state as load_posts_state
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173", "supports_credentials": True}})

load_users_state('./users.json')
load_posts_state('./posts.json')

@app.route('/register', methods=['POST'])
def register_endpoint():
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing request body'}), 400
    
    if 'username' not in data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing username'}), 400
    
    if 'profile_picture_url' not in data:
        return jsonify({'status': 'unsuccessful', 'message': 'Missing profile picture URL'}), 400
    
    username = data['username']
    public_key = data['public_key']
    profile_picture_url = data['profile_picture_url']
    
    user = get_user_from_username(username)
    if user:
        return jsonify({'status': 'unsuccessful', 'message': 'User already exists'}), 400
    
    user = User(username=username, 
                public_key=public_key, 
                profile_picture_url=profile_picture_url)
    users.append(user)
    user.save()
    
    return jsonify({'status': 'successful', 'message': 'User registered'}), 200

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
    print(f"Verifying challenge for user: {username}")
    
    user = get_user_from_username(username)
    if not user:
        print(f"User {username} does not exist")
        return False, "User does not exist"
        
    challenge = get_active_challenge(username)
    if not challenge:
        print(f"No active challenge found for user {username}")
        return False, f"No active challenge found for user {username}"
    original_challenge = challenge.challenge_string
    print(f"Original Challenge: {original_challenge}")
    
    print(f"Challenge Signature: {challenge_signature}")
    
    public_key_b64 = user.public_key
    if public_key_b64:
        truncated_pk = public_key_b64[:5] + "..."
        print(f"User Public Key (truncated): {truncated_pk}")
    else:
        print(f"Public key for user {username} not found")
        return False, "User public key not found"

    is_valid = verify_challenge_response(username, challenge_signature)
    
    if not is_valid:
        print(f"Invalid signature for user {username}")
        challenge.dispose()
        return False, "Invalid signature"
    
    challenge.dispose()
    print(f"Challenge verified and disposed for user {username}")
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

        is_valid, message = verify_and_dispose_challenge(username, challenge_signature)
        if not is_valid:
            return jsonify({'status': 'unsuccessful', 'message': message}), 401

        user = get_user_from_username(username)
        if not user:
            return jsonify({'status': 'unsuccessful', 'message': 'User does not exist'}), 404
        
        print(f"Login successful for user {username}.")

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


@app.route('/toggle_like', methods=['POST', 'OPTIONS'])
def toggle_like():
    if request.method == 'OPTIONS':
        return '', 200
        
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
    
    print(f'User {username} toggled like on post {post_id}')
    post = get_post_by_id(post_id)
    if not post:
        return jsonify({'status': 'unsuccessful', 'message': 'Post not found'}), 404
    if username in post.likes:
        post.likes.remove(username)
    else:
        post.likes.append(username)
    post.save()
    return jsonify({'status': 'successful', 'message': 'Like toggled'}), 200


@app.route('/posts', methods=['POST', 'OPTIONS'])
def get_posts_req():
    if request.method == 'OPTIONS':
        return '', 200
        
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
    
    user_profiles = {}
    for user in users:
        user_profiles[user.username] = user.profile_picture_url
    
    enhanced_posts = []
    for post in posts:
        post_dict = post.to_dict()
        
        author_id = post_dict['author_id']
        post_dict['author_profile_picture'] = user_profiles.get(author_id)
        
        for comment in post_dict.get('comments', []):
            comment_author = comment.get('username')
            if comment_author:
                comment['profile_picture_url'] = user_profiles.get(comment_author)
        
        enhanced_posts.append(post_dict)
    
    return jsonify({'status': 'successful', 'posts': enhanced_posts}), 200    

@app.route('/add_comment', methods=['POST', 'OPTIONS'])
def add_comment():
    if request.method == 'OPTIONS':
        return '', 200
        
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