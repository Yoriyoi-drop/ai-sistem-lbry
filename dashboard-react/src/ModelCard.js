// ModelCard.js - Component to display individual model status
import React, { useState } from 'react';

const ModelCard = ({ modelName, status }) => {
    const [isTesting, setIsTesting] = useState(false);

    const testModel = async () => {
        setIsTesting(true);
        try {
            const startTime = Date.now();
            const response = await fetch(`http://localhost:11434/api/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: modelName,
                    prompt: "Hello, this is a test prompt to check if I'm working.",
                    stream: false
                })
            });

            const responseTime = Date.now() - startTime;

            if (response.ok) {
                alert(`Model ${modelName} responded successfully in ${responseTime}ms!`);
            } else {
                alert(`Model ${modelName} is not responding.`);
            }
        } catch (error) {
            alert(`Error testing model ${modelName}: ${error.message}`);
        } finally {
            setIsTesting(false);
        }
    };

    const getStatusClass = (status) => {
        switch (status) {
            case 'active': return 'status-active';
            case 'inactive': return 'status-inactive';
            case 'error': return 'status-error';
            case 'loading': return 'status-loading';
            default: return 'status-unknown';
        }
    };

    const getStatusText = (status) => {
        switch (status) {
            case 'active': return 'Active';
            case 'inactive': return 'Inactive';
            case 'error': return 'Error';
            case 'loading': return 'Loading...';
            default: return 'Unknown';
        }
    };

    return (
        <div className="model-card card h-100">
            <div className="card-body">
                <h6 className="card-title">
                    <span className={`status-indicator ${getStatusClass(status.status)}`}></span>
                    {modelName}
                </h6>
                <p className="card-text small">Status: {getStatusText(status.status)}</p>
                <p className="card-text small">Response Time: {status.responseTime}ms</p>
            </div>
            <div className="card-footer">
                <button 
                    className="btn btn-sm btn-outline-primary w-100" 
                    onClick={testModel}
                    disabled={isTesting}
                >
                    {isTesting ? 'Testing...' : 'Test Model'}
                </button>
            </div>
        </div>
    );
};

export default ModelCard;