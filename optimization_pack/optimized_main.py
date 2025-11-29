"""
Optimized Main Application with Lazy Loading and Caching
This version implements all optimization strategies while maintaining full functionality
"""
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import asyncio
from dotenv import load_dotenv

# Import optimization utilities
from optimization_pack.lazy_loader import AILazyLoader
from optimization_pack.cache_manager import cache_manager, SecurityCache

# Load environment variables
load_dotenv()

# Initialize FastAPI app with optimized settings
app = FastAPI(
    title="Infinite AI Security Platform - Optimized",
    description="Enterprise AI Security Platform with optimized resource usage",
    version="0.1.0-optimized",
    # Reduce startup overhead
    openapi_url="/openapi.json" if os.getenv("API_DEBUG", "false").lower() == "true" else None
)

# Konfigurasi dari environment variables
AI_ROLE = os.getenv("AI_ROLE", "executor")
AI_NAME = os.getenv("AI_NAME", "DefaultAI")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen:7b-instruct")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 2000))
SYSTEM_PROMPT_TEMPLATE = os.getenv("SYSTEM_PROMPT_TEMPLATE", "You are {ai_name}, a specialized AI agent.")

# Role descriptions - cached for performance
role_descriptions = {
    "strategist": {
        "role_type": "Security Strategy & Planning Expert",
        "function_desc": "Analyzes security threats, creates security implementation plans, and coordinates high-level security strategy",
        "role_instructions": "Break down complex security challenges into actionable steps. Create structured security workflows with dependencies. Assess security risks and resource requirements. Provide strategic guidance to other agents for security implementations. Do NOT execute security measures yourself.",
        "output_format": "1. Threat Analysis\n2. Security Strategy & Plan\n3. Resource Allocation\n4. Expected Security Outcome\n5. Risk Assessment",
        "constraints": "Focus on security planning, not implementation. Keep plans realistic and executable. Consider system capabilities and limitations. Coordinate with NexaFlow for routing."
    },
    "analyzer": {
        "role_type": "Security Analysis & Vulnerability Assessment Expert",
        "function_desc": "Validates security implementations, identifies vulnerabilities, ensures security quality and precision",
        "role_instructions": "Review all security outputs from other agents. Identify security errors, bugs, and vulnerabilities. Verify security logic and accuracy. Test security edge cases and scenarios. Provide constructive security feedback.",
        "output_format": "1. Security Analysis Summary\n2. Findings (by severity)\n3. Security Score (1-10)\n4. Recommendations\n5. Status: PASS/REVISION/FAIL",
        "constraints": "Analyze security, don't create implementations. Be critical but constructive. Focus on security quality over speed. Provide evidence-based feedback."
    },
    "executor": {
        "role_type": "Security Implementation & Execution Specialist",
        "function_desc": "Executes security tasks, implements security measures, writes security code, processes security data",
        "role_instructions": "Execute security tasks assigned by AstraMind. Write secure code, implement security measures, transform security data. Implement security solutions based on specifications. Test and verify your security outputs. Work efficiently and deliver secure results.",
        "output_format": "1. Security Task Confirmation\n2. Approach & Method\n3. Implementation (secure code/measures)\n4. Security Testing Notes\n5. Status: COMPLETED/IN_PROGRESS/BLOCKED",
        "constraints": "Focus on security execution, not planning. Follow security specifications precisely. Deliver tested, secure outputs. Ask for clarification if needed."
    },
    "validator": {
        "role_type": "Security & Compliance Validator",
        "function_desc": "Validates security implementations, checks compliance, prevents security vulnerabilities",
        "role_instructions": "Scan for security vulnerabilities in all outputs. Validate security policy compliance. Check for security gaps or inappropriate content. Ensure data privacy and protection. Final approval before security deployment.",
        "output_format": "1. Validation Type\n2. Security Assessment\n3. Compliance Check\n4. Risk Level: LOW/MEDIUM/HIGH/CRITICAL\n5. Decision: APPROVED/FLAGGED/REJECTED",
        "constraints": "Security over functionality. Be strict, not lenient. Reject anything with security concerns. Document all security concerns clearly."
    },
    "memory": {
        "role_type": "Security Memory & Context Manager",
        "function_desc": "Stores security history, maintains security context, manages security knowledge base",
        "role_instructions": "Store security conversation history and decisions. Retrieve relevant past security information. Maintain security context across sessions. Build and update security knowledge base. Provide historical security insights to other agents.",
        "output_format": "1. Security Context Query\n2. Retrieved Security Data\n3. Relevance Score (1-10)\n4. Additional Security Context\n5. Storage Action Taken",
        "constraints": "Prioritize relevant security information. Keep security data organized and searchable. Protect sensitive security information. Don't overload with unnecessary security history."
    },
    "orchestrator": {
        "role_type": "Security Task Orchestrator & Coordinator",
        "function_desc": "Routes security tasks, manages security workflows, coordinates all security AI agents",
        "role_instructions": "Receive and analyze security requests. Route security tasks to appropriate AI agents. Manage security dependencies and sequencing. Monitor security progress and aggregate results. Handle security errors and implement fallback strategies. SECURITY ROUTING LOGIC: Complex security planning → AstraMind, Security analysis → SpectraLogic, Security implementation → ForgeRun, Security validation → GuardianOS, Security memory/context → ChronaCore",
        "output_format": "1. Security Request Analysis\n2. Routing Decision\n3. Execution Order\n4. Status Monitoring\n5. Final Aggregated Security Response",
        "constraints": "Coordinate, don't dictate. Make efficient security routing decisions. Handle errors gracefully. Ensure smooth security workflow."
    },
    "gateway": {
        "role_type": "Security-Focused API Gateway",
        "function_desc": "Security-focused API Gateway for request handling, security, and optimization",
        "role_instructions": "Handle incoming API requests with security focus. Perform initial security validation. Route requests to appropriate services. Apply security policies. Monitor for suspicious activity.",
        "output_format": "1. Request Analysis\n2. Security Validation Status\n3. Routing Information\n4. Applied Security Measures\n5. Response Status",
        "constraints": "Prioritize security in all operations. Block suspicious requests. Log security events. Maintain performance while ensuring security."
    },
    "modelserver": {
        "role_type": "Model Management System",
        "function_desc": "Manages security-focused LLM models, load balancing, and failover",
        "role_instructions": "Load and manage security-focused LLM models. Handle model requests efficiently. Perform load balancing across models. Manage model failover and recovery. Monitor model performance.",
        "output_format": "1. Model Status\n2. Load Balancing Information\n3. Performance Metrics\n4. Failover Status\n5. Resource Utilization",
        "constraints": "Ensure model availability. Optimize performance. Handle failures gracefully. Maintain security during model operations."
    }
}

