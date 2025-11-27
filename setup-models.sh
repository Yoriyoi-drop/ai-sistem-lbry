#!/bin/bash

####################################################################
# NexaForge AI - Model Setup Script
# Download dan setup Qwen model untuk sistem AI
####################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  NexaForge AI Model Setup                                  ║"
echo "║  Download & Install Qwen2.5-7B Model                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check available space
SPACE_NEEDED=20
SPACE_AVAILABLE=$(df /home | awk 'NR==2 {print int($4/1048576)}')

echo -e "${YELLOW}[1/5]${NC} Checking disk space..."
echo "  Available: ${SPACE_AVAILABLE}GB"
echo "  Required: ${SPACE_NEEDED}GB"

if [ $SPACE_AVAILABLE -lt $SPACE_NEEDED ]; then
    echo -e "${RED}✗ Not enough disk space!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Disk space OK${NC}"

# Check Python
echo -e "${YELLOW}[2/5]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 not found${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Check transformers
echo -e "${YELLOW}[3/5]${NC} Checking transformers library..."
if ! python3 -c "import transformers" 2>/dev/null; then
    echo -e "${YELLOW}  Installing transformers...${NC}"
    pip install --quiet transformers torch
fi
echo -e "${GREEN}✓ Transformers installed${NC}"

# Download model
echo -e "${YELLOW}[4/5]${NC} Downloading Qwen2.5-7B-Instruct model..."
echo -e "${CYAN}  This may take 5-15 minutes depending on internet speed${NC}"

python3 << 'PYTHON_EOF'
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

print("📥 Downloading model...")
try:
    model_name = "Qwen/Qwen2.5-7B-Instruct"
    
    print(f"  • Model: {model_name}")
    print(f"  • Size: ~15GB")
    
    # Download tokenizer
    print("  ⏳ Downloading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("  ✓ Tokenizer downloaded")
    
    # Download model
    print("  ⏳ Downloading model (this may take several minutes)...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    print("  ✓ Model downloaded")
    
    # Get cache location
    cache_path = os.path.expanduser("~/.cache/huggingface/hub")
    print(f"\n✓ Model saved to: {cache_path}")
    
    # Show disk usage
    total_size = 0
    for root, dirs, files in os.walk(cache_path):
        for file in files:
            total_size += os.path.getsize(os.path.join(root, file))
    
    size_gb = total_size / (1024**3)
    print(f"✓ Total model size: {size_gb:.2f}GB")
    
except Exception as e:
    print(f"✗ Error downloading model: {e}")
    exit(1)

print("\n✓ Model download complete!")
PYTHON_EOF

echo -e "${GREEN}✓ Model downloaded successfully${NC}"

# Verify model
echo -e "${YELLOW}[5/5]${NC} Verifying model installation..."

python3 << 'VERIFY_EOF'
from transformers import AutoModelForCausalLM, AutoTokenizer

try:
    model_name = "Qwen/Qwen2.5-7B-Instruct"
    
    # Load model
    print("  Loading model...")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Test inference
    print("  Testing inference...")
    text = "What is artificial intelligence?"
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=50)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print(f"  ✓ Model test successful")
    print(f"  Sample output: {result[:100]}...")
    
except Exception as e:
    print(f"  ✗ Model verification failed: {e}")
    exit(1)

print("\n✓ Model verification complete!")
VERIFY_EOF

echo -e "${GREEN}✓ Model verified${NC}"

echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✓ MODEL SETUP COMPLETE                                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo ""
echo -e "${CYAN}📋 Next Steps:${NC}"
echo ""
echo "1. Copy model to Docker volume:"
echo "   ${BLUE}docker volume create ai-models${NC}"
echo "   ${BLUE}docker run -v ai-models:/models -v ~/.cache:/cache alpine cp -r /cache/huggingface/hub /models/${NC}"
echo ""
echo "2. Update docker-compose.yml to mount model volume:"
echo "   ${BLUE}volumes:${NC}"
echo "   ${BLUE}  - ai-models:/root/.cache/huggingface/hub${NC}"
echo ""
echo "3. Restart containers:"
echo "   ${BLUE}sudo systemctl restart nexaforge-24-7${NC}"
echo ""
echo "4. Test model in container:"
echo "   ${BLUE}docker exec infinite-ai-api python -c \"from transformers import AutoModel; print('✓ Model loaded')\"${NC}"
echo ""

exit 0
