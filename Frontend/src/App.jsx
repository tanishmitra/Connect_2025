import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import SignUp from './components/Signup';
import AddRegion from './components/AddRegion';
import AddSite from './components/AddSite';
import AddDevice from './components/AddDevice';

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [user, setUser] = useState(null);

    const handleLogin = (credentials) => {
        setUser(credentials.userId || credentials.username);
        setIsLoggedIn(true);
    };

    const handleSignup = (newUser) => {
        setUser(newUser.userId);
        setIsLoggedIn(true);
    };

    const handleLogout = () => {
        setIsLoggedIn(false);
        setUser(null);
    };

    return (
        <Router>
            <Routes>
                <Route
                    path="/"
                    element={
                        isLoggedIn
                            ? <Navigate to="/dashboard" />
                            : <Login onLogin={handleLogin} />
                    }
                />
                <Route
                    path="/dashboard"
                    element={
                        isLoggedIn
                            ? <Dashboard user={user} onLogout={handleLogout} />
                            : <Navigate to="/" />
                    }
                />
                <Route
                    path="/add-region"
                    element={
                        isLoggedIn
                            ? <AddRegion onLogout={handleLogout} />
                            : <Navigate to="/" />
                    }
                />
                <Route
                    path="/add-site"
                    element={
                        isLoggedIn
                            ? <AddSite onLogout={handleLogout} />
                            : <Navigate to="/" />
                    }
                />
                <Route
                    path="/add-device"
                    element={
                        isLoggedIn
                            ? <AddDevice onLogout={handleLogout} />
                            : <Navigate to="/" />
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
