import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const RegisterPage = () => {
  const [keyPair, setKeyPair] = useState({ publicKey: '', privateKey: '' });
  const [username, setUsername] = useState('');
  const [profilePic, setProfilePic] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const generateKeys = () => {
    window.crypto.subtle.generateKey(
      {
        name: "RSA-OAEP",
        modulusLength: 2048,
        publicExponent: new Uint8Array([1, 0, 1]),
        hash: "SHA-256",
      },
      true,
      ["encrypt", "decrypt"]
    )
    .then((keyPair) => {
      const exportPublicKey = window.crypto.subtle.exportKey(
        "spki",
        keyPair.publicKey
      );
      
      const exportPrivateKey = window.crypto.subtle.exportKey(
        "pkcs8",
        keyPair.privateKey
      );
      
      Promise.all([exportPublicKey, exportPrivateKey])
        .then(([publicKey, privateKey]) => {
          const publicKeyBase64 = btoa(String.fromCharCode(...new Uint8Array(publicKey)));
          const privateKeyBase64 = btoa(String.fromCharCode(...new Uint8Array(privateKey)));
          
          setKeyPair({
            publicKey: publicKeyBase64,
            privateKey: privateKeyBase64
          });
        });
    });
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
      const url = `http://127.0.0.1:3000/register`
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          public_key: keyPair.publicKey,
          profile_pic: profilePic
        }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || 'Registration failed');
      }
      
      alert('Registration successful! Please save your private key securely before proceeding to login.');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <h1>Register</h1>
        {error && <div className="error-message">{error}</div>}
        
        <div className="key-generation">
          <h2>Generate RSA 2048 Key Pair</h2>
          <button 
            onClick={generateKeys} 
            className="secondary-btn"
            disabled={isLoading}
          >
            Generate Keys
          </button>
          
          <div className="form-group">
            <label>Public Key</label>
            <div className="copy-field">
              <textarea value={keyPair.publicKey} readOnly rows={3} />
              <button 
                onClick={() => copyToClipboard(keyPair.publicKey)}
                className="copy-btn"
                disabled={!keyPair.publicKey || isLoading}
              >
                Copy
              </button>
            </div>
          </div>
          
          <div className="form-group">
            <label>Private Key <span className="important-text">(Save this securely!)</span></label>
            <div className="copy-field">
              <textarea value={keyPair.privateKey} readOnly rows={3} />
              <button 
                onClick={() => copyToClipboard(keyPair.privateKey)}
                className="copy-btn"
                disabled={!keyPair.privateKey || isLoading}
              >
                Copy
              </button>
            </div>
          </div>
        </div>
        
        <form onSubmit={handleRegister}>
          <h2>Register Account</h2>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={isLoading}
              required
            />
          </div>
          <div className="form-group">
            <label>Public Key</label>
            <textarea
              value={keyPair.publicKey}
              readOnly
              required
              rows={3}
            />
          </div>
          <div className="form-group">
            <label>Profile Picture URL</label>
            <input
              type="url"
              value={profilePic}
              onChange={(e) => setProfilePic(e.target.value)}
              disabled={isLoading}
              required
            />
            {profilePic && (
              <div className="profile-preview">
                <img src={profilePic} alt="Profile preview" />
              </div>
            )}
          </div>
          <button 
            type="submit" 
            className="primary-btn"
            disabled={isLoading || !username || !keyPair.publicKey || !profilePic}
          >
            {isLoading ? 'Registering...' : 'Register'}
          </button>
        </form>
        
        <div className="auth-footer">
          <p>Already have an account?</p>
          <Link to="/login">Go To Login</Link>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;