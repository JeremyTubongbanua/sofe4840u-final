from datetime import datetime
import uuid
import json
import os
from typing import Dict, List, Optional
from .user import User, get_user_from_username
from .comment import Comment

# Initialize the global posts list
posts = []

def save_state():
    """Save the current state of posts to a JSON file."""
    global posts
    state = {
        'posts': [post.to_dict() for post in posts],
        'last_updated': datetime.utcnow().isoformat()
    }
    with open('posts.json', 'w') as f:
        json.dump(state, f, indent=2)

def load_state(path: str = 'posts.json'):
    """Load posts from a JSON file into the global posts list."""
    if not os.path.exists(path):
        return
    try:
        with open(path, 'r') as f:
            state = json.load(f)
        
        # Clear existing posts and add loaded ones
        global posts
        posts.clear()  # Clear instead of reassigning to maintain any existing references
        
        for post_data in state.get('posts', []):
            post = Post(
                author_username=post_data['author_id'],
                title=post_data.get('title', ''),
                description=post_data['description'],
                image_url=post_data.get('image_url'),
                post_id=post_data['post_id']
            )
            post.created_at = datetime.fromisoformat(post_data['created_at'])
            post.updated_at = datetime.fromisoformat(post_data['updated_at'])
            post.likes = post_data.get('likes', [])
            post.comments = []
            for comment_data in post_data.get('comments', []):
                if isinstance(comment_data, dict):
                    post.comments.append(Comment(
                        username=comment_data['username'],
                        description=comment_data['description'],
                        profile_picture_url=comment_data.get('profile_picture_url')
                    ))
            posts.append(post)
        print(f"{len(posts)} posts loaded from {path} (last updated: {state.get('last_updated', 'unknown')})")
    except Exception as e:
        print(f"Error loading posts from {path}: {e}")

class Post:
    def __init__(self, author_username: str, title: str, description: str, image_url: Optional[str] = None, post_id: Optional[str] = None, likes: Optional[List[str]] = None, comments: Optional[List[Comment]] = None):
        self.author_username = author_username
        self.title = title
        self.description = description
        self.updated_at = datetime.utcnow()

        self.image_url = image_url
        self.post_id = post_id if post_id else str(uuid.uuid4())

        self.created_at = datetime.utcnow()

        self.likes = likes if likes else []  # list of usernames
        self.comments = comments if comments else []  # list of comment objects

    def to_dict(self) -> Dict:
        """Convert post object to dictionary for serialization."""
        return {
            'post_id': self.post_id,
            'author_id': self.author_username,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'likes': self.likes,
            'comments': [comment.to_dict() for comment in self.comments]
        }

    def save(self):
        """Save post to the global posts list and persist to disk."""
        global posts
        existing_post = next((post for post in posts if post.post_id == self.post_id), None)
        if existing_post:
            existing_post.author_username = self.author_username
            existing_post.title = self.title
            existing_post.description = self.description
            existing_post.image_url = self.image_url
            existing_post.updated_at = datetime.utcnow()
            existing_post.likes = self.likes
            existing_post.comments = self.comments
        else:
            posts.append(self)
        save_state()

    def add_comment(self, username: str, description: str):
        """Add comment to post and persist to disk."""
        user = get_user_from_username(username)
        if not user:
            raise ValueError(f'User {username} not found')
        self.comments.append(Comment(username, description, profile_picture_url=user.profile_picture_url))
        save_state()
        
    def add_like(self, username: str):
        """Add like to post and persist to disk."""
        if username not in self.likes:
            self.likes.append(username)
            save_state()
            
    def remove_like(self, username: str):
        """Remove like from post and persist to disk."""
        if username in self.likes:
            self.likes.remove(username)
            save_state()

def get_posts():
    """Get all posts from the global posts list."""
    global posts
    return posts

def get_post_by_id(post_id: str) -> Optional[Post]:
    """Get post by ID from the global posts list."""
    global posts
    for post in posts:
        if post.post_id == post_id:
            return post
    return None