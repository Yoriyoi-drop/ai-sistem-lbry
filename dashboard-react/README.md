# NexaForge AI Team Dashboard

A React-based dashboard for monitoring and managing your AI Team A running in Ollama Docker containers.

## Features

- Real-time monitoring of all 8 AI Team A models
- Status indicators for each model
- Response time measurements
- Quick action buttons for common operations
- System information panel
- Auto-refresh functionality

## Prerequisites

- Node.js (version 14 or higher)
- Docker with Ollama container running (container name: nexaforge-ollama)
- Ollama API accessible at http://localhost:11434

## Installation

1. Navigate to the dashboard directory:
   ```bash
   cd dashboard-react
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The dashboard will be available at http://localhost:3000

## Production Build

To create a production build:
```bash
npm run build
```

## Models Being Monitored

The dashboard monitors these 8 AI Team A models:

- qwen2.5-coder
- llama3.1:70b
- deepseek-r1:32b
- phi3-vision
- qwen2-vl
- smollm:3b
- gemma2:27b
- llama-guard3

## API Integration

The dashboard connects to the Ollama API at http://localhost:11434 to:

- Check model availability
- Test model responsiveness
- Monitor system status
- Pull new models (simulated in UI)

## Quick Actions

- **Pull AI Team Models**: Initiates download of all AI Team A models
- **Restart Container**: Restarts the Ollama Docker container
- **Check All Models**: Performs a comprehensive status check of all models