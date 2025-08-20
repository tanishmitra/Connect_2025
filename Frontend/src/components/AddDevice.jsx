import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import './css/AddPageFormat.css';

const AddDevice = () => {
  const [deviceName, setDeviceName] = useState('');
  const [devices, setDevices] = useState([]);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const onLogout = () => {
    navigate('/');
  };

  const handleAddDevice = (e) => {
    e.preventDefault();
    const trimmedName = deviceName.trim();
    if (!trimmedName) {
      setMessage('Device name cannot be empty.');
      return;
    }
    if (devices.includes(trimmedName)) {
      setMessage('Device already exists.');
      return;
    }
    setDevices([...devices, trimmedName]);
    setDeviceName('');
    setMessage('Device added successfully!');
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
        <h2>Add New Device</h2>
        <form onSubmit={handleAddDevice}>
          <input
            type="text"
            placeholder="Enter device name"
            value={deviceName}
            onChange={(e) => setDeviceName(e.target.value)}
          />
          <button type="submit">Add Device</button>
        </form>
        {message && <p className="message">{message}</p>}
        {devices.length > 0 && (
          <div className="region-list">
            <h3>Added Devices:</h3>
            <table className="region-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Device Name</th>
                </tr>
              </thead>
              <tbody>
                {devices.map((device, index) => (
                  <tr key={index}>
                    <td>{index + 1}</td>
                    <td>{device}</td>
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

export default AddDevice;