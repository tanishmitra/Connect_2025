import React, { useState } from 'react';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Input validation
    if (!username || !password) {
      setError('Both fields are required.');
      return;
    }

    setError('');
    onLogin({ username, password }); // Send data to App component
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>

        <label>Username:</label><br />
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter your username"
        /><br /><br />

        <label>Password:</label><br />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
        /><br /><br />

        {error && <div style={{ color: 'red' }}>{error}</div>}<br />

        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
