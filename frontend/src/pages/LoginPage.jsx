import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { sign } from "../utils/cryptoUtil";

const LoginPage = ({ setCurrentUser }) => {
  const [username, setUsername] = useState("");
  const [privateKey, setPrivateKey] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const url = `http://127.0.0.1:3000/create_challenge`;
      const challengeResponse = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username }),
      });

      const challengeData = await challengeResponse.json();

      if (!challengeResponse.ok) {
        throw new Error(challengeData.message || "Failed to get challenge");
      }

      const challengeString = challengeData.challenge.challenge_string;

      const signedChallenge = await sign(challengeString, privateKey);

      const url2 = `http://127.0.0.1:3000/login`;
      const loginResponse = await fetch(url2, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          challenge_signature: signedChallenge,
        }),
      });

      const loginData = await loginResponse.json();

      if (!loginResponse.ok) {
        throw new Error(loginData.message || "Login failed");
      }

      const userInfo = {
        username,
        privateKey,
        ...loginData.user,
      };
      
      setCurrentUser(userInfo);
      
      localStorage.setItem("username", username);
      sessionStorage.setItem("privateKey", privateKey);

      navigate("/posts");
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <h1>Login</h1>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleLogin}>
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
            <label>Private Key</label>
            <textarea
              value={privateKey}
              onChange={(e) => setPrivateKey(e.target.value)}
              disabled={isLoading}
              required
              rows={4}
            />
            <p className="helper-text">
              Paste your private key here. This key is only used locally to sign
              the challenge.
            </p>
          </div>
          <button type="submit" className="primary-btn" disabled={isLoading}>
            {isLoading ? "Logging in..." : "Login"}
          </button>
        </form>

        <div className="auth-footer">
          <p>Don't have an account?</p>
          <Link to="/register">Go To Register</Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;