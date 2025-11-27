"""
Hugging Face Inference Client Service for Infinite AI Security Platform
"""
import os
from huggingface_hub import InferenceClient
from typing import Dict, Any, List
import asyncio
import logging
import json

logger = logging.getLogger(__name__)


class HuggingFaceSecurityInference:
    """
    Service untuk menggunakan Hugging Face Inference API untuk deteksi ancaman
    """
    
    def __init__(self):
        self.api_key = os.getenv("HF_TOKEN")
        if not self.api_key:
            raise ValueError("Environment variable HF_TOKEN harus diatur")
        
        self.client = InferenceClient(api_key=self.api_key)
        self.default_model = os.getenv("HF_SECURITY_MODEL", "microsoft/SecurityBert")
    
    async def analyze_threat(self, payload: str, source_ip: str = "127.0.0.1") -> Dict[str, Any]:
        """
        Analisis ancaman menggunakan Hugging Face Inference API
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
            
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {
                        "role": "user",
                        "content": security_prompt
                    }
                ],
                max_tokens=500,
                temperature=0.1,
            )
            
            response_text = response.choices[0].message.content.strip()
            
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
                "id": f"hf_threat_{abs(hash(payload))}",
                "timestamp": int(asyncio.get_event_loop().time()) if hasattr(asyncio.get_event_loop(), 'time') else 0,
                "source_ip": source_ip,
                "threat_type": result.get("threat_type", "Unknown"),
                "severity": result.get("severity", "Medium"),
                "payload": payload,
                "confidence": result.get("confidence", 0.5),
                "geolocation": None,
                "attack_vector": "Web",
                "mitigation_applied": False,
                "explanation": result.get("explanation", "Analysis completed by HF model"),
                "detected_patterns": result.get("detected_patterns", [])
            }
            
            logger.info(f"HF inference completed: {final_result.get('threat_type', 'Unknown threat')}")
            return final_result
            
        except Exception as e:
            logger.error(f"Error in HF threat analysis: {str(e)}")
            # Return fallback response jika inference gagal
            return {
                "id": f"hf_threat_{abs(hash(payload))}",
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
        Deteksi SQL injection khusus menggunakan Hugging Face Inference
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
            
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            response_text = response.choices[0].message.content.strip()
            
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
            logger.error(f"Error in HF SQL injection detection: {str(e)}")
            return {
                "is_malicious": False,
                "threat_level": "LOW",
                "confidence": 0.0,
                "detected_patterns": [],
                "explanation": f"Detection failed: {str(e)}",
                "query_sample": query
            }


# Global instance
hf_security_client = HuggingFaceSecurityInference()