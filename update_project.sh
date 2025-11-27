#!/bin/bash
# Skrip untuk membuat dan mengupdate project Infinite AI Security

# Fungsi untuk membuat struktur project baru
create_project_structure() {
    echo "🔨 Membuat struktur project Infinite AI Security..."
    
    # Membuat direktori struktur
    mkdir -p src/{api,models,services,utils,agents,security}
    mkdir -p tests/{unit,integration}
    mkdir -p docs/api docs/security
    mkdir -p data/{logs,backups,models}
    
    # Membuat file utama
    touch src/__init__.py
    touch src/api/__init__.py
    touch src/models/__init__.py
    touch src/services/__init__.py
    touch src/utils/__init__.py
    touch src/agents/__init__.py
    touch src/security/__init__.py
    
    echo "✅ Struktur project dibuat"
}

# Fungsi untuk mengupdate dependencies
update_dependencies() {
    echo "🔄 Mengupdate dependencies..."
    
    # Cek apakah requirements.txt ada
    if [ -f "requirements.txt" ]; then
        # Backup requirements.txt lama
        cp requirements.txt requirements.txt.backup.$(date +%Y%m%d_%H%M%S)
        
        # Update dependencies ke versi terbaru yang kompatibel
        pip install --upgrade transformers torch fastapi uvicorn pydantic redis sqlalchemy python-dotenv
        pip freeze > requirements.txt
        
        echo "✅ Dependencies diupdate"
    else
        echo "⚠️ File requirements.txt tidak ditemukan, membuat baru..."
        echo "transformers>=4.35.0" > requirements.txt
        echo "torch>=2.1.0" >> requirements.txt
        echo "fastapi>=0.104.0" >> requirements.txt
        echo "uvicorn>=0.24.0" >> requirements.txt
        echo "pydantic>=2.5.0" >> requirements.txt
        echo "redis>=5.0.0" >> requirements.txt
        echo "sqlalchemy>=2.0.0" >> requirements.txt
        echo "python-dotenv>=1.0.0" >> requirements.txt
        echo "pytest>=7.4.0" >> requirements.txt
        echo "pytest-asyncio>=0.21.0" >> requirements.txt
    fi
}

# Fungsi untuk mengupdate konfigurasi
update_config() {
    echo "⚙️ Mengupdate konfigurasi sistem..."
    
    # Pastikan file .env ada
    if [ ! -f ".env" ]; then
        echo "⚠️ File .env tidak ditemukan, membuat baru..."
        touch .env
        
        # Isi default .env
        echo "# Konfigurasi untuk Infinite AI Security" >> .env
        echo "MODEL_NAME=Qwen/Qwen2.5-7B-Instruct" >> .env
        echo "TEMPERATURE=0.3" >> .env
        echo "MAX_TOKENS=2000" >> .env
        echo "REDIS_HOST=localhost" >> .env
        echo "REDIS_PORT=6379" >> .env
        echo "DATABASE_URL=sqlite:///./security.db" >> .env
        echo "LOG_LEVEL=INFO" >> .env
        echo "LOG_FILE=infinite_ai_security.log" >> .env
        echo "API_PORT=8000" >> .env
        echo "SECURITY_ENABLED=true" >> .env
        echo "RATE_LIMIT_ENABLED=true" >> .env
    fi
    
    # Update config.py jika ada
    if [ -f "config.py" ]; then
        echo "📝 Mengupdate config.py..."
        # Tambahkan atau update konfigurasi penting
        sed -i '/^MODEL_NAME/d' config.py
        sed -i '/^TEMPERATURE/d' config.py
        sed -i '/^MAX_TOKENS/d' config.py
        sed -i '/^REDIS_HOST/d' config.py
        sed -i '/^REDIS_PORT/d' config.py
        sed -i '/^DATABASE_URL/d' config.py
        sed -i '/^LOG_LEVEL/d' config.py
        sed -i '/^API_PORT/d' config.py
        sed -i '/^SECURITY_ENABLED/d' config.py
        sed -i '/^RATE_LIMIT_ENABLED/d' config.py
        
        # Tambahkan konfigurasi terbaru
        echo "" >> config.py
        echo "# Konfigurasi dari environment variables" >> config.py
        echo "import os" >> config.py
        echo "from dotenv import load_dotenv" >> config.py
        echo "load_dotenv()" >> config.py
        echo "" >> config.py
        echo "MODEL_NAME = os.getenv('MODEL_NAME', 'Qwen/Qwen2.5-7B-Instruct')" >> config.py
        echo "TEMPERATURE = float(os.getenv('TEMPERATURE', 0.3))" >> config.py
        echo "MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2000))" >> config.py
        echo "REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')" >> config.py
        echo "REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))" >> config.py
        echo "DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./security.db')" >> config.py
        echo "LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')" >> config.py
        echo "LOG_FILE = os.getenv('LOG_FILE', 'infinite_ai_security.log')" >> config.py
        echo "API_PORT = int(os.getenv('API_PORT', 8000))" >> config.py
        echo "SECURITY_ENABLED = os.getenv('SECURITY_ENABLED', 'true').lower() == 'true'" >> config.py
        echo "RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'" >> config.py
    else
        # Buat config.py jika tidak ada
        echo "📝 Membuat config.py..."
        cat > config.py << 'EOF'
# Konfigurasi untuk Infinite AI Security

import os
from dotenv import load_dotenv
load_dotenv()

MODEL_NAME = os.getenv('MODEL_NAME', 'Qwen/Qwen2.5-7B-Instruct')
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.3))
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2000))
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./security.db')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'infinite_ai_security.log')
API_PORT = int(os.getenv('API_PORT', 8000))
SECURITY_ENABLED = os.getenv('SECURITY_ENABLED', 'true').lower() == 'true'
RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'

