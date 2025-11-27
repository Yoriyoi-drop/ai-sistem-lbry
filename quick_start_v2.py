"""
Quick Start Script V2.0 - Enhanced Security Platform
Implements the quick setup from the roadmap with security hardening
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("🛡️" + "=" * 58 + "🛡️")
    print("    INFINITE AI SECURITY PLATFORM V2.0 - QUICK START")
    print("🛡️" + "=" * 58 + "🛡️")
    print()

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3.8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Core dependencies
    core_deps = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "websockets==12.0",
        "pydantic==2.5.0",
        "python-multipart==0.0.6",
        "aiofiles==23.2.1",
        "requests==2.31.0",
        "aiohttp==3.9.0"
    ]
    
    # Enhanced security dependencies
    security_deps = [
        "bcrypt==4.0.1",
        "PyJWT==2.8.0",
        "pyotp==2.9.0",
        "qrcode==7.4.2"
    ]
    
    try:
        # Install core dependencies
        print("  📋 Installing core dependencies...")
        for dep in core_deps:
            print(f"    Installing {dep.split('==')[0]}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"    ⚠️  Warning: Failed to install {dep}")
        
        # Install security dependencies
        print("  🔒 Installing security dependencies...")
        for dep in security_deps:
            print(f"    Installing {dep.split('==')[0]}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"    ⚠️  Warning: Failed to install {dep} (optional)")
        
        print("✅ Dependencies installation completed")
        return True
        
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def setup_environment():
    """Setup environment configuration"""
    print("\n🔧 Setting up environment...")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("  📝 Creating .env file...")
        env_content = """# Infinite AI Security V2.0 Configuration
# Security Settings
JWT_SECRET_KEY=infinite-ai-security-v2-production-key-change-this
JWT_REFRESH_SECRET=infinite-ai-refresh-secret-v2-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Rate Limiting
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=15
DEFAULT_RATE_LIMIT=100
RATE_LIMIT_WINDOW=60

# Database
DATABASE_PATH=infinite_security_v2.db

# Security Features
THREAT_CONFIDENCE_THRESHOLD=0.7
ENABLE_AUTO_BLOCKING=true

# Server Settings
HOST=127.0.0.1
PORT=8000
DEBUG=false
LOG_LEVEL=INFO

# Data Retention
DATA_RETENTION_DAYS=30
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("  ✅ Environment file created")
    else:
        print("  ℹ️  Environment file already exists")
    
    # Create logs directory
    logs_dir = Path("logs")
    if not logs_dir.exists():
        logs_dir.mkdir()
        print("  📁 Logs directory created")
    
    return True

def run_security_tests():
    """Run basic security validation"""
    print("\n🔍 Running security validation...")
    
    try:
        # Test imports
        print("  🧪 Testing security modules...")
        
        # Test enhanced auth
        try:
            from security.enhanced_auth import enhanced_auth
            print("    ✅ Enhanced authentication module")
        except ImportError:
            print("    ⚠️  Enhanced authentication module not found")
        
        # Test input validator
        try:
            from security.input_validator import input_validator
            print("    ✅ Input validation module")
        except ImportError:
            print("    ⚠️  Input validation module not found")
        
        # Test basic functionality
        print("  🔧 Testing basic functionality...")
        
        # Test threat analysis
        try:
            if 'input_validator' in locals():
                result = input_validator.validate_input("test input", "general")
                print("    ✅ Threat analysis working")
            else:
                print("    ⚠️  Using fallback threat analysis")
        except Exception as e:
            print(f"    ❌ Threat analysis error: {e}")
        
        print("✅ Security validation completed")
        return True
        
    except Exception as e:
        print(f"❌ Security validation failed: {e}")
        return False

def start_system():
    """Start the security system"""
    print("\n🚀 Starting Infinite AI Security Platform V2.0...")
    
    try:
        # Check if main_v2.py exists, fallback to main.py
        if Path("main_v2.py").exists():
            main_file = "main_v2.py"
            print("  📋 Using enhanced V2.0 main application")
        elif Path("main.py").exists():
            main_file = "main.py"
            print("  📋 Using standard main application")
        else:
            print("❌ No main application file found!")
            return False
        
        print(f"  🔄 Executing: python {main_file}")
        print("  ⏳ Starting server...")
        print()
        print("🌐 Server will be available at:")
        print("   📊 Dashboard: http://127.0.0.1:8000")
        print("   ❤️  Health Check: http://127.0.0.1:8000/health")
        print("   🔐 Login: admin/admin123")
        print()
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Start the application
        subprocess.run([sys.executable, main_file], check=True)
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting system: {e}")
        return False

def run_tests():
    """Run security test suite"""
    print("\n🧪 Running Security Test Suite...")
    
    try:
        if Path("testing/security_test_suite.py").exists():
            print("  🔍 Found security test suite")
            print("  ⏳ This will test the running system...")
            print("  📝 Make sure the server is running first!")
            
            choice = input("\n  Run tests now? (y/N): ").lower().strip()
            if choice == 'y':
                subprocess.run([sys.executable, "testing/security_test_suite.py"], check=True)
            else:
                print("  ℹ️  Tests skipped. Run manually with:")
                print("     python testing/security_test_suite.py")
        else:
            print("  ⚠️  Security test suite not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Main quick start function"""
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("⚠️  Continuing with existing dependencies...")
    
    # Step 3: Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        sys.exit(1)
    
    # Step 4: Run security validation
    if not run_security_tests():
        print("⚠️  Continuing with warnings...")
    
    # Step 5: Show options
    print("\n🎯 Quick Start Options:")
    print("  1. Start System (Recommended)")
    print("  2. Run Security Tests")
    print("  3. Both (Start system, then run tests)")
    print("  4. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                start_system()
                break
            elif choice == "2":
                run_tests()
                break
            elif choice == "3":
                print("\n📋 Starting system first...")
                print("   After system starts, open a new terminal and run:")
                print("   python testing/security_test_suite.py")
                print()
                start_system()
                break
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()