"""
Sandbox Module for Security Engine
Provides isolated execution environment
"""
import subprocess
import tempfile
import os
import signal
import time
from typing import Dict, Any, Optional
import logging


class ExecutionSandbox:
    """
    Sandbox environment for safe code execution
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.allowed_languages = ["python", "javascript", "bash"]
        self.timeout_limit = 30  # Maximum allowed timeout in seconds
        self.max_memory_mb = 100  # Maximum allowed memory in MB

    def execute(self, code: str, language: str = "python", timeout: int = 5) -> Dict[str, Any]:
        """
        Execute code in a sandboxed environment
        """
        if language not in self.allowed_languages:
            return {
                "success": False,
                "error": f"Language '{language}' not supported",
                "output": "",
                "error_output": f"Language '{language}' not supported",
                "execution_time": 0
            }

        if timeout > self.timeout_limit:
            timeout = self.timeout_limit

        start_time = time.time()
        
        try:
            if language == "python":
                result = self._execute_python(code, timeout)
            elif language == "javascript":
                result = self._execute_javascript(code, timeout)
            elif language == "bash":
                result = self._execute_bash(code, timeout)
            else:
                return {
                    "success": False,
                    "error": f"Language '{language}' not implemented",
                    "output": "",
                    "error_output": f"Language '{language}' not implemented",
                    "execution_time": 0
                }

            execution_time = time.time() - start_time
            result["execution_time"] = round(execution_time, 3)

            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "error_output": str(e),
                "execution_time": round(execution_time, 3)
            }

    def _execute_python(self, code: str, timeout: int) -> Dict[str, Any]:
        """
        Execute Python code in a temporary file with timeout
        """
        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name

        try:
            # Execute the code with timeout
            result = subprocess.run(
                ["python3", temp_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                # Note: In a real implementation, you'd want more restrictions
                # like using a separate user, restricted system calls, etc.
            )
            
            success = result.returncode == 0
            
            return {
                "success": success,
                "output": result.stdout,
                "error_output": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timed out after {timeout} seconds",
                "output": "",
                "error_output": f"Execution timed out after {timeout} seconds",
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "error_output": str(e),
                "return_code": -1
            }
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_path)
            except:
                pass  # Ignore cleanup errors

    def _execute_javascript(self, code: str, timeout: int) -> Dict[str, Any]:
        """
        Execute JavaScript code using Node.js
        """
        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["node", temp_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            
            return {
                "success": success,
                "output": result.stdout,
                "error_output": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timed out after {timeout} seconds",
                "output": "",
                "error_output": f"Execution timed out after {timeout} seconds",
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "error_output": str(e),
                "return_code": -1
            }
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_path)
            except:
                pass

    def _execute_bash(self, code: str, timeout: int) -> Dict[str, Any]:
        """
        Execute bash script with restricted permissions
        """
        # For security, only allow safe commands
        # In a real implementation, you'd want to use a more secure approach
        dangerous_patterns = [
            "rm ", "rm -", "mv ", "cp ", "ln ", "chmod ", "chown ",
            "/dev/", "/proc/", "/sys/", ">/", ">>", "&&", "||", ";",
            "exec ", "eval ", "source ", ".", "import "
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern in code_lower:
                return {
                    "success": False,
                    "error": f"Potentially dangerous command detected: {pattern}",
                    "output": "",
                    "error_output": f"Potentially dangerous command detected: {pattern}",
                    "return_code": -1
                }

        try:
            result = subprocess.run(
                code,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            
            return {
                "success": success,
                "output": result.stdout,
                "error_output": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timed out after {timeout} seconds",
                "output": "",
                "error_output": f"Execution timed out after {timeout} seconds",
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "error_output": str(e),
                "return_code": -1
            }

    def check_safety(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Static analysis to check if code is safe for execution
        """
        issues = []
        
        if language == "python":
            # Check for dangerous imports
            dangerous_imports = [
                "os", "sys", "subprocess", "importlib", "imp", 
                "compile", "exec", "eval", "__import__"
            ]
            
            for imp in dangerous_imports:
                if f"import {imp}" in code or f"from {imp}" in code:
                    issues.append({
                        "type": "dangerous_import",
                        "import": imp,
                        "severity": "high"
                    })
        
        elif language == "bash":
            # Check for dangerous commands (as done in _execute_bash)
            dangerous_patterns = [
                "rm ", "mv ", "chmod ", "chown ", "/dev/", "/proc/", 
                "/sys/", "exec ", "eval ", ">/", ">>", "&&", "||", ";"
            ]
            
            code_lower = code.lower()
            for pattern in dangerous_patterns:
                if pattern in code_lower:
                    issues.append({
                        "type": "dangerous_command",
                        "command": pattern,
                        "severity": "high"
                    })
        
        return {
            "is_safe": len(issues) == 0,
            "issues": issues,
            "risk_level": "low" if len(issues) == 0 else 
                        "high" if any(i["severity"] == "high" for i in issues) else "medium"
        }