# 🚀 NEXAFORGE - PHASE 2: CORE AI INFRASTRUCTURE (L2-L3)

Phase 2: Core AI Infrastructure focuses on implementing the Model AI Layer (L2) and the AI Task Routing Layer (L3) of the NexaForge system.

## ✅ Completed Components

### L2: Model AI Layer
- **Model Manager**: Handles all 10 core AI models for Team A
- **Model Information**: Complete metadata for each model
- **Model Selection**: Logic to select appropriate model for each task type
- **Download Framework**: Script generation for model downloads
- **Model Configuration**: JSON configuration with performance parameters

### L3: AI Task Routing Layer
- **Task Classification**: Intelligent routing based on task content
- **Model Assignment**: Maps tasks to appropriate AI models
- **Routing Statistics**: Tracking and analytics for routing decisions
- **Prompt Optimization**: System to optimize prompts before routing
- **Configuration Framework**: Flexible routing rules and algorithms

## 📁 Files Created

1. `phase2_core_ai.py` - Core implementation of L2 and L3 layers
2. `model_downloader.py` - Model download framework and scripts
3. `ai_config.json` - Comprehensive configuration for AI models and routing
4. `prompt_optimizer.py` - Prompt optimization for L3 routing layer
5. `PHASE2_README.md` - This documentation file

## 🤖 Available AI Models (Team A - L2)

The following 10 models form the core of the Team A AI infrastructure:

| Model Name | Size | Task Type | Description |
|------------|------|-----------|-------------|
| Qwen2.5-Coder-32B-Instruct | 32B | Coding | Coding & Development |
| Qwen2.5-72B | 72B | Reasoning | Reasoning & Analysis |
| Llama-3.1-70B-Instruct | 70B | General | General Assistant |
| DeepSeek-R1-70B-Distill | 70B | Logic | Mathematical & Logical Reasoning |
| Phi-3.5-Vision | 12B | Vision | Vision & OCR |
| Qwen-Audio | 7B | Audio | Speech-to-text |
| Qwen2-VL | 72B | Multimodal | Vision + Text |
| SmolAgent | 3B | Tools | Tool Execution |
| Nous-Hermes-3 | 70B | Creative | Creative Writing |
| Gemma-2-27B | 27B | Efficient | Efficient Inference |

## 🔄 AI Task Routing (L3)

The routing system uses keyword analysis and task classification to route incoming requests to the most appropriate model:

- **Coding tasks** → Qwen2.5-Coder-32B-Instruct
- **Reasoning tasks** → Qwen2.5-72B
- **General queries** → Llama-3.1-70B-Instruct
- **Vision tasks** → Phi-3.5-Vision
- **And more specialized routing for each model**

## 🛠️ Setup and Usage

### 1. Run the core AI system:

```bash
python phase2_core_ai.py
```

### 2. Use the model downloader to create download scripts:

```bash
python model_downloader.py
```

### 3. Use the prompt optimizer:

```bash
python prompt_optimizer.py
```

### 4. Configure the system with ai_config.json

The configuration file contains performance parameters, routing rules, and optimization settings that can be adjusted based on your system resources and requirements.

## ⚙️ Configuration Options

The `ai_config.json` file provides comprehensive control over:

- Model selection preferences and timeouts
- Routing rules and load balancing
- Prompt optimization parameters
- Performance tuning (caching, batching, streaming)

## 📊 Performance Considerations

- Models range from 3B to 72B parameters
- Different GPU memory requirements for each model
- Configurable quantization to reduce memory usage
- Load balancing and caching mechanisms

## 🚀 Next Steps

After completing Phase 2, you can proceed to Phase 3: Agent System (L4) where we'll implement the AI Agent Layer with memory management, tools execution, and task decomposition capabilities.

## 📋 Model Download Notes

⚠️ **Important**: The actual model files are not included due to their large size (3B to 72B parameters require 10GB to 140GB+ of storage).

The model downloader creates shell scripts to download the models from Hugging Face Hub using the `huggingface-cli`. Each script is specific to a model and includes:
- Repository information
- Download commands
- Verification steps
- Size information

To download a model, execute its corresponding script:
```bash
bash download_qwen2_5_coder_32b_instruct.sh
```