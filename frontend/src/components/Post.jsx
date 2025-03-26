import React, { useState } from 'react';
import Comment from './Comment';

const Post = ({ post, currentUser, onAddComment, onToggleLike }) => {
  const [newComment, setNewComment] = useState('');

  const handleSubmitComment = (e) => {
    e.preventDefault();
    if (newComment.trim()) {
      onAddComment(post.id, newComment);
      setNewComment('');
    }
  };

  const userLiked = post.likes.includes(currentUser.username);

  return (
    <div className="post">
      <div className="post-header">
        <div className="author-info">
          <img src={post.authorPic} alt={post.author} className="profile-pic" />
          <span className="author-name">{post.author}</span>
        </div>
      </div>
      
      <div className="post-content">
        <h3 className="post-title">{post.title}</h3>
        <p className="post-description">{post.description}</p>
      </div>
      
      <div className="post-actions">
        <button 
          className={`like-button ${userLiked ? 'liked' : ''}`}
          onClick={() => onToggleLike(post.id)}
        >
          {userLiked ? 'Unlike' : 'Like'} ({post.likes.length})
        </button>
      </div>
      
      <div className="comments-section">
        <h4>Comments ({post.comments.length})</h4>
        
        <form onSubmit={handleSubmitComment} className="add-comment">
          <input
            type="text"
            placeholder="Add a comment..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            required
          />
          <button type="submit">Submit</button>
        </form>
        
        <div className="comments-list">
          {post.comments.map(comment => (
            <Comment key={comment.id} comment={comment} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Post;