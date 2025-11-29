// SystemInfo.js - Component to display system information
import React from 'react';

const SystemInfo = ({ systemInfo }) => {
    const getStatusClass = (status) => {
        switch (status) {
            case 'running': return 'bg-success';
            case 'error': return 'bg-danger';
            case 'offline': return 'bg-danger';
            default: return 'bg-secondary';
        }
    };

    const getStatusText = (status) => {
        switch (status) {
            case 'running': return 'Running';
            case 'error': return 'Error';
            case 'offline': return 'Offline';
            default: return 'Unknown';
        }
    };

    return (
        <div className="card mb-4">
            <div className="card-header">
                <h5>System Information</h5>
            </div>
            <div className="card-body">
                <ul className="list-group list-group-flush">
                    <li className="list-group-item d-flex justify-content-between align-items-center">
                        <span>Ollama Container</span>
                        <span className={`badge ${getStatusClass(systemInfo.containerStatus)}`}>
                            {getStatusText(systemInfo.containerStatus)}
                        </span>
                    </li>
                    <li className="list-group-item d-flex justify-content-between align-items-center">
                        <span>API Endpoint</span>
                        <span>http://localhost:11434</span>
                    </li>
                    <li className="list-group-item d-flex justify-content-between align-items-center">
                        <span>Total Models</span>
                        <span>{systemInfo.totalModels}</span>
                    </li>
                    <li className="list-group-item d-flex justify-content-between align-items-center">
                        <span>Active Models</span>
                        <span>{systemInfo.activeModels}</span>
                    </li>
                    <li className="list-group-item d-flex justify-content-between align-items-center">
                        <span>Memory Usage</span>
                        <span>{systemInfo.memoryUsage}</span>
                    </li>
                </ul>
            </div>
        </div>
    );
};

export default SystemInfo;