import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './css/Login.css';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!username || !password) {
      setError('Both fields are required.');
      return;
    }

    try {
      const response = await axios.post('http://localhost:8787/login', {
        UserName: username,
        UserPassword: password,
      });

      const msg = response.data.Message;
      if (msg ==="SuccessLogin") {
        onLogin({ username });
        navigate('/dashboard');
      } else {
        setError("Invalid username or password.");
      }
    } catch (err) {
      setError("Network or server error: " + err.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <label>Username:</label><br />
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} /><br /><br />
        <label>Password:</label><br />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /><br /><br />
        {error && <div style={{ color: 'red' }}>{error}</div>}<br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
