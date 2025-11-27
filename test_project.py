#!/usr/bin/env python3
"""
Comprehensive Project Testing Script
Tests all components of the Infinite AI Security Platform
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ProjectTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.results = {
            "passed": [],
            "failed": [],
            "warnings": [],
            "skipped": []
        }
        
    def print_header(self, text: str):
        """Print formatted header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")
        
    def print_test(self, name: str, status: str, message: str = ""):
        """Print test result"""
        if status == "PASS":
            color = Colors.OKGREEN
            self.results["passed"].append(name)
        elif status == "FAIL":
            color = Colors.FAIL
            self.results["failed"].append(name)
        elif status == "WARN":
            color = Colors.WARNING
            self.results["warnings"].append(name)
        else:  # SKIP
            color = Colors.OKCYAN
            self.results["skipped"].append(name)
            
        status_text = f"[{status}]"
        print(f"{color}{status_text:8}{Colors.ENDC} {name}")
        if message:
            print(f"         {Colors.BOLD}→{Colors.ENDC} {message}")
    
    def run_command(self, cmd: str, cwd: Path = None) -> Tuple[int, str, str]:
        """Run shell command and return exit code, stdout, stderr"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timeout"
        except Exception as e:
            return -1, "", str(e)
    
    def test_project_structure(self):
        """Test if essential project files and directories exist"""
        self.print_header("1. PROJECT STRUCTURE")
        
        essential_paths = {
            "Root files": [
                "README.md",
                "requirements.txt",
                "docker-compose.yml",
                ".env.example"
            ],
            "Services": [
                "services/api-gateway",
                "services/ai-hub",
                "services/scanner-go",
                "services/labyrinth-rust"
            ],
            "Frontend": [
                "dashboard-react",
                "frontend"
            ],
            "Configuration": [
                "alembic",
                "alembic.ini"
            ]
        }
        
        for category, paths in essential_paths.items():
            print(f"\n{Colors.BOLD}{category}:{Colors.ENDC}")
            for path in paths:
                full_path = self.project_root / path
                if full_path.exists():
                    self.print_test(path, "PASS", f"Found at {full_path}")
                else:
                    self.print_test(path, "WARN", f"Not found at {full_path}")
    
    def test_python_environment(self):
        """Test Python environment and dependencies"""
        self.print_header("2. PYTHON ENVIRONMENT")
        
        # Check Python version
        code, stdout, stderr = self.run_command("python3 --version")
        if code == 0:
            version = stdout.strip()
            self.print_test("Python Version", "PASS", version)
        else:
            self.print_test("Python Version", "FAIL", "Python3 not found")
            return
        
        # Check virtual environment
        venv_paths = [".venv", "venv"]
        venv_found = False
        for venv in venv_paths:
            if (self.project_root / venv).exists():
                self.print_test(f"Virtual Environment ({venv})", "PASS", "Found")
                venv_found = True
                break
        
        if not venv_found:
            self.print_test("Virtual Environment", "WARN", "No venv found")
        
        # Check key dependencies
        dependencies = [
            "fastapi",
            "uvicorn",
            "sqlalchemy",
            "alembic",
            "redis",
            "pytest"
        ]
        
        print(f"\n{Colors.BOLD}Key Dependencies:{Colors.ENDC}")
        code, stdout, stderr = self.run_command("pip3 list")
        if code == 0:
            installed = stdout.lower()
            for dep in dependencies:
                if dep.lower() in installed:
                    self.print_test(dep, "PASS", "Installed")
                else:
                    self.print_test(dep, "WARN", "Not installed")
        else:
            self.print_test("Dependencies Check", "FAIL", "Cannot check pip list")
    
    def test_backend_syntax(self):
        """Test backend Python files for syntax errors"""
        self.print_header("3. BACKEND SYNTAX CHECK")
        
        api_gateway = self.project_root / "services" / "api-gateway"
        if not api_gateway.exists():
            self.print_test("API Gateway", "SKIP", "Directory not found")
            return
        
        # Find all Python files
        python_files = list(api_gateway.rglob("*.py"))
        
        print(f"Found {len(python_files)} Python files\n")
        
        errors = []
        for py_file in python_files[:10]:  # Test first 10 files
            code, stdout, stderr = self.run_command(f"python3 -m py_compile {py_file}")
            relative_path = py_file.relative_to(self.project_root)
            
            if code == 0:
                self.print_test(str(relative_path), "PASS")
            else:
                self.print_test(str(relative_path), "FAIL", stderr[:100])
                errors.append(str(relative_path))
        
        if len(python_files) > 10:
            self.print_test(f"... and {len(python_files) - 10} more files", "SKIP", "Not checked")
    
    def test_frontend_structure(self):
        """Test frontend structure and dependencies"""
        self.print_header("4. FRONTEND STRUCTURE")
        
        frontend_paths = [
            self.project_root / "dashboard-react",
            self.project_root / "frontend"
        ]
        
        for frontend_path in frontend_paths:
            if not frontend_path.exists():
                self.print_test(str(frontend_path.name), "SKIP", "Directory not found")
                continue
            
            print(f"\n{Colors.BOLD}Checking {frontend_path.name}:{Colors.ENDC}")
            
            # Check package.json
            package_json = frontend_path / "package.json"
            if package_json.exists():
                self.print_test("package.json", "PASS", "Found")
                
                # Check if node_modules exists
                node_modules = frontend_path / "node_modules"
                if node_modules.exists():
                    self.print_test("node_modules", "PASS", "Dependencies installed")
                else:
                    self.print_test("node_modules", "WARN", "Run npm install")
            else:
                self.print_test("package.json", "FAIL", "Not found")
            
            # Check for main files
            main_files = ["src/App.js", "src/App.jsx", "index.html"]
            for file in main_files:
                if (frontend_path / file).exists():
                    self.print_test(file, "PASS", "Found")
                    break
            else:
                self.print_test("Main App File", "WARN", "No App.js/jsx found")
    
    def test_database_config(self):
        """Test database configuration"""
        self.print_header("5. DATABASE CONFIGURATION")
        
        # Check alembic
        alembic_ini = self.project_root / "alembic.ini"
        if alembic_ini.exists():
            self.print_test("alembic.ini", "PASS", "Found")
        else:
            self.print_test("alembic.ini", "WARN", "Not found")
        
        alembic_dir = self.project_root / "alembic"
        if alembic_dir.exists():
            self.print_test("alembic/", "PASS", "Found")
            
            # Check for migrations
            versions = alembic_dir / "versions"
            if versions.exists():
                migrations = list(versions.glob("*.py"))
                if migrations:
                    self.print_test("Migrations", "PASS", f"Found {len(migrations)} migration(s)")
                else:
                    self.print_test("Migrations", "WARN", "No migrations found")
        else:
            self.print_test("alembic/", "WARN", "Not found")
        
        # Check for database files
        db_files = list(self.project_root.glob("*.db"))
        if db_files:
            self.print_test("SQLite Databases", "PASS", f"Found {len(db_files)} database(s)")
        else:
            self.print_test("SQLite Databases", "WARN", "No .db files found")
    
    def test_docker_config(self):
        """Test Docker configuration"""
        self.print_header("6. DOCKER CONFIGURATION")
        
        # Check docker-compose files
        docker_files = [
            "docker-compose.yml",
            "docker-compose.production.yml",
            "Dockerfile",
            "Dockerfile.production"
        ]
        
        for file in docker_files:
            path = self.project_root / file
            if path.exists():
                self.print_test(file, "PASS", "Found")
            else:
                self.print_test(file, "WARN", "Not found")
        
        # Check if Docker is installed
        code, stdout, stderr = self.run_command("docker --version")
        if code == 0:
            self.print_test("Docker", "PASS", stdout.strip())
        else:
            self.print_test("Docker", "WARN", "Docker not installed or not in PATH")
        
        # Check if Docker Compose is installed
        code, stdout, stderr = self.run_command("docker compose version")
        if code == 0:
            self.print_test("Docker Compose", "PASS", stdout.strip())
        else:
            self.print_test("Docker Compose", "WARN", "Docker Compose not installed")
    
    def test_environment_config(self):
        """Test environment configuration"""
        self.print_header("7. ENVIRONMENT CONFIGURATION")
        
        env_files = [".env", ".env.example", ".env.production"]
        
        for env_file in env_files:
            path = self.project_root / env_file
            if path.exists():
                self.print_test(env_file, "PASS", "Found")
                
                # Check if it has content
                content = path.read_text()
                lines = [l for l in content.split('\n') if l.strip() and not l.startswith('#')]
                if lines:
                    self.print_test(f"  └─ Variables", "PASS", f"{len(lines)} variables defined")
            else:
                if env_file == ".env":
                    self.print_test(env_file, "WARN", "Not found - copy from .env.example")
                else:
                    self.print_test(env_file, "WARN", "Not found")
    
    def test_api_imports(self):
        """Test if main API file can be imported"""
        self.print_header("8. API IMPORT TEST")
        
        api_main = self.project_root / "services" / "api-gateway" / "app" / "main.py"
        
        if not api_main.exists():
            self.print_test("API Main", "SKIP", "File not found")
            return
        
        # Try to check imports
        code, stdout, stderr = self.run_command(
            f"python3 -c 'import sys; sys.path.insert(0, \"services/api-gateway\"); from app import main'",
            cwd=self.project_root
        )
        
        if code == 0:
            self.print_test("API Main Import", "PASS", "Successfully imported")
        else:
            error_msg = stderr.split('\n')[0] if stderr else "Unknown error"
            self.print_test("API Main Import", "FAIL", error_msg)
    
    def test_frontend_build(self):
        """Test if frontend can be built"""
        self.print_header("9. FRONTEND BUILD TEST")
        
        frontend_path = self.project_root / "dashboard-react"
        
        if not frontend_path.exists():
            self.print_test("Frontend Build", "SKIP", "dashboard-react not found")
            return
        
        package_json = frontend_path / "package.json"
        if not package_json.exists():
            self.print_test("Frontend Build", "SKIP", "package.json not found")
            return
        
        # Check if node_modules exists
        node_modules = frontend_path / "node_modules"
        if not node_modules.exists():
            self.print_test("Frontend Build", "WARN", "Run 'npm install' first")
            return
        
        # Try to run build (with timeout)
        print("Running npm build (this may take a while)...")
        code, stdout, stderr = self.run_command("npm run build", cwd=frontend_path)
        
        if code == 0:
            self.print_test("Frontend Build", "PASS", "Build successful")
        else:
            error_lines = stderr.split('\n')[:3]
            self.print_test("Frontend Build", "FAIL", " | ".join(error_lines))
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("TEST SUMMARY")
        
        total = sum(len(v) for v in self.results.values())
        
        print(f"{Colors.OKGREEN}✓ PASSED:  {len(self.results['passed']):3d}{Colors.ENDC}")
        print(f"{Colors.FAIL}✗ FAILED:  {len(self.results['failed']):3d}{Colors.ENDC}")
        print(f"{Colors.WARNING}⚠ WARNINGS:{len(self.results['warnings']):3d}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}○ SKIPPED: {len(self.results['skipped']):3d}{Colors.ENDC}")
        print(f"{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}")
        print(f"{Colors.BOLD}  TOTAL:   {total:3d}{Colors.ENDC}\n")
        
        # Overall status
        if len(self.results['failed']) == 0:
            if len(self.results['warnings']) == 0:
                print(f"{Colors.OKGREEN}{Colors.BOLD}🎉 ALL TESTS PASSED!{Colors.ENDC}\n")
            else:
                print(f"{Colors.WARNING}{Colors.BOLD}⚠️  TESTS PASSED WITH WARNINGS{Colors.ENDC}\n")
        else:
            print(f"{Colors.FAIL}{Colors.BOLD}❌ SOME TESTS FAILED{Colors.ENDC}\n")
        
        # Recommendations
        if self.results['warnings'] or self.results['failed']:
            print(f"{Colors.BOLD}RECOMMENDATIONS:{Colors.ENDC}\n")
            
            if "Virtual Environment" in self.results['warnings']:
                print("  • Create a virtual environment: python3 -m venv .venv")
            
            if any("not installed" in str(w).lower() for w in self.results['warnings']):
                print("  • Install Python dependencies: pip install -r requirements.txt")
            
            if "node_modules" in str(self.results['warnings']):
                print("  • Install frontend dependencies: cd dashboard-react && npm install")
            
            if ".env" in str(self.results['warnings']):
                print("  • Create .env file: cp .env.example .env")
            
            print()
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}")
        print("╔════════════════════════════════════════════════════════════════════════════╗")
        print("║                   INFINITE AI SECURITY PLATFORM                            ║")
        print("║                      COMPREHENSIVE TEST SUITE                              ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}\n")
        
        try:
            self.test_project_structure()
            self.test_python_environment()
            self.test_backend_syntax()
            self.test_frontend_structure()
            self.test_database_config()
            self.test_docker_config()
            self.test_environment_config()
            self.test_api_imports()
            # self.test_frontend_build()  # Skip build test as it takes time
            
            self.print_summary()
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.WARNING}Test interrupted by user{Colors.ENDC}\n")
            sys.exit(1)
        except Exception as e:
            print(f"\n\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}\n")
            import traceback
            traceback.print_exc()
            sys.exit(1)

def main():
    tester = ProjectTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