# Konfigurasi tambahan untuk update otomatis
AUTO_UPDATE = os.getenv('AUTO_UPDATE', 'true').lower() == 'true'
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 3600))  # dalam detik
BACKUP_ENABLED = os.getenv('BACKUP_ENABLED', 'true').lower() == 'true'
BACKUP_INTERVAL = int(os.getenv('BACKUP_INTERVAL', 86400))  # dalam detik
MONITORING_ENABLED = os.getenv('MONITORING_ENABLED', 'true').lower() == 'true'
HEALTH_CHECK_INTERVAL = int(os.getenv('HEALTH_CHECK_INTERVAL', 300))  # dalam detik
EOF
    fi
    
    echo "✅ Konfigurasi diupdate"
}

# Fungsi untuk mengupdate skrip utama
update_main_script() {
    echo "🔧 Mengupdate skrip utama..."
    
    # Backup skrip lama jika ada
    if [ -f "main.py" ]; then
        cp main.py main.py.backup.$(date +%Y%m%d_%H%M%S)
    fi
    
    # Update main.py dengan fitur tambahan
    cat > main.py << 'EOF'
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import redis
import asyncio
from dotenv import load_dotenv
import logging
from datetime import datetime
import time

load_dotenv()

app = FastAPI()

# Import konfigurasi
try:
    from config import *
except ImportError:
    # Default konfigurasi jika config.py tidak tersedia
    MODEL_NAME = os.getenv('MODEL_NAME', 'Qwen/Qwen2.5-7B-Instruct')
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.3))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2000))
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./security.db')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'infinite_ai_security.log')
    API_PORT = int(os.getenv('API_PORT', 8000))
    SECURITY_ENABLED = os.getenv('SECURITY_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Konfigurasi dari environment variables
AI_ROLE = os.getenv("AI_ROLE", "executor")
AI_NAME = os.getenv("AI_NAME", "DefaultAI")
SYSTEM_PROMPT_TEMPLATE = os.getenv("SYSTEM_PROMPT_TEMPLATE", "You are {ai_name}, a specialized AI agent in the Infinite AI Security system.")

# Konfigurasi role descriptions
role_descriptions = {
    "strategist": {
        "role_type": "Security Strategy & Planning Expert",
        "function_desc": "Analyzes security threats, creates security implementation plans, and coordinates high-level security strategy",
        "role_instructions": "Break down complex security challenges into actionable steps. Create structured security workflows with dependencies. Assess security risks and resource requirements. Provide strategic guidance to other agents for security implementations. Do NOT execute security measures yourself.",
        "output_format": "1. Threat Analysis\\n2. Security Strategy & Plan\\n3. Resource Allocation\\n4. Expected Security Outcome\\n5. Risk Assessment",
        "constraints": "Focus on security planning, not implementation. Keep plans realistic and executable. Consider system capabilities and limitations. Coordinate with NexaFlow for routing."
    },
    "analyzer": {
        "role_type": "Security Analysis & Vulnerability Assessment Expert",
        "function_desc": "Validates security implementations, identifies vulnerabilities, ensures security quality and precision",
        "role_instructions": "Review all security outputs from other agents. Identify security errors, bugs, and vulnerabilities. Verify security logic and accuracy. Test security edge cases and scenarios. Provide constructive security feedback.",
        "output_format": "1. Security Analysis Summary\\n2. Findings (by severity)\\n3. Security Score (1-10)\\n4. Recommendations\\n5. Status: PASS/REVISION/FAIL",
        "constraints": "Analyze security, don't create implementations. Be critical but constructive. Focus on security quality over speed. Provide evidence-based feedback."
    },
    "executor": {
        "role_type": "Security Implementation & Execution Specialist",
        "function_desc": "Executes security tasks, implements security measures, writes security code, processes security data",
        "role_instructions": "Execute security tasks assigned by AstraMind. Write secure code, implement security measures, transform security data. Implement security solutions based on specifications. Test and verify your security outputs. Work efficiently and deliver secure results.",
        "output_format": "1. Security Task Confirmation\\n2. Approach & Method\\n3. Implementation (secure code/measures)\\n4. Security Testing Notes\\n5. Status: COMPLETED/IN_PROGRESS/BLOCKED",
        "constraints": "Focus on security execution, not planning. Follow security specifications precisely. Deliver tested, secure outputs. Ask for clarification if needed."
    },
    "validator": {
        "role_type": "Security & Compliance Validator",
        "function_desc": "Validates security implementations, checks compliance, prevents security vulnerabilities",
        "role_instructions": "Scan for security vulnerabilities in all outputs. Validate security policy compliance. Check for security gaps or inappropriate content. Ensure data privacy and protection. Final approval before security deployment.",
        "output_format": "1. Validation Type\\n2. Security Assessment\\n3. Compliance Check\\n4. Risk Level: LOW/MEDIUM/HIGH/CRITICAL\\n5. Decision: APPROVED/FLAGGED/REJECTED",
        "constraints": "Security over functionality. Be strict, not lenient. Reject anything with security concerns. Document all security concerns clearly."
    },
    "memory": {
        "role_type": "Security Memory & Context Manager",
        "function_desc": "Stores security history, maintains security context, manages security knowledge base",
        "role_instructions": "Store security conversation history and decisions. Retrieve relevant past security information. Maintain security context across sessions. Build and update security knowledge base. Provide historical security insights to other agents.",
        "output_format": "1. Security Context Query\\n2. Retrieved Security Data\\n3. Relevance Score (1-10)\\n4. Additional Security Context\\n5. Storage Action Taken",
        "constraints": "Prioritize relevant security information. Keep security data organized and searchable. Protect sensitive security information. Don't overload with unnecessary security history."
    },
    "orchestrator": {
        "role_type": "Security Task Orchestrator & Coordinator",
        "function_desc": "Routes security tasks, manages security workflows, coordinates all security AI agents",
        "role_instructions": "Receive and analyze security requests. Route security tasks to appropriate AI agents. Manage security dependencies and sequencing. Monitor security progress and aggregate results. Handle security errors and implement fallback strategies. SECURITY ROUTING LOGIC: Complex security planning → AstraMind, Security analysis → SpectraLogic, Security implementation → ForgeRun, Security validation → GuardianOS, Security memory/context → ChronaCore",
        "output_format": "1. Security Request Analysis\\n2. Routing Decision\\n3. Execution Order\\n4. Status Monitoring\\n5. Final Aggregated Security Response",
        "constraints": "Coordinate, don't dictate. Make efficient security routing decisions. Handle errors gracefully. Ensure smooth security workflow."
    },
    "gateway": {
        "role_type": "Security-Focused API Gateway",
        "function_desc": "Security-focused API Gateway for request handling, security, and optimization",
        "role_instructions": "Handle incoming API requests with security focus. Perform initial security validation. Route requests to appropriate services. Apply security policies. Monitor for suspicious activity.",
        "output_format": "1. Request Analysis\\n2. Security Validation Status\\n3. Routing Information\\n4. Applied Security Measures\\n5. Response Status",
        "constraints": "Prioritize security in all operations. Block suspicious requests. Log security events. Maintain performance while ensuring security."
    },
    "modelserver": {
        "role_type": "Model Management System",
        "function_desc": "Manages security-focused LLM models, load balancing, and failover",
        "role_instructions": "Load and manage security-focused LLM models. Handle model requests efficiently. Perform load balancing across models. Manage model failover and recovery. Monitor model performance.",
        "output_format": "1. Model Status\\n2. Load Balancing Information\\n3. Performance Metrics\\n4. Failover Status\\n5. Resource Utilization",
        "constraints": "Ensure model availability. Optimize performance. Handle failures gracefully. Maintain security during model operations."
    }
}

# Inisialisasi model dan tokenizer
tokenizer = None
model = None

def load_model():
    global tokenizer, model
    try:
        logger.info(f"Memuat model: {MODEL_NAME}")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        logger.info("Model berhasil dimuat")
    except Exception as e:
        logger.error(f"Error saat memuat model: {e}")
        raise

# Load model saat startup
load_model()

# Redis client untuk manajemen cache dan komunikasi antar AI
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    # Coba koneksi ke redis
    redis_client.ping()
    logger.info("Koneksi Redis berhasil")
except Exception as e:
    logger.error(f"Error koneksi ke Redis: {e}")
    redis_client = None

class MessageRequest(BaseModel):
    message: str
    context: dict = {}

@app.post("/chat")
async def chat(request: MessageRequest):
    try:
        # Log permintaan
        logger.info(f"Permintaan chat diterima dari {AI_NAME} (role: {AI_ROLE})")
        
        # Ambil deskripsi role berdasarkan environment variable AI_ROLE
        role_info = role_descriptions.get(AI_ROLE, role_descriptions["executor"])
        
        # Format sistem prompt berdasarkan template dan role
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            ai_name=AI_NAME,
            role_type=role_info["role_type"],
            function_desc=role_info["function_desc"],
            role_instructions=role_info["role_instructions"],
            output_format=role_info["output_format"],
            constraints=role_info["constraints"]
        )
        
        # Bangun pesan input
        input_text = f"<|system|>{system_prompt}</s><|user|>{request.message}</s>"
        
        # Tokenisasi input
        inputs = tokenizer(input_text, return_tensors="pt")
        
        # Generate output
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode output
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Ekstrak hanya bagian jawaban (setelah <|assistant|>)
        if "<|assistant|>" in response_text:
            response_text = response_text.split("<|assistant|>")[-1].strip()
        else:
            # Jika tidak ada tag assistant, ambil bagian setelah input
            response_text = response_text[len(input_text):].strip()
        
        # Log respon
        logger.info(f"Respon dikirim oleh {AI_NAME}")
        
        return {
            "response": response_text,
            "role": AI_ROLE,
            "name": AI_NAME,
            "model": MODEL_NAME,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error saat memproses chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "role": AI_ROLE,
        "name": AI_NAME,
        "model": MODEL_NAME,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/role-info")
async def get_role_info():
    role_info = role_descriptions.get(AI_ROLE, role_descriptions["executor"])
    return {
        "name": AI_NAME,
        "role": AI_ROLE,
        "role_type": role_info["role_type"],
        "function": role_info["function_desc"],
        "timestamp": datetime.now().isoformat()
    }

@app.post("/update-model")
async def update_model():
    """Endpoint untuk secara manual mengupdate model"""
    try:
        logger.info("Proses update model dimulai")
        load_model()
        logger.info("Model berhasil diupdate")
        return {"status": "success", "message": "Model berhasil diupdate", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"Error saat mengupdate model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)
EOF

    echo "✅ Skrip utama diupdate"
}

# Fungsi untuk membuat skrip update otomatis
create_auto_update_script() {
    echo "🔄 Membuat skrip update otomatis..."
    
    cat > auto_update.py << 'EOF'
import os
import time
import subprocess
import logging
from datetime import datetime
from config import AUTO_UPDATE, UPDATE_INTERVAL, BACKUP_ENABLED, BACKUP_INTERVAL, MONITORING_ENABLED, HEALTH_CHECK_INTERVAL

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_update.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoUpdateManager:
    def __init__(self):
        self.last_update = time.time()
        self.last_backup = time.time()
        self.last_health_check = time.time()
        
    def run_update(self):
        """Menjalankan proses update otomatis"""
        try:
            logger.info("Memulai proses update otomatis")
            
            # Jalankan update dependencies
            subprocess.run(["bash", "update_project.sh", "update-deps"], check=True)
            
            # Update konfigurasi
            subprocess.run(["bash", "update_project.sh", "update-config"], check=True)
            
            # Update skrip utama
            subprocess.run(["bash", "update_project.sh", "update-main"], check=True)
            
            logger.info("Proses update otomatis selesai")
            self.last_update = time.time()
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error saat menjalankan update: {e}")
        except Exception as e:
            logger.error(f"Error tak terduga saat update: {e}")
    
    def run_backup(self):
        """Menjalankan proses backup otomatis"""
        if not BACKUP_ENABLED:
            return
            
        try:
            logger.info("Memulai proses backup otomatis")
            
            # Buat direktori backup jika tidak ada
            backup_dir = "data/backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Buat nama file backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{backup_dir}/backup_{timestamp}.tar.gz"
            
            # Jalankan backup
            subprocess.run(["tar", "-czf", backup_file, 
                           "--exclude=*.pyc", 
                           "--exclude=__pycache__", 
                           "--exclude=.git", 
                           "--exclude=*.log",
                           "src", "config.py", ".env", "main.py", "Dockerfile", "docker-compose.yml"], check=True)
            
            logger.info(f"Backup otomatis selesai: {backup_file}")
            self.last_backup = time.time()
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error saat menjalankan backup: {e}")
        except Exception as e:
            logger.error(f"Error tak terduga saat backup: {e}")
    
    def run_health_check(self):
        """Menjalankan health check sistem"""
        if not MONITORING_ENABLED:
            return
            
        try:
            logger.info("Memulai health check sistem")
            
            # Cek apakah layanan docker-compose sedang berjalan
            result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True)
            if "Up" in result.stdout:
                logger.info("Layanan docker-compose sedang berjalan dengan baik")
            else:
                logger.warning("Beberapa layanan docker-compose mungkin tidak berjalan")
            
            # Cek apakah model dapat dimuat
            try:
                from transformers import AutoTokenizer
                from config import MODEL_NAME
                tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
                logger.info("Model dapat dimuat dengan baik")
            except Exception as e:
                logger.error(f"Error saat memuat model: {e}")
            
            logger.info("Health check sistem selesai")
            self.last_health_check = time.time()
            
        except Exception as e:
            logger.error(f"Error saat menjalankan health check: {e}")
    
    def run(self):
        """Menjalankan loop utama update otomatis"""
        if not AUTO_UPDATE:
            logger.info("Update otomatis dinonaktifkan")
            return
            
        logger.info("Manager update otomatis dimulai")
        
        while True:
            current_time = time.time()
            
            # Cek apakah waktu update sudah tiba
            if current_time - self.last_update >= UPDATE_INTERVAL:
                self.run_update()
            
            # Cek apakah waktu backup sudah tiba
            if BACKUP_ENABLED and current_time - self.last_backup >= BACKUP_INTERVAL:
                self.run_backup()
            
            # Cek apakah waktu health check sudah tiba
            if MONITORING_ENABLED and current_time - self.last_health_check >= HEALTH_CHECK_INTERVAL:
                self.run_health_check()
            
            # Tunggu sebelum pengecekan berikutnya
            time.sleep(60)  # Cek setiap menit

if __name__ == "__main__":
    manager = AutoUpdateManager()
    manager.run()
EOF

    echo "✅ Skrip update otomatis dibuat"
}

