import React, { useState } from 'react';
import Login from './components/Login';
import SignUp from './components/Signup';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  const [user, setUser] = useState(null);

  const handleLogin = (credentials) => {
    // For now, just simulate login success
    console.log('Login submitted:', credentials);
    setUser(credentials.userId || credentials.username);
    setIsLoggedIn(true);
  };

  const handleSignup = (newUser) => {
    // For now, just simulate signup success
    console.log('Signup submitted:', newUser);
    setUser(newUser.userId);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
  };

  return (
    <div>
      {!isLoggedIn ? (
        <>
          {showSignup ? (
            <>
              <SignUp onSignup={handleSignup} />
              <p>
                Already have an account?{' '}
                <button onClick={() => setShowSignup(false)}>Login here</button>
              </p>
            </>
          ) : (
            <>
              <Login onLogin={handleLogin} />
              <p>
                Don't have an account?{' '}
                <button onClick={() => setShowSignup(true)}>Sign up</button>
              </p>
            </>
          )}
        </>
      ) : (
        <div>
          <h2>Welcome, {user}!</h2>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}
    </div>
  );
}

export default App;
