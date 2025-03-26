import React from 'react';

const Comment = ({ comment }) => {
  if (!comment) return null;
  
  return (
    <div className="comment">
      <div className="comment-header">
        <img 
          src={comment.profile_picture_url || '/default-profile.png'} 
          alt={comment.username || 'Unknown'} 
          className="comment-profile-pic" 
        />
        <span className="comment-author">{comment.username}</span>
      </div>
      <div className="comment-content">
        <p>{comment.description}</p>
      </div>
    </div>
  );
};

export default Comment;