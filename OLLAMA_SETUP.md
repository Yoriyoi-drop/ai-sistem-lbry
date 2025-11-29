# Ollama Setup Guide for Infinite AI Security

This document provides instructions for setting up Ollama with Docker to run AI models in the Infinite AI Security project.

## Prerequisites

- Docker and Docker Compose installed
- At least 15GB of free disk space for models
- (Optional) NVIDIA GPU with CUDA drivers for GPU acceleration

## Quick Start

### 1. Start Ollama Service

```bash
# Start Ollama service only
docker-compose -f docker-compose.ollama.yml up -d ollama

# Or start Ollama with web UI
docker-compose -f docker-compose.ollama.yml up -d
```

### 2. Pull the Qwen Model

```bash
# Pull the model (first time setup)
docker exec -it infinite-ai-ollama ollama pull qwen2.5:7b-instruct

# Or pull other models as needed
docker exec -it infinite-ai-ollama ollama pull llama3.1
```

### 3. Verify Installation

```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# List available models
curl http://localhost:11434/api/tags
```

## Using Ollama with the AI Security System

### Option 1: Start Complete Stack with Ollama

```bash
# Create a combined docker-compose file
docker-compose -f docker-compose.yml -f docker-compose.ollama.yml up -d
```

### Option 2: Use Environment File

```bash
# Copy the environment file
cp .env.ollama .env

# Start the services with Ollama
docker-compose up -d
```

### Option 3: Manual Configuration

Configure your application to connect to Ollama by setting these environment variables:

```bash
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=qwen2.5:7b-instruct
```

## Available Models

The following models are recommended for the security system:

### Security-Focused Models:
- `qwen2.5:7b-instruct` - Main model for security tasks
- `llama3.1` - General purpose model
- `mistral` - Fast security analysis
- `codellama` - Code security analysis

### Pull Recommended Models:

```bash
# Pull all recommended models
docker exec -it infinite-ai-ollama ollama pull qwen2.5:7b-instruct
docker exec -it infinite-ai-ollama ollama pull llama3.1
docker exec -it infinite-ai-ollama ollama pull mistral
docker exec -it infinite-ai-ollama ollama pull codellama
```

## GPU Acceleration

If you have an NVIDIA GPU, you can enable GPU acceleration for faster model processing:

1. Install NVIDIA Docker runtime:
```bash
# Add NVIDIA package repositories
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Install nvidia-container-toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Restart Docker daemon
sudo systemctl restart docker
```

2. Verify GPU access:
```bash
docker run --rm --gpus all nvidia/cuda:11.0-base-ubuntu20.04 nvidia-smi
```

3. To enable GPU support, uncomment the GPU configuration in `docker-compose.ollama.yml`:
```yaml
# Uncomment the following for GPU support if you have NVIDIA GPU
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
# Alternative for older Docker versions:
# runtime: nvidia
# environment:
#   - NVIDIA_VISIBLE_DEVICES=all
```

4. If you encounter issues with GPU initialization (like `libnvidia-ml.so.1` errors), your system may not have the required NVIDIA drivers. In this case, use the CPU-only configuration which is already set up in the default `docker-compose.ollama.yml`.

## Troubleshooting

### Common Issues

0. **Docker daemon not running**
   - Make sure Docker is installed and running
   - On Linux: `sudo systemctl start docker`
   - On Windows/Mac with Docker Desktop: Start Docker Desktop app
   - Verify with: `docker ps`

1. **Port already in use**
   - Ensure port 11434 is free
   - Check with: `netstat -tulpn | grep :11434`

2. **Insufficient disk space**
   - Free up space before pulling models
   - Clean old Docker images: `docker system prune`

3. **Permission errors**
   - Check Docker permissions
   - Ensure you're running as a user in the docker group

4. **Model loading fails**
   - Verify model name: `docker exec -it ollama ollama list`
   - Check available disk space in the volume

### API Testing

Test the Ollama API directly:

```bash
# Simple test
curl http://localhost:11434/api/tags

# Chat completion test
curl http://localhost:11434/api/chat -d '{
  "model": "qwen2.5:7b-instruct",
  "messages": [
    {"role": "user", "content": "Hello, how can you help with security?"}
  ]
}'
```

## Security Considerations

- The Ollama API is only accessible from the Docker network by default
- Use authentication if exposing Ollama API externally
- Regularly update the Ollama Docker image for security patches
- Monitor model usage and resource consumption

## Stopping Services

```bash
# Stop only Ollama
docker-compose -f docker-compose.ollama.yml down

# Stop with volumes (removes data)
docker-compose -f docker-compose.ollama.yml down -v
```

## Updating Models

```bash
# Pull the latest model version
docker exec -it infinite-ai-ollama ollama pull qwen2.5:7b-instruct

# Check for updates
docker exec -it infinite-ai-ollama ollama list
```