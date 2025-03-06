# Zero Trust Flask API

This is a Flask-based REST API implementing Zero Trust security principles. It provides backend services for a social media application with users, posts, comments, and likes.

## Sample CURL Commands

Get Posts

```bash
curl -X GET http://localhost:3000/posts \
  -H "Content-Type: application/json" \
  -d '{"username": "jeremy", "password": "123", "session_id": "123"}'
```

Register

```bash
curl -X POST http://localhost:3000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "Testing+", "password": "Testing1+"}'
```

Login

```bash
curl -X POST http://localhost:3000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "Testing+", "password": "Testing1+"}'
```

Like

```bash
curl -X POST http://localhost:3000/toggle_like \
 -H "Content-Type: application/json" \
 -d '{"post_id":"post1", "username":"jeremy", "password":"123", "session_id":"123"}'
```
