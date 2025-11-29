# Ollama Integration for Infinite AI Security

This project integrates Ollama to run local AI models for security-focused tasks. The setup includes Docker configuration, model management, and integration with the existing security AI system.

## Table of Contents
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Model Management](#model-management)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## Architecture

The Ollama integration includes:

- **Ollama Service**: Runs local AI models with REST API
- **Ollama Web UI**: Optional web interface for model management
- **Security AI Agents**: Multiple specialized AI agents for security tasks
- **Database**: PostgreSQL for data persistence
- **Cache**: Redis for fast data access
- **Monitoring**: Prometheus and Grafana for system metrics

## Prerequisites

- Docker Engine (20.10.0 or later)
- Docker Compose (2.0.0 or later)
- At least 20GB free disk space for models
- (Optional) NVIDIA GPU with CUDA for acceleration

## Quick Start

### 1. Start Ollama Service
```bash
# Start Ollama only
docker-compose -f docker-compose.ollama.yml up -d ollama

# Or start with Web UI
docker-compose -f docker-compose.ollama.yml up -d

# Or integrate with the full security stack
docker-compose -f docker-compose.yml -f docker-compose.ollama.yml up -d
```

### 2. Pull Required Models
```bash
# Make sure script is executable
chmod +x pull_ollama_models.sh

# Pull default security models
./pull_ollama_models.sh

# Or pull specific models
./pull_ollama_models.sh qwen2.5:7b-instruct llama3.1
```

### 3. Configure Environment
```bash
# Copy the environment file
cp .env.ollama .env

# Or set specific variables
export OLLAMA_HOST=http://localhost:11434
export MODEL_NAME=qwen2.5:7b-instruct
```

### 4. Start the Security System
```bash
# Start with docker-compose
docker-compose up -d

# Or run the main application
python main.py
```

## Model Management

### Available Models

Recommended models for security tasks:

- `qwen2.5:7b-instruct` - Primary security model
- `llama3.1` - General purpose tasks
- `mistral` - Fast analysis
- `codellama` - Code security analysis

### Pull Models Manually

```bash
# Pull a specific model
docker exec -it infinite-ai-ollama ollama pull qwen2.5:7b-instruct

# List available models
docker exec -it infinite-ai-ollama ollama list

# Check model info
curl http://localhost:11434/api/tags
```

### Model Configuration

The system uses the following configuration in `ai_config.json`:

```json
{
  "model_config": {
    "default_model": "qwen2.5:7b-instruct",
    "model_selection_timeout": 30,
    "max_concurrent_models": 4
  },
  "routing_config": {
    "enable_intelligent_routing": true,
    "fallback_model": "qwen2.5:7b-instruct",
    "enable_load_balancing": true
  }
}
```

## Usage

### API Endpoints

Once running, the system provides these endpoints:

- `http://localhost:11434` - Ollama API
- `http://localhost:8000/health` - Health check
- `http://localhost:8000/chat` - Chat interface
- `http://localhost:3001` - Ollama Web UI (if enabled)

### Security AI Roles

The system implements multiple specialized AI agents:

- **AstraMind**: Strategic planning
- **SpectraLogic**: Analysis and vulnerability assessment
- **ForgeRun**: Implementation
- **GuardianOS**: Validation and compliance
- **ChronaCore**: Memory and context management

### Example API Call

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze this security configuration for potential vulnerabilities",
    "context": {}
  }'
```

## GPU Acceleration

For GPU acceleration (NVIDIA only):

1. Install NVIDIA Container Toolkit:
```bash
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

2. Verify GPU access:
```bash
docker run --gpus all nvidia/cuda:11.0-base-ubuntu20.04 nvidia-smi
```

3. Start with GPU support:
```bash
docker-compose -f docker-compose.ollama.yml up -d
```

## Troubleshooting

### Common Issues

0. **Docker daemon not running**: Make sure Docker is installed and running
   - On Linux: `sudo systemctl start docker`
   - On Windows/Mac: Start Docker Desktop application
   - Verify with: `docker ps`
1. **Port conflicts**: Ensure ports 11434, 8000, 3000, 3001 are free
2. **Disk space**: Ensure at least 20GB free for models
3. **Docker permissions**: Add user to docker group: `sudo usermod -aG docker $USER`

### Health Checks

```bash
# Check if services are running
docker ps | grep -E "(ollama|infinite)"

# Check Ollama logs
docker logs infinite-ai-ollama

# Test API connectivity
curl http://localhost:11434/api/version
```

### Reset Setup

```bash
# Stop all services
docker-compose -f docker-compose.ollama.yml down

# Remove volumes (CAUTION: This deletes models)
docker-compose -f docker-compose.ollama.yml down -v

# Clean Docker system
docker system prune -a
```

## Development

### Custom Models

To use custom models:

1. Create a model file (Modelfile)
2. Import to Ollama:
```bash
docker cp Modelfile infinite-ai-ollama:/Modelfile
docker exec -it infinite-ai-ollama ollama create my-custom-model -f /Modelfile
```

### Model Fine-tuning

For security-specific fine-tuning, see the feedback collection system in `main.py` that stores user corrections in `data/feedback.jsonl`.

## Security Considerations

- API endpoints are restricted to localhost by default
- Use authentication when exposing services externally
- Regularly update model images for security patches
- Monitor resource usage to prevent abuse
- The system includes rate limiting and security validation

## Performance Tuning

Adjust these environment variables for performance:

- `OLLAMA_NUM_PARALLEL`: Number of parallel operations
- `OLLAMA_MAX_LOADED_MODELS`: Maximum models to keep in memory
- `TEMPERATURE`: Model creativity (0.0 to 1.0)
- `MAX_TOKENS`: Maximum response length

## Updating

```bash
# Update Ollama image
docker pull ollama/ollama:latest

# Pull latest models
docker exec -it infinite-ai-ollama ollama pull qwen2.5:7b-instruct

# Restart services
docker-compose -f docker-compose.ollama.yml restart
```

For detailed setup instructions, see [OLLAMA_SETUP.md](OLLAMA_SETUP.md).