import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const LoginPage = ({ setCurrentUser }) => {
  const [username, setUsername] = useState("");
  const [privateKey, setPrivateKey] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const signChallenge = async (challengeString, privateKeyBase64) => {
    try {
      let privateKeyBytes;

      if (privateKeyBase64.includes("-----BEGIN")) {
        const pemContent = privateKeyBase64
          .replace(/-----(BEGIN|END) (PRIVATE KEY|RSA PRIVATE KEY)-----/g, "")
          .replace(/\s/g, "");
        privateKeyBytes = Uint8Array.from(atob(pemContent), (c) =>
          c.charCodeAt(0)
        );
      } else {
        privateKeyBytes = Uint8Array.from(atob(privateKeyBase64), (c) =>
          c.charCodeAt(0)
        );
      }

      let privateKey;
      try {
        privateKey = await window.crypto.subtle.importKey(
          "pkcs8",
          privateKeyBytes,
          {
            name: "RSA-PSS",
            hash: { name: "SHA-256" },
          },
          false, // not extractable
          ["sign"]
        );
      } catch (pkcs8Error) {
        try {
          privateKey = await window.crypto.subtle.importKey(
            "spki",
            privateKeyBytes,
            {
              name: "RSA-PSS",
              hash: { name: "SHA-256" },
            },
            false,
            ["sign"]
          );
        } catch (spkiError) {
          console.error("PKCS8 import failed:", pkcs8Error);
          console.error("SPKI import failed:", spkiError);
          throw new Error(
            "Failed to import private key in any supported format"
          );
        }
      }

      const challengeBytes = new TextEncoder().encode(challengeString);

      const signature = await window.crypto.subtle.sign(
        {
          name: "RSA-PSS",
          saltLength: 32, // This matches PSS.MAX_LENGTH in Python cryptography
        },
        privateKey,
        challengeBytes
      );

      const signatureBytes = new Uint8Array(signature);
      const signatureBase64 = btoa(
        String.fromCharCode.apply(null, signatureBytes)
      );

      return signatureBase64;
    } catch (error) {
      console.error("Error signing challenge:", error);
      throw new Error(`Failed to sign challenge: ${error.message}`);
    }
  };

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

      const signedChallenge = await signChallenge(challengeString, privateKey);

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

      setCurrentUser({
        username,
        privateKey,
        ...loginData.user,
      });

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
