// App.js - Main React Component for AI Team Dashboard
import React, { useState, useEffect } from 'react';
import './App.css';
import ModelCard from './ModelCard';
import SystemInfo from './SystemInfo';
import QuickActions from './QuickActions';

const AI_MODELS = [
    'qwen2.5-coder',
    'llama3.1:70b', 
    'deepseek-r1:32b',
    'phi3-vision',
    'qwen2-vl',
    'smollm:3b',
    'gemma2:27b',
    'llama-guard3'
];

function App() {
    const [modelStatus, setModelStatus] = useState({});
    const [systemInfo, setSystemInfo] = useState({
        containerStatus: 'unknown',
        totalModels: AI_MODELS.length,
        activeModels: 0,
        memoryUsage: '--'
    });
    const [lastUpdated, setLastUpdated] = useState(new Date());

    // Fetch model status from Ollama API
    const fetchModelStatus = async () => {
        const newStatus = {};
        let activeCount = 0;

        for (const modelName of AI_MODELS) {
            try {
                const startTime = Date.now();
                const response = await fetch(`http://localhost:11434/api/generate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        model: modelName,
                        prompt: "Hello, are you available?",
                        stream: false
                    })
                });

                const responseTime = Date.now() - startTime;

                if (response.ok) {
                    newStatus[modelName] = { status: 'active', responseTime };
                    activeCount++;
                } else {
                    newStatus[modelName] = { status: 'inactive', responseTime: '--' };
                }
            } catch (error) {
                newStatus[modelName] = { status: 'error', responseTime: '--' };
            }
        }

        setModelStatus(newStatus);
        setSystemInfo(prev => ({
            ...prev,
            activeModels: activeCount
        }));
        setLastUpdated(new Date());
    };

    // Fetch system status from Ollama API
    const fetchSystemStatus = async () => {
        try {
            const response = await fetch(`http://localhost:11434/api/tags`);
            if (response.ok) {
                setSystemInfo(prev => ({ ...prev, containerStatus: 'running' }));
            } else {
                setSystemInfo(prev => ({ ...prev, containerStatus: 'error' }));
            }
        } catch (error) {
            setSystemInfo(prev => ({ ...prev, containerStatus: 'offline' }));
        }
    };

    // Update all statuses
    const updateAllStatus = async () => {
        await fetchSystemStatus();
        await fetchModelStatus();
    };

    // Initial load and set up auto-refresh
    useEffect(() => {
        updateAllStatus();
        const interval = setInterval(updateAllStatus, 30000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="App">
            <header className="app-header">
                <h1>NexaForge AI Team Dashboard</h1>
                <div>
                    <button className="btn btn-primary" onClick={updateAllStatus}>
                        Refresh Status
                    </button>
                    <span className="last-updated ms-3">
                        Last updated: {lastUpdated.toLocaleTimeString()}
                    </span>
                </div>
            </header>

            <div className="main-content">
                <div className="left-panel">
                    <div className="card mb-4">
                        <div className="card-header">
                            <h5>AI Team Status</h5>
                        </div>
                        <div className="card-body">
                            <div className="model-grid">
                                {AI_MODELS.map(modelName => (
                                    <ModelCard 
                                        key={modelName} 
                                        modelName={modelName} 
                                        status={modelStatus[modelName] || { status: 'loading', responseTime: '--' }} 
                                    />
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                <div className="right-panel">
                    <SystemInfo systemInfo={systemInfo} />
                    <QuickActions />
                </div>
            </div>
        </div>
    );
}

export default App;