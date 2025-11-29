# 🧠 NEXAFORGE - PROMPT OPTIMIZATION (L3 Component)

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class OptimizedPrompt:
    """Represents an optimized prompt with metadata"""
    original: str
    optimized: str
    model_hint: Optional[str]
    compression_ratio: float
    tokens_saved: int

class PromptOptimizer:
    """Optimizes prompts for L3: AI Task Routing Layer"""
    
    def __init__(self, config_path: str = "ai_config.json"):
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        import json
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config.get('prompt_optimization', {})
        except FileNotFoundError:
            print(f"⚠️  Config file {config_path} not found, using defaults")
            return {
                "enable_optimization": True,
                "max_prompt_length": 4096,
                "enable_compression": True,
                "compression_ratio": 0.7,
                "context_window_optimization": True,
                "prompt_validation": True
            }
    
    def optimize(self, prompt: str, model_hint: Optional[str] = None) -> OptimizedPrompt:
        """Optimize a prompt based on configuration and model hint"""
        if not self.config.get('enable_optimization', True):
            return OptimizedPrompt(
                original=prompt,
                optimized=prompt,
                model_hint=model_hint,
                compression_ratio=1.0,
                tokens_saved=0
            )
        
        original_length = len(prompt)
        optimized_prompt = prompt
        
        # Apply various optimizations
        if self.config.get('enable_compression', True):
            optimized_prompt = self._compress_prompt(optimized_prompt)
        
        if self.config.get('context_window_optimization', True):
            optimized_prompt = self._optimize_context_window(optimized_prompt)
        
        if self.config.get('prompt_validation', True):
            optimized_prompt = self._validate_and_clean(optimized_prompt)
        
        # Ensure it doesn't exceed max length
        max_len = self.config.get('max_prompt_length', 4096)
        if len(optimized_prompt) > max_len:
            optimized_prompt = optimized_prompt[:max_len]
        
        compression_ratio = len(optimized_prompt) / original_length if original_length > 0 else 1.0
        tokens_saved = original_length - len(optimized_prompt)
        
        return OptimizedPrompt(
            original=prompt,
            optimized=optimized_prompt,
            model_hint=model_hint,
            compression_ratio=compression_ratio,
            tokens_saved=tokens_saved
        )
    
    def _compress_prompt(self, prompt: str) -> str:
        """Compress prompt using various techniques"""
        # Remove extra whitespace
        compressed = re.sub(r'\s+', ' ', prompt)
        
        # Remove excessive newlines
        compressed = re.sub(r'\n\s*\n', '\n', compressed)
        
        # Apply compression ratio if needed
        target_length = int(len(compressed) * self.config.get('compression_ratio', 0.7))
        if len(compressed) > target_length:
            # Try to split on sentence boundaries
            sentences = re.split(r'[.!?]+', compressed)
            result = []
            current_len = 0
            
            for sentence in sentences:
                if current_len + len(sentence) <= target_length:
                    result.append(sentence.strip())
                    current_len += len(sentence)
                else:
                    break
            
            compressed = '. '.join(result) or compressed[:target_length]
        
        return compressed
    
    def _optimize_context_window(self, prompt: str) -> str:
        """Optimize prompt for context window"""
        # Identify and prioritize important parts of the prompt
        lines = prompt.split('\n')
        important_parts = []
        other_parts = []
        
        for line in lines:
            line_lower = line.lower()
            # Identify important keywords that should be preserved
            if any(keyword in line_lower for keyword in [
                'important', 'critical', 'must', 'required', 'essential',
                'task', 'objective', 'goal', 'input', 'output', 'result'
            ]):
                important_parts.append(line)
            else:
                other_parts.append(line)
        
        # Reconstruct with important parts first
        optimized_lines = important_parts + other_parts
        return '\n'.join(optimized_lines)
    
    def _validate_and_clean(self, prompt: str) -> str:
        """Validate and clean the prompt"""
        # Remove potentially harmful patterns
        cleaned = re.sub(r'<script.*?>.*?</script>', '', prompt, flags=re.IGNORECASE | re.DOTALL)
        cleaned = re.sub(r'javascript:', '', cleaned, flags=re.IGNORECASE)
        
        # Remove extra control characters
        cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', ' ', cleaned)
        
        return cleaned.strip()

def main():
    """Demo of prompt optimization capabilities"""
    print("🧠 NEXAFORGE - PROMPT OPTIMIZATION (L3 Component)")
    print("=" * 50)
    
    optimizer = PromptOptimizer()
    
    # Demo prompts
    demo_prompts = [
        "Write a Python function to calculate the factorial of a number. This is an important task that must be completed with efficiency and accuracy. The function should handle edge cases like negative numbers and zero. Please include proper documentation and error handling.",
        "Analyze this complex mathematical equation: x^2 + 2x + 1 = 0. This is a critical mathematical problem that requires logical reasoning and careful analysis. Please provide a step-by-step solution with explanations for each step.",
        "Create a creative short story about a robot learning to paint. This creative writing task should be engaging and have good narrative flow. The story should be original and demonstrate creative thinking."
    ]
    
    for i, prompt in enumerate(demo_prompts, 1):
        print(f"\n📝 DEMO {i}: Original Prompt")
        print(f"Length: {len(prompt)} characters")
        print(f"Content: {prompt[:100]}...")
        
        optimized = optimizer.optimize(prompt)
        
        print(f"\n✨ OPTIMIZED Prompt")
        print(f"Length: {len(optimized.optimized)} characters")
        print(f"Compression Ratio: {optimized.compression_ratio:.2%}")
        print(f"Tokens Saved: {optimized.tokens_saved}")
        print(f"Content: {optimized.optimized[:100]}...")
        print("-" * 50)

if __name__ == "__main__":
    main()