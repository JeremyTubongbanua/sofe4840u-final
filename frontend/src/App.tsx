import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import PostsPage from './pages/PostsPage';
import './App.css';

const App = () => {
  const [currentUser, setCurrentUser] = useState(() => {
    const saved = localStorage.getItem('currentUser');
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    if (currentUser) {
      localStorage.setItem('currentUser', JSON.stringify(currentUser));
    } else {
      localStorage.removeItem('currentUser');
    }
  }, [currentUser]);

  const handleLogout = () => {
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
          <Route path="/login" element={
            currentUser ? <Navigate to="/posts" /> : <LoginPage setCurrentUser={setCurrentUser} />
          } />
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