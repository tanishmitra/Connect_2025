import React, { useState } from 'react';
import Login from './components/Login.jsx';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);

  const handleLogin = ({ username, password }) => {
    console.log('Login submitted:', username, password);

    // Simulate login success
    setUserData({ username });
    setIsLoggedIn(true);
  };

  return (
    <div className="app">
      {isLoggedIn ? (
        <h2>Welcome, {userData.username}!</h2>
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
