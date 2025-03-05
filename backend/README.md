# Zero Trust Flask API

This is a Flask-based REST API implementing Zero Trust security principles. It provides backend services for a social media application with users, posts, comments, and likes.

## Zero Trust Implementation

The API follows these key Zero Trust principles:

1. **Never Trust, Always Verify**: Every API request is verified by validating session tokens, IP addresses, and user agents.
2. **Least Privilege Access**: Users can only access and modify their own resources.
3. **Continuous Validation**: Sessions are short-lived (30 minutes) and require continuous revalidation.
4. **Micro-segmentation**: Each model has its own access control mechanisms.
5. **Comprehensive Logging**: All authentication and authorization events are logged.

## Models

The API consists of the following data models:

- **User**: Manages user accounts with secure password hashing
- **Session**: Tracks user authentication sessions with multi-factor validation
- **Post**: Handles social media posts with author verification
- **Comment**: Manages comments on posts with ownership validation
- **Like**: Handles post likes with unique constraints (one like per user per post)

## API Endpoints

### Authentication

- `POST /api/login`: Create a new session (returns session token)
- `POST /api/logout`: Invalidate the current session
- `GET /api/sessions`: List all active sessions for current user
- `DELETE /api/sessions/<session_id>`: Revoke a specific session

### Users

- `GET /api/users`: List all users (admin only in a real-world scenario)
- `GET /api/users/<user_id>`: Get user details
- `POST /api/users`: Create a new user (registration)
- `PUT /api/users/<user_id>`: Update a user (only own profile)

### Posts

- `GET /api/posts`: List all posts
- `GET /api/posts/<post_id>`: Get post details with comments
- `POST /api/posts`: Create a new post
- `PUT /api/posts/<post_id>`: Update a post (only own posts)
- `DELETE /api/posts/<post_id>`: Delete a post (only own posts)

### Comments

- `GET /api/posts/<post_id>/comments`: List all comments for a post
- `POST /api/posts/<post_id>/comments`: Create a new comment
- `PUT /api/comments/<comment_id>`: Update a comment (only own comments)
- `DELETE /api/comments/<comment_id>`: Delete a comment (only own comments)

### Likes

- `POST /api/posts/<post_id>/like`: Like a post
- `DELETE /api/posts/<post_id>/like`: Unlike a post

## Authentication Flow

1. **Registration**: Create a user account via `POST /api/users`
2. **Login**: Get a session token via `POST /api/login`
3. **API Requests**: Include the session token in the `Authorization` header as `Bearer <token>`

## Default User

The system comes with a default user:
- Username: `jeremy`
- Password: `X23Jem$`

## Running the API

```bash
# Install dependencies
pip install flask

# Run the API
python api.py
```

The API will be available at `http://localhost:5000`.

## Implementation Notes

- All data is stored in-memory for simplicity (in a real application, you would use a database)
- Passwords are securely hashed using PBKDF2 with SHA-256
- Sessions are validated on every request against IP and user agent
- All requests are logged for audit purposes