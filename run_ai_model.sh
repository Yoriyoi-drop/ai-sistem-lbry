#!/bin/bash
# Script untuk menjalankan model AI menggunakan Ollama
# File: run_ai_model.sh

echo "🚀 Starting AI Model Service (Qwen2.5:7b-instruct)"
echo "=================================================="

# Cek apakah Ollama berjalan
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama tidak merespons di port 11434"
    echo "💡 Memulai layanan Ollama..."
    cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security
    docker compose -f docker-compose.ollama.yml up -d
    sleep 10
fi

# Tampilkan model yang tersedia
echo "📦 Model yang tersedia:"
curl -s http://localhost:11434/api/tags | python3 -m json.tool | grep -E 'name|parameter_size'

echo ""
echo "💬 Menguji model Qwen2.5:7b-instruct:"
echo "Q: Hello, can you introduce yourself?"
echo "A: $(curl -s -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d '{"model": "qwen2.5:7b-instruct", "prompt": "Hello, can you introduce yourself briefly?", "stream": false}' --max-time 60 | python3 -c "import sys, json; print(json.load(sys.stdin)['response'])")"

echo ""
echo "🎯 AI Model siap digunakan!"
echo ""
echo "💡 Tips: Anda bisa menggunakan perintah berikut untuk berinteraksi dengan model:"
echo "   curl -X POST http://localhost:11434/api/generate -H 'Content-Type: application/json' \\"
echo "   -d '{\"model\": \"qwen2.5:7b-instruct\", \"prompt\": \"pesan Anda di sini\", \"stream\": false}'"
echo ""
echo "🌐 Atau buka antarmuka web di http://localhost:3001 untuk manajemen model"