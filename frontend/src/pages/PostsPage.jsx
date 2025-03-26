import React, { useState, useEffect, useRef } from "react";
import Post from "../components/Post";
import { sign } from "../utils/cryptoUtil";

const API_URL = "http://127.0.0.1:3000";

const PostsPage = ({ currentUser }) => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const fetchInProgress = useRef(false);

  const getChallenge = async (username) => {
    const challengeResponse = await fetch(`${API_URL}/create_challenge`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username }),
    });

    const challengeData = await challengeResponse.json();
    
    if (challengeData.status !== "successful") {
      throw new Error(
        "Failed to get challenge: " + (challengeData.message || "Unknown error")
      );
    }

    return challengeData.challenge;
  };

  const createSignature = async (challenge, privateKey) => {
    return await sign(challenge.challenge_string, privateKey);
  };

  const fetchPosts = async () => {
    if (fetchInProgress.current) return;
    fetchInProgress.current = true;

    if (!currentUser || !currentUser.username) {
      setError("User not logged in");
      setLoading(false);
      fetchInProgress.current = false;
      return;
    }

    try {
      setLoading(true);
      
      const challenge = await getChallenge(currentUser.username);
      const signature = await createSignature(challenge, currentUser.privateKey);
      
      console.log("Generated signature for /posts request");

      const postsResponse = await fetch(`${API_URL}/posts`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: currentUser.username,
          challenge_signature: signature,
        }),
      });

      const postsData = await postsResponse.json();
      console.log("Posts response:", postsData);

      if (postsData.status === "successful") {
        const formattedPosts = postsData.posts.map((post) => ({
          ...post,
          id: post.post_id,
          likes: post.likes || [],
          comments: post.comments || [],
        }));
        setPosts(formattedPosts);
        setError(null);
      } else {
        setError("Failed to fetch posts: " + postsData.message);
      }
    } catch (err) {
      console.error("Error fetching posts:", err);
      setError("Error: " + err.message);
    } finally {
      setLoading(false);
      fetchInProgress.current = false;
    }
  };

  const handleAddComment = async (postId, commentText) => {
    if (!currentUser || !currentUser.username) {
      setError("User not logged in");
      return;
    }
    
    try {
      const challenge = await getChallenge(currentUser.username);
      const signature = await createSignature(challenge, currentUser.privateKey);

      const response = await fetch(`${API_URL}/add_comment`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          username: currentUser.username,
          challenge_signature: signature,
          post_id: postId,
          comment: commentText,
        }),
        credentials: "include",
      });
      const responseData = await response.json();

      if (responseData.status === "successful") {
        fetchPosts();
      } else {
        setError("Failed to add comment: " + responseData.message);
      }
    } catch (err) {
      setError("Error: " + err.message);
      console.error("Error adding comment:", err);
    }
  };

  const handleToggleLike = async (postId) => {
    if (!currentUser || !currentUser.username) {
      setError("User not logged in");
      return;
    }
    
    try {
      const challenge = await getChallenge(currentUser.username);
      const signature = await createSignature(challenge, currentUser.privateKey);

      const response = await fetch(`${API_URL}/toggle_like`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          username: currentUser.username,
          challenge_signature: signature,
          post_id: postId,
        }),
        credentials: "include",
      });
      const responseData = await response.json();

      if (responseData.status === "successful") {
        setPosts(
          posts.map((post) => {
            if (post.id === postId || post.post_id === postId) {
              const userLiked = post.likes.includes(currentUser.username);
              const updatedLikes = userLiked
                ? post.likes.filter(
                    (username) => username !== currentUser.username
                  )
                : [...post.likes, currentUser.username];

              return { ...post, likes: updatedLikes };
            }
            return post;
          })
        );
      } else {
        setError("Failed to toggle like: " + responseData.message);
      }
    } catch (err) {
      setError("Error: " + err.message);
      console.error("Error toggling like:", err);
    }
  };

  useEffect(() => {
    if (currentUser?.username) {
      fetchPosts();
    } else {
      setLoading(false);
    }

    return () => {
      fetchInProgress.current = false;
    };
  }, [currentUser]);

  if (loading) {
    return <div className="loading">Loading posts...</div>;
  }

  if (!currentUser || !currentUser.username) {
    return <div className="error-container">Please log in to view posts</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={fetchPosts}>Try Again</button>
      </div>
    );
  }

  return (
    <div className="posts-page">
      <h1 className="page-title">Feed</h1>

      {posts.length === 0 ? (
        <div className="no-posts">No posts available</div>
      ) : (
        <div className="posts-container">
          {posts.map((post) => (
            <Post
              key={post.id || post.post_id || `post-${posts.indexOf(post)}`}
              post={post}
              currentUser={currentUser}
              onAddComment={handleAddComment}
              onToggleLike={handleToggleLike}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default PostsPage;