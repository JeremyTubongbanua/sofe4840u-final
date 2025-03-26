import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import PostsPage from './pages/PostsPage';
import './App.css';

const App = () => {
  const [currentUser, setCurrentUser] = useState(() => {
    const username = localStorage.getItem('username');
    const privateKey = sessionStorage.getItem('privateKey');
    
    if (username) {
      return {
        username,
        privateKey: privateKey || ''
      };
    }
    return null;
  });

  useEffect(() => {
    if (currentUser && currentUser.username) {
      localStorage.setItem('username', currentUser.username);
      if (currentUser.privateKey) {
        sessionStorage.setItem('privateKey', currentUser.privateKey);
      }
    }
  }, [currentUser]);

  const handleLogout = () => {
    localStorage.removeItem('username');
    sessionStorage.removeItem('privateKey');
    setCurrentUser(null);
  };

  return (
    <Router>
      <div className="app">
        {currentUser && (
          <nav>
            <div className="nav-content">
              <a href="/posts">Posts</a>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </div>
          </nav>
        )}
        <Routes>
          <Route path="/login" element={<LoginPage setCurrentUser={setCurrentUser} />} />
          <Route path="/register" element={
            currentUser ? <Navigate to="/posts" /> : <RegisterPage />
          } />
          <Route path="/posts" element={
            currentUser ? <PostsPage currentUser={currentUser} /> : <Navigate to="/login" />
          } />
          <Route path="/" element={<Navigate to={currentUser ? "/posts" : "/login"} />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;