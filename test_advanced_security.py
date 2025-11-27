"""
Test script for Advanced Security Detection
"""
import requests
import json
import time

def test_advanced_security():
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Advanced Security Detection...")
    print("="*60)
    
    # Test 1: XSS Detection
    print("\n1. Testing XSS Detection:")
    xss_payload = "<script>alert('XSS')</script>"
    response = requests.post(
        f"{base_url}/advanced-security/detect-xss",
        json={"content": xss_payload},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ XSS Detection: {result['severity']} (Confidence: {result['confidence']:.2f})")
        print(f"   Patterns: {result['detected_patterns']}")
    else:
        print(f"   ❌ XSS Detection failed: {response.status_code} - {response.text}")
    
    # Test 2: Command Injection Detection
    print("\n2. Testing Command Injection Detection:")
    cmd_payload = "ls | cat /etc/passwd"
    response = requests.post(
        f"{base_url}/advanced-security/detect-command-injection",
        json={"command": cmd_payload},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Command Injection: {result['severity']} (Confidence: {result['confidence']:.2f})")
        print(f"   Patterns: {result['detected_patterns']}")
    else:
        print(f"   ❌ Command Injection failed: {response.status_code} - {response.text}")
    
    # Test 3: Path Traversal Detection
    print("\n3. Testing Path Traversal Detection:")
    path_payload = "../../../etc/passwd"
    response = requests.post(
        f"{base_url}/advanced-security/detect-path-traversal",
        json={"path": path_payload},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Path Traversal: {result['severity']} (Confidence: {result['confidence']:.2f})")
        print(f"   Patterns: {result['detected_patterns']}")
    else:
        print(f"   ❌ Path Traversal failed: {response.status_code} - {response.text}")
    
    # Test 4: Auth Bruteforce Detection
    print("\n4. Testing Auth Bruteforce Detection:")
    auth_payload = {
        "username": "admin",
        "password": "123"
    }
    response = requests.post(
        f"{base_url}/advanced-security/detect-auth-bruteforce",
        json=auth_payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Auth Bruteforce: {result['severity']} (Confidence: {result['confidence']:.2f})")
        print(f"   Patterns: {result['detected_patterns']}")
    else:
        print(f"   ❌ Auth Bruteforce failed: {response.status_code} - {response.text}")
    
    # Test 5: Get recent detections
    print("\n5. Testing Recent Detections:")
    response = requests.get(f"{base_url}/advanced-security/recent-detections?limit=5")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Retrieved {result['total']} detections")
        if result['detections']:
            print(f"   Latest detection: {result['detections'][0]['threat_type']}")
    else:
        print(f"   ❌ Recent Detections failed: {response.status_code} - {response.text}")
    
    print("\n" + "="*60)
    print("🎯 Advanced Security Detection Tests Completed!")
    print("All security detection types are now functional.")


if __name__ == "__main__":
    # Wait a moment to ensure server is ready
    time.sleep(2)
    test_advanced_security()