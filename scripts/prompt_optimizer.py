#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt Optimization and Caching Script

This script optimizes prompts for AI image generation by:
1. Compressing long prompts while preserving key information
2. Caching optimized prompts for faster reuse
3. Adding language-specific enhancements
"""

import os
import re
import hashlib
import time
import json
from typing import List, Optional

class PromptOptimizer:
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Redundant phrases to remove
        self.redundant_phrases = [
            "please make sure",
            "ensure that",
            "it is important that",
            "you should",
            "you need to",
            "remember to",
            "make sure to",
            "be sure to",
            "please ensure",
            "please remember"
        ]
        
        # Language-specific enhancements
        self.language_enhancements = {
            "zh": {
                "text_rendering": "清晰渲染文字，确保无错别字",
                "layout": "保持良好的留白和可读性",
                "quality": "高质量产品图片，细节清晰"
            },
            "en": {
                "text_rendering": "Clear text rendering with no typos",
                "layout": "Good white space and readability",
                "quality": "High-quality product image with clear details"
            },
            "fr": {
                "text_rendering": "Rendu clair du texte sans fautes d'orthographe",
                "layout": "Bon espace blanc et lisibilité",
                "quality": "Image de produit de haute qualité avec des détails clairs"
            },
            "ja": {
                "text_rendering": "テキストを正確にレンダリングし、誤字なし",
                "layout": "適切な余白と読みやすさを確保",
                "quality": "高品質な製品画像で、詳細が明確"
            }
        }
    
    def generate_cache_key(self, prompt: str, images: List[str]) -> str:
        """Generate cache key based on prompt and images"""
        data = prompt + "|" + "|".join(sorted(images))
        return hashlib.md5(data.encode()).hexdigest()
    
    def get_cached_prompt(self, prompt: str, images: List[str]) -> Optional[str]:
        """Get cached prompt if available"""
        key = self.generate_cache_key(prompt, images)
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Check if cache is not too old (1 week)
                    if time.time() - data.get('timestamp', 0) < 604800:
                        return data.get('prompt')
            except Exception:
                pass
        return None
    
    def cache_prompt(self, prompt: str, images: List[str]) -> None:
        """Cache prompt for future use"""
        key = self.generate_cache_key(prompt, images)
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        
        data = {
            'prompt': prompt,
            'timestamp': time.time(),
            'images': images
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def compress_prompt(self, prompt: str, max_length: int = 1000) -> str:
        """Compress prompt while preserving key information"""
        if len(prompt) <= max_length:
            return prompt
        
        # Remove redundant phrases
        compressed = prompt
        for phrase in self.redundant_phrases:
            compressed = compressed.replace(phrase, "")
        
        # Remove extra spaces
        compressed = re.sub(r'\s+', ' ', compressed)
        
        # Truncate if still too long, preserving important parts
        if len(compressed) > max_length:
            # Keep the first part (context) and last part (specific instructions)
            # while removing some middle content
            first_part = compressed[:400]
            last_part = compressed[-600:]
            compressed = first_part + "... " + last_part
        
        return compressed
    
    def optimize_prompt(self, prompt: str, images: List[str], language: str = "en") -> str:
        """Optimize prompt with caching and compression"""
        # Check cache first
        cached = self.get_cached_prompt(prompt, images)
        if cached:
            return cached
        
        # Compress if needed
        optimized = self.compress_prompt(prompt)
        
        # Add language-specific enhancements
        if language in self.language_enhancements:
            enhancements = self.language_enhancements[language]
            # Add quality enhancement at the end
            if enhancements.get("quality"):
                optimized += f" {enhancements['quality']}"
        
        # Cache the result
        self.cache_prompt(optimized, images)
        
        return optimized
    
    def batch_optimize_prompts(self, prompts: List[str], images_list: List[List[str]], language: str = "en") -> List[str]:
        """Optimize multiple prompts in batch"""
        optimized_prompts = []
        
        for prompt, images in zip(prompts, images_list):
            optimized = self.optimize_prompt(prompt, images, language)
            optimized_prompts.append(optimized)
        
        return optimized_prompts
    
    def clear_cache(self) -> int:
        """Clear all cached prompts"""
        count = 0
        try:
            for file in os.listdir(self.cache_dir):
                if file.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, file))
                    count += 1
        except Exception:
            pass
        return count

def main():
    """Main function for testing"""
    optimizer = PromptOptimizer()
    
    # Test prompt compression
    long_prompt = """Please make sure to generate a high-quality product image for a Stainless Steel Tumbler. The tumbler should be placed on a clean white background. Ensure that the product is well-lit and all details are clearly visible. Remember to include the brand logo on the tumbler. Be sure to render the text 'Keeps drinks cold for 24 hours' clearly with no typos."""
    
    print("Prompt optimization test:")
    print(f"Original prompt length: {len(long_prompt)}")
    
    optimized = optimizer.optimize_prompt(long_prompt, ["image1.jpg"])
    print(f"Optimized prompt length: {len(optimized)}")
    print(f"Optimized prompt: {optimized}")
    
    # Test caching
    cached = optimizer.get_cached_prompt(long_prompt, ["image1.jpg"])
    print(f"\nCached prompt matches optimized: {cached == optimized}")
    
    # Test batch optimization
    test_prompts = [
        "Generate a product image for a ceramic mug",
        "Create an image of a wooden desk organizer"
    ]
    test_images = [
        ["mug_ref.jpg"],
        ["organizer_ref.jpg"]
    ]
    
    batch_optimized = optimizer.batch_optimize_prompts(test_prompts, test_images)
    print("\nBatch optimization results:")
    for i, (original, optimized) in enumerate(zip(test_prompts, batch_optimized)):
        print(f"Prompt {i+1}:")
        print(f"  Original: {original}")
        print(f"  Optimized: {optimized}")
    
    # Test cache clearing
    cleared = optimizer.clear_cache()
    print(f"\nCleared {cleared} cached prompts")

if __name__ == "__main__":
    main()