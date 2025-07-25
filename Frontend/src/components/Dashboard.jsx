import React from 'react';
import Navbar from './Navbar';


const Dashboard = ({ user, onLogout }) => {
  return (
    <div className="dashboard-wrapper">
      <Navbar onLogout={onLogout} />
      <div className="dashboard-content">
        <h2>Welcome, {user}!</h2>
        <p>Select an option from the sidebar.</p>
      </div>
    </div>
  );
};

export default Dashboard;
