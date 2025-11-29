# 🤖 NEXAFORGE - PHASE 2: CORE AI INFRASTRUCTURE (L2-L3)

import os
import json
import subprocess
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AIModel:
    """Represents an AI model in the NexaForge system"""
    name: str
    size: str
    task_type: str
    description: str
    path: Optional[str] = None
    is_installed: bool = False

class ModelManager:
    """Manages AI models for L2: Model AI Layer"""
    
    def __init__(self, models_path: str = "~/nexaforge/models"):
        self.models_path = Path(models_path).expanduser()
        self.models_path.mkdir(parents=True, exist_ok=True)
        
        # Define the core AI models for Team A (L2)
        self.available_models: List[AIModel] = [
            AIModel("Qwen2.5-Coder-32B-Instruct", "32B", "coding", "Coding & Development"),
            AIModel("Qwen2.5-72B", "72B", "reasoning", "Reasoning & Analysis"),
            AIModel("Llama-3.1-70B-Instruct", "70B", "general", "General Assistant"),
            AIModel("DeepSeek-R1-70B-Distill", "70B", "logic", "Mathematical & Logical Reasoning"),
            AIModel("Phi-3.5-Vision", "12B", "vision", "Vision & OCR"),
            AIModel("Qwen-Audio", "7B", "audio", "Speech-to-text"),
            AIModel("Qwen2-VL", "72B", "multimodal", "Vision + Text"),
            AIModel("SmolAgent", "3B", "tools", "Tool Execution"),
            AIModel("Nous-Hermes-3", "70B", "creative", "Creative Writing"),
            AIModel("Gemma-2-27B", "27B", "efficient", "Efficient Inference"),
        ]
    
    def list_available_models(self) -> List[AIModel]:
        """List all available models"""
        return self.available_models
    
    def get_model_by_task(self, task_type: str) -> Optional[AIModel]:
        """Get the best model for a specific task type"""
        for model in self.available_models:
            if model.task_type == task_type:
                # For complex tasks, prefer larger models
                if task_type == "reasoning" and model.name == "Qwen2.5-72B":
                    return model
                elif task_type == "coding" and model.name == "Qwen2.5-Coder-32B-Instruct":
                    return model
                elif task_type == "general" and model.name == "Llama-3.1-70B-Instruct":
                    return model
                elif task_type == "vision" and model.name == "Phi-3.5-Vision":
                    return model
                elif task_type == "audio" and model.name == "Qwen-Audio":
                    return model
                elif task_type == "creative" and model.name == "Nous-Hermes-3":
                    return model
                elif task_type == "logic" and model.name == "DeepSeek-R1-70B-Distill":
                    return model
                elif task_type == "tools" and model.name == "SmolAgent":
                    return model
                elif task_type == "multimodal" and model.name == "Qwen2-VL":
                    return model
                elif task_type == "efficient" and model.name == "Gemma-2-27B":
                    return model
        return None