# Lazy loading for Ollama client
def get_ollama_client():
    """Lazy load Ollama client only when needed"""
    return AILazyLoader.get_ollama_client()

def check_model_availability():
    """Check if the Ollama model is available with caching"""
    cache_key = f"model_availability_{MODEL_NAME}"
    cached_result = cache_manager.get(cache_key)
    
    if cached_result is not None:
        return cached_result
    
    try:
        # Lazy load the client when needed
        ollama = get_ollama_client()
        
        # Test connection to Ollama
        response = ollama.list()
        available_models = [m['name'] for m in response['models']]
        is_available = MODEL_NAME in available_models
        
        # Cache for 5 minutes
        cache_manager.set(cache_key, is_available, expire_seconds=300)
        
        if is_available:
            print(f"Model {MODEL_NAME} is available in Ollama")
        else:
            print(f"Model {MODEL_NAME} is not available in Ollama. Available models: {available_models}")
        
        return is_available
    except Exception as e:
        print(f"Error checking model availability: {e}")
        return False

# Check model availability at startup
if not check_model_availability():
    print(f"Warning: Model {MODEL_NAME} may not be available. Please run: ollama pull {MODEL_NAME}")

# Redis client for caching and communication with lazy initialization
class LazyRedisClient:
    """Redis client that connects only when needed"""
    def __init__(self):
        self._client = None
    
    def get_client(self):
        if self._client is None:
            self._client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'), 
                port=int(os.getenv('REDIS_PORT', 6379)), 
                db=int(os.getenv('REDIS_DB', 0)), 
                decode_responses=True
            )
        return self._client

