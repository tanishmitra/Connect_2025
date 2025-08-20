import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import './css/AddPageFormat.css';

const AddRegion = () => {
    const [regionName, setRegionName] = useState('');
    const [regions, setRegions] = useState([]);
    const [message, setMessage] = useState('');
    const navigate = useNavigate();
    const onLogout = () => {
        navigate('/');
    };

    const handleAddRegion = (e) => {
        e.preventDefault();

        const trimmedName = regionName.trim();

        if (!trimmedName) {
            setMessage('Region name cannot be empty.');
            return;
        }

        if (regions.includes(trimmedName)) {
            setMessage('Region already exists.');
            return;
        }

        setRegions([...regions, trimmedName]);
        setRegionName('');
        setMessage('Region added successfully.');
    };

    return (
        <div className="dashboard-wrapper">
            <Navbar onLogout={onLogout} />
            <div className="add-region-container">
                <button className="back-button" onClick={() => navigate('/dashboard')} style={{marginBottom: '15px'}}>Back to Dashboard</button>
                <h2>Add New Region</h2>
                <form onSubmit={handleAddRegion}>
                    <input
                        type="text"
                        placeholder="Enter region name"
                        value={regionName}
                        onChange={(e) => setRegionName(e.target.value)}
                    />
                    <button type="submit">Add Region</button>
                </form>
                {message && <p className="message">{message}</p>}

                {regions.length > 0 && (
                    <div className="region-list">
                        <h3>Added Regions:</h3>
                        <table className="region-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Region Name</th>
                                </tr>
                            </thead>
                            <tbody>
                                {regions.map((region, index) => (
                                    <tr key={index}>
                                        <td>{index + 1}</td>
                                        <td>{region}</td>
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

export default AddRegion;
