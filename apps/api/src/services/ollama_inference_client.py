"""
Ollama Inference Client Service for Infinite AI Security Platform
"""
import os
from typing import Dict, Any, List
import asyncio
import logging
import json
import ollama

logger = logging.getLogger(__name__)


class OllamaSecurityInference:
    """
    Service untuk menggunakan Ollama untuk deteksi ancaman keamanan
    """

    def __init__(self):
        self.default_model = os.getenv("OLLAMA_SECURITY_MODEL", "qwen:7b-instruct")
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        
        # Test connection to Ollama
        try:
            ollama.Client(host=self.ollama_host).list()
            logger.info(f"Successfully connected to Ollama at {self.ollama_host}")
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            raise

    async def analyze_threat(self, payload: str, source_ip: str = "127.0.0.1") -> Dict[str, Any]:
        """
        Analisis ancaman menggunakan Ollama
        """
        try:
            # Format pesan untuk analisis keamanan
            security_prompt = f"""
            Sebagai model keamanan AI, analisis payload berikut untuk mendeteksi potensi ancaman keamanan:

            PAYLOAD: {payload}
            SOURCE IP: {source_ip}

            BERIKAN RESPON DALAM FORMAT JSON BERIKUT:
            {{
                "threat_type": "jenis ancaman (SQLInjection, XSS, CommandInjection, PathTraversal, dll)",
                "severity": "tingkat keparahan (Critical, High, Medium, Low)",
                "confidence": "tingkat kepercayaan (0.0-1.0)",
                "explanation": "penjelasan tentang mengapa dianggap berbahaya",
                "vulnerable": "true/false",
                "detected_patterns": ["array", "of", "detected", "patterns"]
            }}
            """

            response = ollama.chat(
                model=self.default_model,
                messages=[
                    {
                        "role": "user",
                        "content": security_prompt
                    }
                ],
                options={
                    "temperature": 0.1,
                    "num_predict": 500
                }
            )

            response_text = response['message']['content'].strip()

            # Bersihkan respons jika diperlukan
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Hapus ```json
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Hapus ```

            try:
                # Coba parsing JSON respons
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # Jika parsing gagal, buat respons default
                result = {
                    "threat_type": "Unknown",
                    "severity": "Medium",
                    "confidence": 0.5,
                    "explanation": response_text,
                    "vulnerable": "true" in response_text.lower(),
                    "detected_patterns": []
                }

            # Gabungkan dengan format ThreatIntel
            final_result = {
                "id": f"ollama_threat_{abs(hash(payload))}",
                "timestamp": int(asyncio.get_event_loop().time()) if hasattr(asyncio.get_event_loop(), 'time') else 0,
                "source_ip": source_ip,
                "threat_type": result.get("threat_type", "Unknown"),
                "severity": result.get("severity", "Medium"),
                "payload": payload,
                "confidence": result.get("confidence", 0.5),
                "geolocation": None,
                "attack_vector": "Web",
                "mitigation_applied": False,
                "explanation": result.get("explanation", "Analysis completed by Ollama model"),
                "detected_patterns": result.get("detected_patterns", [])
            }

            logger.info(f"Ollama inference completed: {final_result.get('threat_type', 'Unknown threat')}")
            return final_result

        except Exception as e:
            logger.error(f"Error in Ollama threat analysis: {str(e)}")
            # Return fallback response jika inference gagal
            return {
                "id": f"ollama_threat_{abs(hash(payload))}",
                "timestamp": 0,
                "source_ip": source_ip,
                "threat_type": "Unknown",
                "severity": "Medium",
                "payload": payload,
                "confidence": 0.0,
                "geolocation": None,
                "attack_vector": "Web",
                "mitigation_applied": False,
                "explanation": f"Analysis failed: {str(e)}",
                "detected_patterns": []
            }

    async def detect_sql_injection(self, query: str) -> Dict[str, Any]:
        """
        Deteksi SQL injection khusus menggunakan Ollama
        """
        try:
            prompt = f"""
            Analisis query SQL berikut untuk mendeteksi kemungkinan SQL injection:

            QUERY: {query}

            BERIKAN RESPON DALAM FORMAT JSON:
            {{
                "is_malicious": true/false,
                "threat_level": "CRITICAL/HIGH/MEDIUM/LOW",
                "confidence": 0.0-1.0,
                "detected_patterns": ["array", "of", "detected", "patterns"],
                "explanation": "penjelasan tentang temuan"
            }}
            """

            response = ollama.chat(
                model=self.default_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.1,
                    "num_predict": 500
                }
            )

            response_text = response['message']['content'].strip()

            # Bersihkan respons jika diperlukan
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Hapus ```json
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Hapus ```

            try:
                # Coba parsing JSON respons
                result = json.loads(response_text)
                # Gabungkan dengan format yang diharapkan oleh frontend
                formatted_result = {
                    "is_malicious": result.get("is_malicious", False),
                    "threat_level": result.get("threat_level", "LOW"),
                    "confidence": result.get("confidence", 0.0),
                    "detected_patterns": result.get("detected_patterns", []),
                    "explanation": result.get("explanation", "SQL injection analysis completed"),
                    "query_sample": query
                }
            except json.JSONDecodeError:
                # Jika parsing gagal, buat respons default
                formatted_result = {
                    "is_malicious": "true" in response_text.lower(),
                    "threat_level": "MEDIUM",
                    "confidence": 0.7,
                    "detected_patterns": [response_text[:50]],
                    "explanation": response_text,
                    "query_sample": query
                }

            return formatted_result

        except Exception as e:
            logger.error(f"Error in Ollama SQL injection detection: {str(e)}")
            return {
                "is_malicious": False,
                "threat_level": "LOW",
                "confidence": 0.0,
                "detected_patterns": [],
                "explanation": f"Detection failed: {str(e)}",
                "query_sample": query
            }


# Global instance
ollama_security_client = OllamaSecurityInference()