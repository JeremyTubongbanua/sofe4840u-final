# Zero Trust Flask API

This is a Flask-based REST API implementing Zero Trust security principles. It provides backend services for a social media application with users, posts, comments, and likes.

## Sample CURL Commands

```bash
curl -X GET http://localhost:3000/posts \
  -H "Content-Type: application/json" \
  -d '{"username": "jeremy", "password_hash": "123", "session_id": "123"}'
```
