"""
Test script to verify SQL Injection Detection is working
"""
import asyncio
import requests
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from asm.sql_injection_detector import detect_sql_injection


def test_sql_detector():
    print("🧪 Testing SQL Injection Detector...")
    print("="*50)
    
    test_cases = [
        {
            "query": "SELECT * FROM users WHERE id = 1",
            "expected_malicious": False,
            "description": "Safe query"
        },
        {
            "query": "SELECT * FROM users WHERE id = 1 OR 1=1",
            "expected_malicious": True,
            "description": "Classic SQL injection"
        },
        {
            "query": "SELECT * FROM users WHERE name = 'admin' -- comment",
            "expected_malicious": True,
            "description": "Comment-based injection"
        },
        {
            "query": "SELECT * FROM users WHERE name = 'admin' UNION SELECT password FROM admin_table",
            "expected_malicious": True,
            "description": "Union-based injection"
        },
        {
            "query": "SELECT * FROM users WHERE id = '1' OR '1'='1'",
            "expected_malicious": True,
            "description": "Boolean-based injection"
        },
        {
            "query": "SELECT * FROM products WHERE category = 'electronics'",
            "expected_malicious": False,
            "description": "Safe query with normal input"
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        result = detect_sql_injection(test_case["query"])
        
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Query: {test_case['query']}")
        print(f"Detected as malicious: {result['is_malicious']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Threat Level: {result['threat_level']}")
        print(f"Patterns: {result['detected_patterns']}")
        
        if result['is_malicious'] == test_case['expected_malicious']:
            print("✅ PASSED")
            passed += 1
        else:
            print("❌ FAILED")
    
    print("\n" + "="*50)
    print(f"Test Results: {passed}/{total} passed")
    accuracy = (passed / total) * 100
    print(f"Accuracy: {accuracy:.1f}%")
    
    return passed == total


def test_api():
    print("\n🌐 Testing API (make sure main_sql_detector.py is running on port 8000)")
    print("="*50)
    
    try:
        # Test the health endpoint
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            print("✅ API Health Check: OK")
        else:
            print(f"❌ API Health Check: Failed (Status: {response.status_code})")
            return False
            
        # Test the SQL injection detection endpoint
        test_query = "SELECT * FROM users WHERE id = 1 OR 1=1"
        response = requests.post(
            "http://127.0.0.1:8000/sql-injection/detect",
            json={"query": test_query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Detection Test: OK")
            print(f"   Malicious: {result['is_malicious']}")
            print(f"   Confidence: {result['confidence']}")
            print(f"   Threat Level: {result['threat_level']}")
            return True
        else:
            print(f"❌ API Detection Test: Failed (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ API Test: Connection failed - is the server running on port 8000?")
        print("   To start the server: python main_sql_detector.py")
        return False


if __name__ == "__main__":
    print("🚀 Starting SQL Injection Detection Tests")
    print("="*60)
    
    # Test the core logic
    logic_passed = test_sql_detector()
    
    # Test the API
    api_passed = test_api()
    
    print("\n" + "="*60)
    print("🎯 FINAL RESULTS:")
    print(f"   Core Logic: {'✅ PASS' if logic_passed else '❌ FAIL'}")
    print(f"   API Test: {'✅ PASS' if api_passed else '❌ FAIL'}")
    
    if logic_passed and api_passed:
        print("\n🎉 All tests passed! SQL Injection Detection is working correctly.")
        print("You can now integrate this with your React frontend.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
        
    print("="*60)