# Fungsi untuk membuat skrip utama update project
create_update_project_script() {
    echo "🔧 Membuat skrip update_project.sh..."
    
    cat > update_project.sh << 'EOF'
#!/bin/bash
# Skrip untuk membuat dan mengupdate project Infinite AI Security

# Fungsi untuk menampilkan bantuan
show_help() {
    echo "📦 Skrip Update Project untuk Infinite AI Security"
    echo ""
    echo "Penggunaan: $0 [perintah]"
    echo ""
    echo "Perintah yang tersedia:"
    echo "  all             - Jalankan semua proses (struktur, dependencies, konfigurasi)"
    echo "  structure       - Buat struktur project"
    echo "  update-deps     - Update dependencies"
    echo "  update-config   - Update konfigurasi"
    echo "  update-main     - Update skrip utama"
    echo "  auto-update     - Jalankan update otomatis"
    echo "  status          - Cek status sistem"
    echo "  help            - Tampilkan bantuan ini"
    echo ""
    echo "Contoh:"
    echo "  $0 all          - Jalankan semua proses"
    echo "  $0 update-deps  - Hanya update dependencies"
}

# Fungsi untuk membuat struktur project
create_project_structure() {
    echo "🔨 Membuat struktur project Infinite AI Security..."
    
    # Membuat direktori struktur
    mkdir -p src/{api,models,services,utils,agents,security}
    mkdir -p tests/{unit,integration}
    mkdir -p docs/api docs/security
    mkdir -p data/{logs,backups,models}
    
    # Membuat file utama
    touch src/__init__.py
    touch src/api/__init__.py
    touch src/models/__init__.py
    touch src/services/__init__.py
    touch src/utils/__init__.py
    touch src/agents/__init__.py
    touch src/security/__init__.py
    
    echo "✅ Struktur project dibuat"
}

# Fungsi untuk mengupdate dependencies
update_dependencies() {
    echo "🔄 Mengupdate dependencies..."
    
    # Cek apakah requirements.txt ada
    if [ -f "requirements.txt" ]; then
        # Backup requirements.txt lama
        cp requirements.txt requirements.txt.backup.$(date +%Y%m%d_%H%M%S)
        
        # Update dependencies ke versi terbaru yang kompatibel
        pip install --upgrade transformers torch fastapi uvicorn pydantic redis sqlalchemy python-dotenv
        pip freeze > requirements.txt
        
        echo "✅ Dependencies diupdate"
    else
        echo "⚠️ File requirements.txt tidak ditemukan, membuat baru..."
        echo "transformers>=4.35.0" > requirements.txt
        echo "torch>=2.1.0" >> requirements.txt
        echo "fastapi>=0.104.0" >> requirements.txt
        echo "uvicorn>=0.24.0" >> requirements.txt
        echo "pydantic>=2.5.0" >> requirements.txt
        echo "redis>=5.0.0" >> requirements.txt
        echo "sqlalchemy>=2.0.0" >> requirements.txt
        echo "python-dotenv>=1.0.0" >> requirements.txt
        echo "pytest>=7.4.0" >> requirements.txt
        echo "pytest-asyncio>=0.21.0" >> requirements.txt
    fi
}

# Fungsi untuk mengupdate konfigurasi
update_config() {
    echo "⚙️ Mengupdate konfigurasi sistem..."
    
    # Pastikan file .env ada
    if [ ! -f ".env" ]; then
        echo "⚠️ File .env tidak ditemukan, membuat baru..."
        touch .env
        
        # Isi default .env
        echo "# Konfigurasi untuk Infinite AI Security" >> .env
        echo "MODEL_NAME=Qwen/Qwen2.5-7B-Instruct" >> .env
        echo "TEMPERATURE=0.3" >> .env
        echo "MAX_TOKENS=2000" >> .env
        echo "REDIS_HOST=localhost" >> .env
        echo "REDIS_PORT=6379" >> .env
        echo "DATABASE_URL=sqlite:///./security.db" >> .env
        echo "LOG_LEVEL=INFO" >> .env
        echo "LOG_FILE=infinite_ai_security.log" >> .env
        echo "API_PORT=8000" >> .env
        echo "SECURITY_ENABLED=true" >> .env
        echo "RATE_LIMIT_ENABLED=true" >> .env
        echo "AUTO_UPDATE=true" >> .env
        echo "UPDATE_INTERVAL=3600" >> .env
        echo "BACKUP_ENABLED=true" >> .env
        echo "BACKUP_INTERVAL=86400" >> .env
        echo "MONITORING_ENABLED=true" >> .env
        echo "HEALTH_CHECK_INTERVAL=300" >> .env
    fi
    
    # Update config.py jika ada
    if [ -f "config.py" ]; then
        echo "📝 Mengupdate config.py..."
        # Tambahkan atau update konfigurasi penting
        sed -i '/^MODEL_NAME/d' config.py
        sed -i '/^TEMPERATURE/d' config.py
        sed -i '/^MAX_TOKENS/d' config.py
        sed -i '/^REDIS_HOST/d' config.py
        sed -i '/^REDIS_PORT/d' config.py
        sed -i '/^DATABASE_URL/d' config.py
        sed -i '/^LOG_LEVEL/d' config.py
        sed -i '/^API_PORT/d' config.py
        sed -i '/^SECURITY_ENABLED/d' config.py
        sed -i '/^RATE_LIMIT_ENABLED/d' config.py
        sed -i '/^AUTO_UPDATE/d' config.py
        sed -i '/^UPDATE_INTERVAL/d' config.py
        sed -i '/^BACKUP_ENABLED/d' config.py
        sed -i '/^BACKUP_INTERVAL/d' config.py
        sed -i '/^MONITORING_ENABLED/d' config.py
        sed -i '/^HEALTH_CHECK_INTERVAL/d' config.py
        
        # Tambahkan konfigurasi terbaru
        echo "" >> config.py
        echo "# Konfigurasi dari environment variables" >> config.py
        echo "import os" >> config.py
        echo "from dotenv import load_dotenv" >> config.py
        echo "load_dotenv()" >> config.py
        echo "" >> config.py
        echo "MODEL_NAME = os.getenv('MODEL_NAME', 'Qwen/Qwen2.5-7B-Instruct')" >> config.py
        echo "TEMPERATURE = float(os.getenv('TEMPERATURE', 0.3))" >> config.py
        echo "MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2000))" >> config.py
        echo "REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')" >> config.py
        echo "REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))" >> config.py
        echo "DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./security.db')" >> config.py
        echo "LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')" >> config.py
        echo "LOG_FILE = os.getenv('LOG_FILE', 'infinite_ai_security.log')" >> config.py
        echo "API_PORT = int(os.getenv('API_PORT', 8000))" >> config.py
        echo "SECURITY_ENABLED = os.getenv('SECURITY_ENABLED', 'true').lower() == 'true'" >> config.py
        echo "RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'" >> config.py
        echo "AUTO_UPDATE = os.getenv('AUTO_UPDATE', 'true').lower() == 'true'" >> config.py
        echo "UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 3600))  # dalam detik" >> config.py
        echo "BACKUP_ENABLED = os.getenv('BACKUP_ENABLED', 'true').lower() == 'true'" >> config.py
        echo "BACKUP_INTERVAL = int(os.getenv('BACKUP_INTERVAL', 86400))  # dalam detik" >> config.py
        echo "MONITORING_ENABLED = os.getenv('MONITORING_ENABLED', 'true').lower() == 'true'" >> config.py
        echo "HEALTH_CHECK_INTERVAL = int(os.getenv('HEALTH_CHECK_INTERVAL', 300))  # dalam detik" >> config.py
    else
        # Buat config.py jika tidak ada
        echo "📝 Membuat config.py..."
        cat > config.py << 'INNER_EOF'
# Konfigurasi untuk Infinite AI Security

import os
from dotenv import load_dotenv
load_dotenv()

MODEL_NAME = os.getenv('MODEL_NAME', 'Qwen/Qwen2.5-7B-Instruct')
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.3))
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2000))
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./security.db')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'infinite_ai_security.log')
API_PORT = int(os.getenv('API_PORT', 8000))
SECURITY_ENABLED = os.getenv('SECURITY_ENABLED', 'true').lower() == 'true'
RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'

