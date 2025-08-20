import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import './css/AddPageFormat.css';

const AddSite = () => {
  const [siteName, setSiteName] = useState('');
  const [sites, setSites] = useState([]);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const onLogout = () => {
    navigate('/');
  };

  const handleAddSite = (e) => {
    e.preventDefault();
    const trimmedName = siteName.trim();
    if (!trimmedName) {
      setMessage('Site name cannot be empty.');
      return;
    }
    if (sites.includes(trimmedName)) {
      setMessage('Site already exists.');
      return;
    }
    setSites([...sites, trimmedName]);
    setSiteName('');
    setMessage('Site added successfully!');
  };

  return (
    <div className="dashboard-wrapper">
      <Navbar onLogout={onLogout} />
      <div className="add-region-container">
        <button
          type="button"
          className="back-button"
          onClick={() => navigate('/dashboard')}
          style={{ marginBottom: '15px' }}
        >
          Back to Dashboard
        </button>
        <h2>Add New Site</h2>
        <form onSubmit={handleAddSite}>
          <input
            type="text"
            placeholder="Enter site name"
            value={siteName}
            onChange={(e) => setSiteName(e.target.value)}
          />
          <button type="submit">Add Site</button>
        </form>
        {message && <p className="message">{message}</p>}
        {sites.length > 0 && (
          <div className="region-list">
            <h3>Added Sites:</h3>
            <table className="region-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Site Name</th>
                </tr>
              </thead>
              <tbody>
                {sites.map((site, index) => (
                  <tr key={index}>
                    <td>{index + 1}</td>
                    <td>{site}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default AddSite;