import React from 'react';

const Comment = ({ comment }) => {
  return (
    <div className="comment">
      <div className="comment-header">
        <img 
          src={comment.authorPic} 
          alt={comment.author} 
          className="profile-pic small" 
        />
        <span className="comment-author">{comment.author}</span>
      </div>
      <p className="comment-content">{comment.content}</p>
    </div>
  );
};

export default Comment;