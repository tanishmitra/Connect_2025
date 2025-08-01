import React, { useState } from 'react';
import axios from 'axios';
import './css/Signup.css';

function SignUp({ onSignup }) {
    const [userId, setUserId] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!userId || !password) {
            setError('Both fields are required.');
            return;
        }

        try {
            const response = await axios.post('http://localhost:8787/signup', {
                UserName: userId,
                UserPassword: password,
            });

            const msg = response.data.Message;

            if (msg === "SuccessSignup") {
                setError('');
                onSignup({ userId });
            } else if (msg === "UserAlreadyExists") {
                setError('User already exists');
            } else {
                setError('Signup failed');
            }
        } catch (err) {
            setError('Signup error: ' + (err.response?.data?.Message || err.message));
        }
        setLoading(false);
    };

    return (
        <div className="signup-container">
            <h2>Sign Up</h2>
            <form onSubmit={handleSubmit}>
                <label>Username:</label><br />
                <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} /><br /><br />
                <label>Password:</label><br />
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /><br /><br />
                {error && <div style={{ color: 'red' }}>{error}</div>}<br />
                <button type="submit" disabled={loading}>Sign Up</button>
            </form>
        </div>
    );
}

export default SignUp;
