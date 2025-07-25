import React from 'react';
import './css/Navbar.css';

const Navbar = ({ onLogout }) => {
    return (
        <div className="sidebar">
            <h2 className="sidebar-title">Dashboard</h2>
            <nav className="nav-links">
                <button className="nav-item">Manage Region</button>
                <button className="nav-item">Manage Site</button>
                <button className="nav-item">Manage Device</button>
            </nav>
            <button onClick={onLogout} className="logout-button">Logout</button>
        </div>
    );
};

export default Navbar;