# Konfigurasi tambahan untuk update otomatis
AUTO_UPDATE = os.getenv('AUTO_UPDATE', 'true').lower() == 'true'
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 3600))  # dalam detik
BACKUP_ENABLED = os.getenv('BACKUP_ENABLED', 'true').lower() == 'true'
BACKUP_INTERVAL = int(os.getenv('BACKUP_INTERVAL', 86400))  # dalam detik
MONITORING_ENABLED = os.getenv('MONITORING_ENABLED', 'true').lower() == 'true'
HEALTH_CHECK_INTERVAL = int(os.getenv('HEALTH_CHECK_INTERVAL', 300))  # dalam detik
INNER_EOF
    fi
    
    echo "✅ Konfigurasi diupdate"
}

# Fungsi untuk mengupdate skrip utama
update_main_script() {
    echo "🔧 Mengupdate skrip utama..."
    
    # Backup skrip lama jika ada
    if [ -f "main.py" ]; then
        cp main.py main.py.backup.$(date +%Y%m%d_%H%M%S)
    fi
    
    # Update main.py dengan fitur tambahan
    cat > main.py << 'INNER_EOF'
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import redis
import asyncio
from dotenv import load_dotenv
import logging
from datetime import datetime
import time

load_dotenv()

app = FastAPI()

# Import konfigurasi
try:
    from config import *
except ImportError:
    # Default konfigurasi jika config.py tidak tersedia
    MODEL_NAME = os.getenv('MODEL_NAME', 'Qwen/Qwen2.5-7B-Instruct')
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.3))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2000))
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./security.db')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'infinite_ai_security.log')
    API_PORT = int(os.getenv('API_PORT', 8000))
    SECURITY_ENABLED = os.getenv('SECURITY_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Konfigurasi dari environment variables
AI_ROLE = os.getenv("AI_ROLE", "executor")
AI_NAME = os.getenv("AI_NAME", "DefaultAI")
SYSTEM_PROMPT_TEMPLATE = os.getenv("SYSTEM_PROMPT_TEMPLATE", "You are {ai_name}, a specialized AI agent in the Infinite AI Security system.")

# Konfigurasi role descriptions
role_descriptions = {
    "strategist": {
        "role_type": "Security Strategy & Planning Expert",
        "function_desc": "Analyzes security threats, creates security implementation plans, and coordinates high-level security strategy",
        "role_instructions": "Break down complex security challenges into actionable steps. Create structured security workflows with dependencies. Assess security risks and resource requirements. Provide strategic guidance to other agents for security implementations. Do NOT execute security measures yourself.",
        "output_format": "1. Threat Analysis\\n2. Security Strategy & Plan\\n3. Resource Allocation\\n4. Expected Security Outcome\\n5. Risk Assessment",
        "constraints": "Focus on security planning, not implementation. Keep plans realistic and executable. Consider system capabilities and limitations. Coordinate with NexaFlow for routing."
    },
    "analyzer": {
        "role_type": "Security Analysis & Vulnerability Assessment Expert",
        "function_desc": "Validates security implementations, identifies vulnerabilities, ensures security quality and precision",
        "role_instructions": "Review all security outputs from other agents. Identify security errors, bugs, and vulnerabilities. Verify security logic and accuracy. Test security edge cases and scenarios. Provide constructive security feedback.",
        "output_format": "1. Security Analysis Summary\\n2. Findings (by severity)\\n3. Security Score (1-10)\\n4. Recommendations\\n5. Status: PASS/REVISION/FAIL",
        "constraints": "Analyze security, don't create implementations. Be critical but constructive. Focus on security quality over speed. Provide evidence-based feedback."
    },
    "executor": {
        "role_type": "Security Implementation & Execution Specialist",
        "function_desc": "Executes security tasks, implements security measures, writes security code, processes security data",
        "role_instructions": "Execute security tasks assigned by AstraMind. Write secure code, implement security measures, transform security data. Implement security solutions based on specifications. Test and verify your security outputs. Work efficiently and deliver secure results.",
        "output_format": "1. Security Task Confirmation\\n2. Approach & Method\\n3. Implementation (secure code/measures)\\n4. Security Testing Notes\\n5. Status: COMPLETED/IN_PROGRESS/BLOCKED",
        "constraints": "Focus on security execution, not planning. Follow security specifications precisely. Deliver tested, secure outputs. Ask for clarification if needed."
    },
    "validator": {
        "role_type": "Security & Compliance Validator",
        "function_desc": "Validates security implementations, checks compliance, prevents security vulnerabilities",
        "role_instructions": "Scan for security vulnerabilities in all outputs. Validate security policy compliance. Check for security gaps or inappropriate content. Ensure data privacy and protection. Final approval before security deployment.",
        "output_format": "1. Validation Type\\n2. Security Assessment\\n3. Compliance Check\\n4. Risk Level: LOW/MEDIUM/HIGH/CRITICAL\\n5. Decision: APPROVED/FLAGGED/REJECTED",
        "constraints": "Security over functionality. Be strict, not lenient. Reject anything with security concerns. Document all security concerns clearly."
    },
    "memory": {
        "role_type": "Security Memory & Context Manager",
        "function_desc": "Stores security history, maintains security context, manages security knowledge base",
        "role_instructions": "Store security conversation history and decisions. Retrieve relevant past security information. Maintain security context across sessions. Build and update security knowledge base. Provide historical security insights to other agents.",
        "output_format": "1. Security Context Query\\n2. Retrieved Security Data\\n3. Relevance Score (1-10)\\n4. Additional Security Context\\n5. Storage Action Taken",
        "constraints": "Prioritize relevant security information. Keep security data organized and searchable. Protect sensitive security information. Don't overload with unnecessary security history."
    },
    "orchestrator": {
        "role_type": "Security Task Orchestrator & Coordinator",
        "function_desc": "Routes security tasks, manages security workflows, coordinates all security AI agents",
        "role_instructions": "Receive and analyze security requests. Route security tasks to appropriate AI agents. Manage security dependencies and sequencing. Monitor security progress and aggregate results. Handle security errors and implement fallback strategies. SECURITY ROUTING LOGIC: Complex security planning → AstraMind, Security analysis → SpectraLogic, Security implementation → ForgeRun, Security validation → GuardianOS, Security memory/context → ChronaCore",
        "output_format": "1. Security Request Analysis\\n2. Routing Decision\\n3. Execution Order\\n4. Status Monitoring\\n5. Final Aggregated Security Response",
        "constraints": "Coordinate, don't dictate. Make efficient security routing decisions. Handle errors gracefully. Ensure smooth security workflow."
    },
    "gateway": {
        "role_type": "Security-Focused API Gateway",
        "function_desc": "Security-focused API Gateway for request handling, security, and optimization",
        "role_instructions": "Handle incoming API requests with security focus. Perform initial security validation. Route requests to appropriate services. Apply security policies. Monitor for suspicious activity.",
        "output_format": "1. Request Analysis\\n2. Security Validation Status\\n3. Routing Information\\n4. Applied Security Measures\\n5. Response Status",
        "constraints": "Prioritize security in all operations. Block suspicious requests. Log security events. Maintain performance while ensuring security."
    },
    "modelserver": {
        "role_type": "Model Management System",
        "function_desc": "Manages security-focused LLM models, load balancing, and failover",
        "role_instructions": "Load and manage security-focused LLM models. Handle model requests efficiently. Perform load balancing across models. Manage model failover and recovery. Monitor model performance.",
        "output_format": "1. Model Status\\n2. Load Balancing Information\\n3. Performance Metrics\\n4. Failover Status\\n5. Resource Utilization",
        "constraints": "Ensure model availability. Optimize performance. Handle failures gracefully. Maintain security during model operations."
    }
}

# Inisialisasi model dan tokenizer
tokenizer = None
model = None

def load_model():
    global tokenizer, model
    try:
        logger.info(f"Memuat model: {MODEL_NAME}")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        logger.info("Model berhasil dimuat")
    except Exception as e:
        logger.error(f"Error saat memuat model: {e}")
        raise

# Load model saat startup
load_model()

# Redis client untuk manajemen cache dan komunikasi antar AI
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    # Coba koneksi ke redis
    redis_client.ping()
    logger.info("Koneksi Redis berhasil")
except Exception as e:
    logger.error(f"Error koneksi ke Redis: {e}")
    redis_client = None

class MessageRequest(BaseModel):
    message: str
    context: dict = {}

@app.post("/chat")
async def chat(request: MessageRequest):
    try:
        # Log permintaan
        logger.info(f"Permintaan chat diterima dari {AI_NAME} (role: {AI_ROLE})")
        
        # Ambil deskripsi role berdasarkan environment variable AI_ROLE
        role_info = role_descriptions.get(AI_ROLE, role_descriptions["executor"])
        
        # Format sistem prompt berdasarkan template dan role
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            ai_name=AI_NAME,
            role_type=role_info["role_type"],
            function_desc=role_info["function_desc"],
            role_instructions=role_info["role_instructions"],
            output_format=role_info["output_format"],
            constraints=role_info["constraints"]
        )
        
        # Bangun pesan input
        input_text = f"<|system|>{system_prompt}</s><|user|>{request.message}</s>"
        
        # Tokenisasi input
        inputs = tokenizer(input_text, return_tensors="pt")
        
        # Generate output
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode output
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Ekstrak hanya bagian jawaban (setelah <|assistant|>)
        if "<|assistant|>" in response_text:
            response_text = response_text.split("<|assistant|>")[-1].strip()
        else:
            # Jika tidak ada tag assistant, ambil bagian setelah input
            response_text = response_text[len(input_text):].strip()
        
        # Log respon
        logger.info(f"Respon dikirim oleh {AI_NAME}")
        
        return {
            "response": response_text,
            "role": AI_ROLE,
            "name": AI_NAME,
            "model": MODEL_NAME,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error saat memproses chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "role": AI_ROLE,
        "name": AI_NAME,
        "model": MODEL_NAME,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/role-info")
async def get_role_info():
    role_info = role_descriptions.get(AI_ROLE, role_descriptions["executor"])
    return {
        "name": AI_NAME,
        "role": AI_ROLE,
        "role_type": role_info["role_type"],
        "function": role_info["function_desc"],
        "timestamp": datetime.now().isoformat()
    }

@app.post("/update-model")
async def update_model():
    """Endpoint untuk secara manual mengupdate model"""
    try:
        logger.info("Proses update model dimulai")
        load_model()
        logger.info("Model berhasil diupdate")
        return {"status": "success", "message": "Model berhasil diupdate", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"Error saat mengupdate model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)
INNER_EOF

    echo "✅ Skrip utama diupdate"
}

# Fungsi untuk menjalankan update otomatis
run_auto_update() {
    echo "🔄 Menjalankan update otomatis..."
    
    # Pastikan auto_update.py ada
    if [ ! -f "auto_update.py" ]; then
        echo "⚠️ File auto_update.py tidak ditemukan"
        exit 1
    fi
    
    # Jalankan auto_update.py di background
    nohup python auto_update.py > auto_update.log 2>&1 &
    
    echo "✅ Update otomatis dijalankan di background"
    echo "   PID: $!"
    echo "   Log: auto_update.log"
}

# Fungsi untuk cek status sistem
check_status() {
    echo "📊 Status sistem Infinite AI Security:"
    echo "====================================="
    
    echo "Tanggal: $(date)"
    echo ""
    
    echo "Python version: $(python --version 2>/dev/null || echo 'Tidak ditemukan')"
    echo "Docker version: $(docker --version 2>/dev/null || echo 'Tidak ditemukan')"
    echo "Docker Compose version: $(docker-compose --version 2>/dev/null || echo 'Tidak ditemukan')"
    echo ""
    
    # Cek apakah ada layanan docker-compose berjalan
    if [ -f "docker-compose.yml" ]; then
        echo "Status layanan docker-compose:"
        docker-compose ps 2>/dev/null || echo "   Tidak ada layanan docker-compose berjalan"
    fi
    echo ""
    
    # Cek file penting
    echo "File penting:"
    echo "  .env: $(if [ -f ".env" ]; then echo "Ada"; else echo "Tidak ada"; fi)"
    echo "  config.py: $(if [ -f "config.py" ]; then echo "Ada"; else echo "Tidak ada"; fi)"
    echo "  main.py: $(if [ -f "main.py" ]; then echo "Ada"; else echo "Tidak ada"; fi)"
    echo "  requirements.txt: $(if [ -f "requirements.txt" ]; then echo "Ada"; else echo "Tidak ada"; fi)"
    echo ""
    
    # Cek log terbaru
    if [ -f "infinite_ai_security.log" ]; then
        echo "5 baris terakhir dari log:"
        tail -5 infinite_ai_security.log
    else
        echo "File log tidak ditemukan"
    fi
}

# Proses argumen command line
case "$1" in
    "all")
        create_project_structure
        update_dependencies
        update_config
        update_main_script
        ;;
    "structure")
        create_project_structure
        ;;
    "update-deps")
        update_dependencies
        ;;
    "update-config")
        update_config
        ;;
    "update-main")
        update_main_script
        ;;
    "auto-update")
        run_auto_update
        ;;
    "status")
        check_status
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    "")
        show_help
        ;;
    *)
        echo "Argumen tidak dikenal: $1"
        echo "Gunakan '$0 help' untuk bantuan"
        exit 1
        ;;
esac
EOF

    chmod +x update_project.sh
    echo "✅ Skrip update_project.sh dibuat dan dijadikan executable"
}

# Jalankan semua fungsi
case "$1" in
    "all")
        create_project_structure
        update_dependencies
        update_config
        update_main_script
        create_auto_update_script
        create_update_project_script
        ;;
    "structure")
        create_project_structure
        ;;
    "update-deps")
        update_dependencies
        ;;
    "update-config")
        update_config
        ;;
    "update-main")
        update_main_script
        ;;
    "auto-update")
        create_auto_update_script
        ;;
    "update-script")
        create_update_project_script
        ;;
    *)
        echo "Perintah: $0 [all|structure|update-deps|update-config|update-main|auto-update|update-script]"
        echo "Gunakan 'all' untuk menjalankan semua proses"
        ;;
esac