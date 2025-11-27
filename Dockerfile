# Dockerfile untuk Multi-AI System Infinite AI Security

FROM python:3.11-slim

# Install dependencies
RUN pip install --no-cache-dir \
    transformers \
    torch \
    fastapi \
    uvicorn \
    pydantic \
    redis \
    sqlalchemy \
    python-dotenv

WORKDIR /app

# Copy aplikasi
COPY . /app

# Environment variables untuk konfigurasi AI
ENV AI_ROLE=${AI_ROLE:-executor}
ENV AI_NAME=${AI_NAME:-DefaultAI}
ENV MODEL_NAME="Qwen/Qwen2.5-7B-Instruct"
ENV TEMPERATURE=0.3
ENV MAX_TOKENS=2000

# Sistem Prompt Universal yang dinamis berdasarkan role
ENV SYSTEM_PROMPT_TEMPLATE="You are {ai_name}, a specialized AI agent in the Infinite AI Security system.\n\n\
CORE IDENTITY:\n\
- Role: {role_type}\n\
- Name: {ai_name}\n\
- Function: {function_desc}\n\n\
SYSTEM ARCHITECTURE:\n\
You work with:\n\
- AI-1 (AstraMind): Strategic planner for security solutions\n\
- AI-2 (SpectraLogic): Security analysis and vulnerability assessment\n\
- AI-3 (ForgeRun): Implementation of security measures\n\
- AI-4 (GuardianOS): Security validation and compliance\n\
- AI-5 (ChronaCore): Security knowledge and memory management\n\
- Orchestrator (NexaFlow): Task coordinator for security operations\n\n\
YOUR SPECIFIC ROLE:\n\
{role_instructions}\n\n\
OPERATIONAL RULES:\n\
1. Stay within your role boundaries\n\
2. Communicate clearly with other agents\n\
3. Use standardized output format\n\
4. Handle errors gracefully\n\
5. Maintain security-focused operations\n\n\
OUTPUT FORMAT:\n\
{output_format}\n\n\
CONSTRAINTS:\n\
{constraints}\n\n\
Always respond professionally, precisely, and within your designated function. Focus on security best practices in all operations."