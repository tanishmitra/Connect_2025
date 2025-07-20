import React, { useState } from 'react';
import axios from 'axios';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!username || !password) {
      setError('Both fields are required.');
      return;
    }

    try {
      const response = await axios.post('http://localhost:8080/api/login', {
        username,
        password,
      });

      if (response.status === 200) {
        onLogin({ username });
      } else {
        setError('Login failed.');
      }
    } catch (err) {
      setError('Login error: ' + (err.response?.data?.message || err.message));
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
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