redis_client = LazyRedisClient()
DATABASE_URL = os.getenv("DATABASE_URL", "")
REDIS_FEEDBACK_KEY = os.getenv("REDIS_FEEDBACK_KEY", "infinite:feedback")

class MessageRequest(BaseModel):
    message: str
    context: dict = {}


class FeedbackRequest(BaseModel):
    user_id: str | None = None
    message: str
    model_response: str | None = None
    corrected_response: str | None = None
    metadata: dict = {}

@cache_manager.cache_with_ttl(ttl_seconds=300)  # Cache chat responses for 5 minutes if similar
@app.post("/chat")
async def chat(request: MessageRequest):
    try:
        # Use cached role information
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

        # Create messages for Ollama
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ]

        # Lazy load and use Ollama client
        ollama = get_ollama_client()
        
        # Generate response using Ollama
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            options={
                "temperature": TEMPERATURE,
                "num_predict": MAX_TOKENS
            }
        )

        response_text = response['message']['content']

        return {
            "response": response_text,
            "role": AI_ROLE,
            "name": AI_NAME,
            "model": MODEL_NAME
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
async def feedback(fb: FeedbackRequest):
    """Collect user feedback / corrections for model outputs with optimized storage."""
    try:
        os.makedirs("data", exist_ok=True)
        record = {
            "ts": __import__("time").time(),
            "user_id": fb.user_id,
            "message": fb.message,
            "model_response": fb.model_response,
            "corrected_response": fb.corrected_response,
            "metadata": fb.metadata,
        }
        fname = os.path.join("data", "feedback.jsonl")
        with open(fname, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        # Push to Redis list for faster ingestion / pipeline processing
        try:
            redis_client.get_client().rpush(REDIS_FEEDBACK_KEY, json.dumps(record, ensure_ascii=False))
        except Exception:
            # Non-fatal: continue even if Redis is not available
            pass

        # If DATABASE_URL provided, attempt to insert into Postgres table `feedback`
        if DATABASE_URL:
            try:
                # Lazy import for database operations
                import psycopg2
                from psycopg2.extras import Json

                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                cur.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id serial PRIMARY KEY,
                    ts double precision,
                    user_id text,
                    message text,
                    model_response text,
                    corrected_response text,
                    metadata jsonb
                )""")
                cur.execute(
                    "INSERT INTO feedback (ts, user_id, message, model_response, corrected_response, metadata) VALUES (%s,%s,%s,%s,%s,%s)",
                    (record["ts"], record["user_id"], record["message"], record["model_response"], record["corrected_response"], Json(record["metadata"]))
                )
                conn.commit()
                cur.close()
                conn.close()
            except Exception:
                # Non-fatal: log or ignore
                pass

        return {"status": "ok", "written": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "role": AI_ROLE,
        "name": AI_NAME,
        "model": MODEL_NAME
    }

@app.get("/role-info")
async def get_role_info():
    role_info = role_descriptions.get(AI_ROLE, role_descriptions["executor"])
    return {
        "name": AI_NAME,
        "role": AI_ROLE,
        "role_type": role_info["role_type"],
        "function": role_info["function_desc"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=os.getenv("API_HOST", "0.0.0.0"), 
        port=int(os.getenv("API_PORT", 8000)),
        workers=int(os.getenv("API_WORKERS", 1)),
        log_level=os.getenv("LOG_LEVEL", "info")
    )