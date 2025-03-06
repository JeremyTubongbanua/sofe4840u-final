from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import json
from models.user import get_user_from_username, User, users
from models.challenge import create_challenge, challenges
from models import create_default_data

app = Flask(__name__)
create_default_data()

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

    # Check if user already exists
    potential_user = get_user_from_username(username)
    if potential_user:
        return jsonify({'status': 'unsuccessful', 'message': 'User already exists'}), 400

    # Create user
    user = User(username, public_key)
    user.save()

    print([user.to_dict() for user in users])

    return jsonify({'status': 'successful', 'message': 'User created'}), 201

@app.route('/create_challenge', methods=['POST'])
def create_challenge_endpoint():
    data = request.get_json()
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
    data = request.get_json() # will contain username and challenge_response

    username = data['username']
    challenge_response = data['challenge_response']
    pass

@app.route('/toggle_like', methods=['POST'])
def toggle_like():
    data = request.get_json()
    pass

@app.route('/posts', methods=['GET'])
def posts():
    pass

@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)