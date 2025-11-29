#!/usr/bin/env python3
"""
Script sederhana untuk menguji model AI yang tersedia di Ollama
"""
import requests
import json

def test_ollama_model(port=11434):
    """Test model Qwen2.5:7b-instruct di Ollama"""
    url = f"http://localhost:{port}/api/generate"

    # Data untuk permintaan ke model
    data = {
        "model": "qwen2.5:7b-instruct",
        "prompt": "Hello, this is a test to check if the AI model is working properly. Please respond with a simple greeting and your model name.",
        "stream": False
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        result = response.json()
        print("✅ Model AI merespons dengan sukses!")
        print(f"📊 Model: {result['model']}")
        print(f"💬 Respon: {result['response']}")
        print(f"⏰ Durasi total: {result['total_duration']/1e9:.2f} detik")

        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error saat menghubungi Ollama di port {port}: {e}")
        return False
    except KeyError as e:
        print(f"❌ Error: Struktur respons tidak sesuai: {e}")
        return False

def list_models(port=11434):
    """Daftar model yang tersedia di Ollama"""
    url = f"http://localhost:{port}/api/tags"

    try:
        response = requests.get(url)
        response.raise_for_status()

        result = response.json()
        print(f"📦 Model-model yang tersedia di Ollama (port {port}):")
        for model in result["models"]:
            print(f"  - {model['name']} ({model['details']['parameter_size']})")

        return result["models"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Error saat mengambil daftar model dari port {port}: {e}")
        return []

def check_ports():
    """Cek port-port Ollama yang tersedia"""
    ports = [11434, 11436, 11437]
    available_ports = []

    for port in ports:
        try:
            response = requests.get(f"http://localhost:{port}/api/tags", timeout=5)
            if response.status_code == 200:
                available_ports.append(port)
                print(f"✅ Port {port} aktif")
        except:
            print(f"❌ Port {port} tidak merespons")

    return available_ports

if __name__ == "__main__":
    print("🧪 Testing AI Model - Qwen2.5:7b-instruct")
    print("="*50)

    # Cek port yang tersedia
    available_ports = check_ports()
    print()

    # Coba setiap port yang tersedia
    success = False
    for port in available_ports:
        print(f"\n🔍 Menguji model di port {port}:")
        models = list_models(port)
        print()

        if models:  # Jika ada model tersedia di port ini
            success = test_ollama_model(port)
            if success:
                break  # Berhenti jika berhasil

    if not success and available_ports:
        # Jika tidak berhasil di port mana pun yang ditemukan aktif, coba port 11436 karena ini yang terlihat dari docker ps
        print(f"\n🔍 Mencoba port 11436 sebagai fallback (berdasarkan output docker ps):")
        models = list_models(11436)
        if models:
            success = test_ollama_model(11436)

    if success:
        print("\n🎉 AI Model berfungsi dengan baik!")
    else:
        print("\n⚠️  Terdapat masalah dengan layanan AI.")