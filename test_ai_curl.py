#!/usr/bin/env python3
"""
Script untuk menguji model AI menggunakan curl dari dalam Python
"""
import subprocess
import json
import sys

def test_ollama_with_curl():
    """Test model Qwen2.5:7b-instruct di Ollama menggunakan curl"""
    
    # Perintah curl untuk mengecek model yang tersedia
    print("🔍 Mengecek model-model yang tersedia...")
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:11434/api/tags'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            models_data = json.loads(result.stdout)
            print("📦 Model-model yang tersedia di Ollama (port 11434):")
            for model in models_data["models"]:
                print(f"  - {model['name']} ({model['details']['parameter_size']})")
            
            # Sekarang coba generate respon
            print("\n💬 Menguji kemampuan model...")
            curl_data = {
                "model": "qwen2.5:7b-instruct",
                "prompt": "Hello, this is a test to check if the AI model is working properly. Please respond with a simple greeting and your model name.",
                "stream": False
            }
            
            curl_cmd = [
                'curl',
                '-X', 'POST',
                'http://localhost:11434/api/generate',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps(curl_data)
            ]
            
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                response_data = json.loads(result.stdout)
                print("✅ Model AI merespons dengan sukses!")
                print(f"📊 Model: {response_data['model']}")
                print(f"💬 Respon: {response_data['response']}")
                print(f"⏰ Durasi total: {response_data['total_duration']/1e9:.2f} detik")
                return True
            else:
                print(f"❌ Error saat menggenerate respon: {result.stderr}")
                return False
        else:
            print(f"❌ Error saat mengambil daftar model: {result.stderr}")
            # Coba port lain
            for port in [11436, 11437]:
                print(f"\n🔍 Mencoba port alternatif: {port}")
                result = subprocess.run(['curl', '-s', f'http://localhost:{port}/api/tags'], 
                                       capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    try:
                        models_data = json.loads(result.stdout)
                        print(f"📦 Model-model yang tersedia di Ollama (port {port}):")
                        for model in models_data["models"]:
                            print(f"  - {model['name']} ({model['details']['parameter_size']})")
                        
                        # Coba generate dengan port ini
                        curl_data = {
                            "model": "qwen2.5:7b-instruct",
                            "prompt": "Hello, this is a test to check if the AI model is working properly. Please respond with a simple greeting and your model name.",
                            "stream": False
                        }
                        
                        curl_cmd = [
                            'curl',
                            '-X', 'POST',
                            f'http://localhost:{port}/api/generate',
                            '-H', 'Content-Type: application/json',
                            '-d', json.dumps(curl_data)
                        ]
                        
                        gen_result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
                        if gen_result.returncode == 0:
                            response_data = json.loads(gen_result.stdout)
                            print("✅ Model AI merespons dengan sukses!")
                            print(f"📊 Model: {response_data['model']}")
                            print(f"💬 Respon: {response_data['response']}")
                            print(f"⏰ Durasi total: {response_data['total_duration']/1e9:.2f} detik")
                            return True
                        else:
                            print(f"❌ Error saat menggenerate respon di port {port}: {gen_result.stderr}")
                    except json.JSONDecodeError:
                        print(f"❌ Respon dari port {port} bukan JSON yang valid")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Timeout saat mengakses API Ollama")
        return False
    except json.JSONDecodeError:
        print("❌ Respon dari API Ollama bukan JSON yang valid")
        return False
    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing AI Model - Qwen2.5:7b-instruct (menggunakan curl)")
    print("="*60)
    
    success = test_ollama_with_curl()
    
    if success:
        print("\n🎉 AI Model berfungsi dengan baik!")
    else:
        print("\n⚠️  Terdapat masalah dengan layanan AI.")
        print("💡 Pastikan layanan Ollama berjalan dan model telah diunduh.")