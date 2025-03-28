import React, { useState } from 'react';
import Comment from './Comment';

const Post = ({ post = {}, currentUser, onAddComment, onToggleLike }) => {
  const [newComment, setNewComment] = useState('');
  const [showAllLikes, setShowAllLikes] = useState(false);

  const handleSubmitComment = (e) => {
    e.preventDefault();
    if (newComment.trim()) {
      onAddComment(post.post_id, newComment);
      setNewComment('');
    }
  };

  const likes = post?.likes || [];
  const userLiked = currentUser && likes.includes(currentUser.username);
  
  const comments = post?.comments || [];

  const renderLikesPreview = () => {
    if (likes.length === 0) return null;
    
    const MAX_DISPLAYED_LIKES = 3;
    let likesText = '';
    
    if (likes.length <= MAX_DISPLAYED_LIKES) {
      likesText = likes.join(', ');
    } else if (showAllLikes) {
      likesText = likes.join(', ');
    } else {
      likesText = `${likes.slice(0, MAX_DISPLAYED_LIKES).join(', ')} ... and ${likes.length - MAX_DISPLAYED_LIKES} more`;
    }
    
    return (
      <div className="likes-preview">
        <span>
          Liked by: {likesText}
        </span>
        {likes.length > MAX_DISPLAYED_LIKES && (
          <button 
            className="show-likes-btn" 
            onClick={() => setShowAllLikes(!showAllLikes)}
          >
            {showAllLikes ? 'Show less' : 'Show all'}
          </button>
        )}
      </div>
    );
  };

  if (!post) return null;

  return (
    <div className="post">
      <div className="post-header">
        <div className="author-info">
          <img 
            src={post?.author_profile_picture || '/default-profile.png'} 
            alt={post?.author_id || 'Unknown'} 
            className="profile-pic" 
          />
          <span className="author-name">{post?.author_id || 'Unknown'}</span>
        </div>
      </div>
      
      <div className="post-content">
        <h3 className="post-title">{post?.title || 'Untitled Post'}</h3>
        <p className="post-description">{post?.description || 'No description'}</p>
        {post?.image_url && (
          <img 
            src={post.image_url} 
            alt={post.title || 'Post image'} 
            className="post-image" 
          />
        )}
      </div>
      
      <div className="post-actions">
        <button 
          className={`like-button ${userLiked ? 'liked' : ''}`}
          onClick={() => onToggleLike(post.post_id)}
        >
          {userLiked ? 'Unlike' : 'Like'} ({likes.length})
        </button>
      </div>
      
      {renderLikesPreview()}
      
      <div className="comments-section">
        <h4>Comments ({comments.length})</h4>
        
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
          {comments.map((comment, index) => (
            <Comment key={`comment-${post.post_id}-${index}`} comment={comment} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Post;