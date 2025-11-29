// QuickActions.js - Component for quick action buttons
import React from 'react';

const QuickActions = () => {
    const handlePullModels = () => {
        if (!confirm('This will pull all AI Team models. This may take a while and use significant bandwidth. Continue?')) {
            return;
        }
        alert('In a real implementation, this would start pulling all AI Team models. For this demo, we are simulating the action.');
        console.log('Simulating: Pulling all models');
    };

    const handleRestartContainer = () => {
        if (!confirm('Restart the Ollama container? This will temporarily interrupt service.')) {
            return;
        }
        alert('In a real implementation, this would restart the Ollama Docker container.');
        console.log('Simulating: Restarting container');
    };

    const handleCheckModels = () => {
        alert('Checking status of all models...');
        // This would trigger a refresh of model status
        window.location.reload();
    };

    return (
        <div className="card mb-4">
            <div className="card-header">
                <h5>Quick Actions</h5>
            </div>
            <div className="card-body">
                <button className="btn btn-success w-100 mb-2" onClick={handlePullModels}>
                    Pull AI Team Models
                </button>
                <button className="btn btn-warning w-100 mb-2" onClick={handleRestartContainer}>
                    Restart Container
                </button>
                <button className="btn btn-info w-100" onClick={handleCheckModels}>
                    Check All Models
                </button>
            </div>
        </div>
    );
};

export default QuickActions;