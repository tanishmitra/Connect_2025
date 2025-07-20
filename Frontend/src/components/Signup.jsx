import React, { useState } from 'react';

function SignUp({ onSignup }) {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!userId || !password) {
      setError('Both fields are required.');
      return;
    }

    setError('');
    onSignup({ userId, password }); // Send data to parent (App.jsx)
  };

  return (
    <div className="signup-container">
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>

        <label>User ID:</label><br />
        <input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="Enter your user ID"
        /><br /><br />

        <label>Password:</label><br />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
        /><br /><br />

        {error && <div style={{ color: 'red' }}>{error}</div>}<br />

        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default SignUp;