class AITaskRouter:
    """Handles AI task routing for L3: AI Task Routing Layer"""
    
    def __init__(self):
        self.model_manager = ModelManager()
        self.routing_history = []
    
    def route_task(self, task_description: str) -> Dict:
        """Route a task to the appropriate AI model"""
        # Determine task type based on keywords
        task_type = self._determine_task_type(task_description)
        
        # Get the best model for this task
        model = self.model_manager.get_model_by_task(task_type)
        
        if model:
            route_info = {
                "task": task_description,
                "task_type": task_type,
                "model": model.name,
                "model_size": model.size,
                "model_path": model.path or f"~/nexaforge/models/{model.name.lower().replace('-', '_')}",
                "is_available": model.is_installed
            }
        else:
            route_info = {
                "task": task_description,
                "task_type": task_type,
                "model": "default_model",
                "model_size": "unknown",
                "model_path": "~/nexaforge/models/default",
                "is_available": False
            }
        
        # Log routing decision
        self.routing_history.append(route_info)
        
        return route_info
    
    def _determine_task_type(self, task_description: str) -> str:
        """Determine the task type based on keywords in the description"""
        task_description_lower = task_description.lower()
        
        # Define keywords for each task type
        task_keywords = {
            "coding": ["code", "programming", "developer", "python", "javascript", "function", "class", "algorithm", "debug"],
            "reasoning": ["reason", "analyze", "think", "logic", "evaluate", "compare", "assess", "determine"],
            "general": ["help", "assistance", "question", "information", "explain", "describe", "summarize"],
            "vision": ["image", "picture", "photo", "visual", "ocr", "document", "scan", "recognize"],
            "audio": ["audio", "speech", "voice", "transcribe", "record", "sound"],
            "creative": ["write", "story", "poem", "creative", "narrative", "fiction", "lyrics", "art"],
            "logic": ["math", "calculate", "equation", "formula", "solve", "compute", "number", "algorithm", "proof"],
            "tools": ["execute", "run", "command", "tool", "utility", "operation", "automate", "script"],
            "multimodal": ["multimodal", "combined", "both", "text image", "visual text", "multi"],
            "efficient": ["quick", "fast", "simple", "light", "small", "minimal", "efficient"]
        }
        
        # Count keyword matches for each task type
        task_scores = {}
        for task_type, keywords in task_keywords.items():
            score = sum(1 for keyword in keywords if keyword in task_description_lower)
            task_scores[task_type] = score
        
        # Return the task type with the highest score
        best_task_type = max(task_scores, key=task_scores.get)
        return best_task_type if task_scores[best_task_type] > 0 else "general"
    
    def get_routing_stats(self) -> Dict:
        """Get statistics about routing decisions"""
        if not self.routing_history:
            return {"total_routed": 0}
        
        total_routed = len(self.routing_history)
        task_type_counts = {}
        model_counts = {}
        
        for route in self.routing_history:
            task_type = route["task_type"]
            model = route["model"]
            
            task_type_counts[task_type] = task_type_counts.get(task_type, 0) + 1
            model_counts[model] = model_counts.get(model, 0) + 1
        
        return {
            "total_routed": total_routed,
            "task_type_distribution": task_type_counts,
            "model_distribution": model_counts
        }

def main():
    """Demo of Phase 2 implementation"""
    print("🚀 NEXAFORGE - PHASE 2: CORE AI INFRASTRUCTURE (L2-L3)")
    print("=" * 60)
    
    # Initialize the AI Task Router
    router = AITaskRouter()
    
    # Show available models
    print("\n🤖 AVAILABLE AI MODELS (L2 Layer):")
    model_manager = ModelManager()
    models = model_manager.list_available_models()
    
    for model in models:
        print(f"  • {model.name} ({model.size}) - {model.description}")
    
    print(f"\n📋 Total models: {len(models)}")
    
    # Demo routing capabilities
    print("\n🔄 AI TASK ROUTING DEMO (L3 Layer):")
    demo_tasks = [
        "Write a Python function to calculate factorial",
        "Analyze this mathematical equation: x^2 + 2x + 1 = 0",
        "Help me understand quantum computing in simple terms",
        "Describe this image of a sunset landscape",
        "Convert this audio file to text",
        "Create a short creative story about a robot",
        "Solve this calculus problem: integral of x^2 dx",
        "Execute a shell command to list files in a directory",
        "Combine this text with that image to create a meme",
        "Provide a quick answer to what is the capital of France"
    ]
    
    for task in demo_tasks:
        route_info = router.route_task(task)
        print(f"  Task: {task[:50]}...")
        print(f"    → Type: {route_info['task_type']}")
        print(f"    → Model: {route_info['model']}")
        print(f"    → Available: {'Yes' if route_info['is_available'] else 'No'}")
        print()
    
    # Show routing statistics
    stats = router.get_routing_stats()
    print("📊 ROUTING STATISTICS:")
    print(f"  Total tasks routed: {stats['total_routed']}")
    print(f"  Task type distribution: {stats['task_type_distribution']}")
    print(f"  Model distribution: {stats['model_distribution']}")

if __name__ == "__main__":
    main()