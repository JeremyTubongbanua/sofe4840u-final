# sofe4840u-final

Final Project for SOFE 4840U - Software and Computer Security

## Backend

### Authentication

This API uses challenge-based authentication with RSA signatures. For authenticated endpoints:

1. First request a challenge via `/create_challenge`
2. Sign the challenge with your private key
3. Include the challenge signature in subsequent requests

### Endpoints

#### Key Generation

**GET** `/generate_rsa_2048_keypair`

Generate a new RSA 2048-bit key pair for registration.

**Response:**

```json
{
  "private_key": "base64-encoded-private-key-without-headers",
  "public_key": "base64-encoded-public-key-without-headers"
}
```

#### Registration

**POST** `/register`

Register a new user account.

**Request Body:**

```json
{
  "username": "username",
  "public_key": "base64-encoded-public-key"
}
```

**Response:**

```json
{
  "status": "successful",
  "message": "User created"
}
```

**Errors:**

- 400: User already exists

#### Challenge Creation

**POST** `/create_challenge`

Create an authentication challenge for a user.

**Request Body:**

```json
{
  "username": "username"
}
```

**Response:**

```json
{
  "status": "successful",
  "challenge": {
    "username": "username",
    "expire_timestamp": "iso-date-time",
    "challenge_string": "username:challenge_id"
  }
}
```

**Errors:**

- 400: User does not exist or missing request body

#### Login

**POST** `/login`

Log in with a signed challenge.

**Request Body:**

```json
{
  "username": "username",
  "challenge_signature": "base64-encoded-signature"
}
```

**Response:**

```json
{
  "status": "successful",
  "message": "Login successful",
  "auth_token": "token",
  "user": {
    "id": "user-id",
    "username": "username"
  }
}
```

**Errors:**

- 400: Missing request body, username, or challenge signature
- 404: User does not exist
- 400: No active challenge found
- 500: User public key not found
- 401: Invalid signature

#### Get Posts

**GET** `/posts`

Retrieve all posts.

**Request Body:**

```json
{
  "username": "username",
  "challenge_signature": "base64-encoded-signature"
}
```

**Response:**

```json
{
  "status": "successful",
  "posts": [
    {
      "id": "post-id",
      "username": "author-username",
      "content": "post-content",
      "timestamp": "iso-date-time",
      "likes": ["username1", "username2"],
      "comments": [
        {
          "username": "commenter-username",
          "content": "comment-content",
          "timestamp": "iso-date-time"
        }
      ]
    }
  ]
}
```

**Errors:**

- 400: Missing request body, username, or challenge signature
- 404: User does not exist
- 400: No active challenge found
- 500: User public key not found
- 401: Invalid signature

#### Toggle Like

**POST** `/toggle_like`

Like or unlike a post.

**Request Body:**

```json
{
  "username": "username",
  "challenge_signature": "base64-encoded-signature",
  "post_id": "post-id"
}
```

**Response:**

```json
{
  "status": "successful",
  "message": "Like toggled"
}
```

**Errors:**

- 400: Missing request body, username, challenge signature, or post ID
- 404: User does not exist or post not found
- 400: No active challenge found
- 500: User public key not found
- 401: Invalid signature

#### Add Comment

**POST** `/add_comment`

Add a comment to a post.

**Request Body:**

```json
{
  "username": "username",
  "challenge_signature": "base64-encoded-signature",
  "post_id": "post-id",
  "comment": "comment-text"
}
```

**Response:**

```json
{
  "status": "successful",
  "message": "Comment added"
}
```

**Errors:**

- 400: Missing request body, username, challenge signature, post ID, or comment
- 404: User does not exist or post not found
- 400: No active challenge found
- 500: User public key not found
- 401: Invalid signature

### Security Notes

1. Each challenge is single-use and invalidated after verification
2. Authentication is required for all operations (except key generation and registration)
3. RSA 2048-bit signatures with PSS padding are used for authentication
4. Challenges expire (though expiration time is not specified in the code)
