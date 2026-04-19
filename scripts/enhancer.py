#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amazon Product Image Generator with Enhanced Features

This script provides enhanced functionality for the amazon-product-image-wan27 skill,
including multi-language support, style mapping, and performance optimizations.
"""

import os
import sys
import json
import re
import hashlib
import time
from typing import Dict, List, Optional, Any

class AmazonProductImageEnhancer:
    def __init__(self):
        self.skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.scripts_dir = os.path.dirname(os.path.abspath(__file__))
        self.cache_dir = os.path.join(self.skill_dir, "cache")
        self.style_mappings = self._load_style_mappings()
        self.language_templates = self._load_language_templates()
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _load_style_mappings(self) -> Dict[str, Dict[str, str]]:
        """Load style mappings for different languages"""
        mappings = {
            "zh": {
                "极简现代": "minimal_modern",
                "日系柔和": "japanese_soft",
                "奢华编辑": "luxury_editorial",
                "圆润大粗体": "rounded_bold",
                "雅黑light": "yahoma_light",
                "现代简洁": "minimal_modern",
                "手写风格": "japanese_soft",
                "高端杂志": "luxury_editorial",
                "可爱友好": "rounded_bold",
                "纤细轻量": "yahoma_light"
            },
            "fr": {
                "moderne minimal": "minimal_modern",
                "japonais doux": "japanese_soft",
                "luxueux éditorial": "luxury_editorial",
                "épais arrondi": "rounded_bold",
                "yahei léger": "yahoma_light"
            },
            "ja": {
                "ミニマルモダン": "minimal_modern",
                "日本の柔らかさ": "japanese_soft",
                "高級エディトリアル": "luxury_editorial",
                "まるっと太字": "rounded_bold",
                "ヤハオライト": "yahoma_light"
            }
        }
        return mappings
    
    def _load_language_templates(self) -> Dict[str, Dict[str, str]]:
        """Load language-specific prompt templates"""
        templates = {
            "zh": {
                "text_rendering": "清晰渲染文字 '{text}'，确保无错别字，字体风格为 {typography}",
                "layout": "文字位于{position}，保持良好的留白和可读性"
            },
            "en": {
                "text_rendering": "Clear rendering of text '{text}' with no typos, typography style: {typography}",
                "layout": "Text positioned at {position} with good white space and readability"
            },
            "fr": {
                "text_rendering": "Rendu clair du texte '{text}' sans fautes d'orthographe, style typographique : {typography}",
                "layout": "Texte positionné à {position} avec bon espace blanc et lisibilité"
            },
            "ja": {
                "text_rendering": "テキスト '{text}' を正確にレンダリングし、誤字なし、タイポグラフィスタイル: {typography}",
                "layout": "テキストを{position}に配置し、適切な余白と読みやすさを確保"
            }
        }
        return templates
    
    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        # Simple language detection based on character sets
        if re.search(r'[\u4e00-\u9fff]', text):  # Chinese characters
            return "zh"
        elif re.search(r'[\u3040-\u30ff]', text):  # Japanese characters
            return "ja"
        elif re.search(r'[éèêëàâäôöùûüÿç]', text, re.IGNORECASE):  # French accented characters
            return "fr"
        else:
            return "en"
    
    def map_style(self, style: str, language: str = "en") -> str:
        """Map style from different languages to English style profile"""
        if language in self.style_mappings and style in self.style_mappings[language]:
            return self.style_mappings[language][style]
        return style  # Return original if no mapping found
    
    def compress_prompt(self, prompt: str, max_length: int = 1000) -> str:
        """Compress prompt while preserving key information"""
        if len(prompt) <= max_length:
            return prompt
        
        # Remove redundant phrases
        redundant_phrases = [
            "please make sure", "ensure that", "it is important that",
            "you should", "you need to", "remember to",
            "make sure to", "be sure to", "please ensure"
        ]
        
        compressed = prompt
        for phrase in redundant_phrases:
            compressed = compressed.replace(phrase, "")
        
        # Remove extra spaces
        compressed = re.sub(r'\s+', ' ', compressed)
        
        # Truncate if still too long, preserving the end which often contains important details
        if len(compressed) > max_length:
            # Keep the first 300 characters and the last 700 characters
            compressed = compressed[:300] + "... " + compressed[-700:]
        
        return compressed
    
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
    
    def generate_optimized_prompt(self, base_prompt: str, images: List[str], language: str = "en") -> str:
        """Generate optimized prompt with caching and compression"""
        # Check cache first
        cached = self.get_cached_prompt(base_prompt, images)
        if cached:
            return cached
        
        # Compress if needed
        optimized = self.compress_prompt(base_prompt)
        
        # Add language-specific enhancements
        if language in self.language_templates:
            # This is a placeholder - actual implementation would integrate templates
            pass
        
        # Cache the result
        self.cache_prompt(optimized, images)
        
        return optimized
    
    def analyze_text_rendering(self, text: str, image_url: str) -> Dict[str, Any]:
        """Analyze text rendering quality (placeholder implementation)"""
        # This would typically use an OCR service to detect text in the image
        # and compare it with the expected text
        
        # Placeholder implementation
        analysis = {
            'text': text,
            'image_url': image_url,
            'detected_text': text,  # Simulate perfect detection
            'accuracy': 1.0,  # Simulate perfect accuracy
            'has_typos': False,
            'recommendation': "Text rendering appears correct"
        }
        
        return analysis
    
    def batch_edit_images(self, image_ids: List[str], edit_instructions: str) -> List[Dict[str, str]]:
        """Batch edit multiple images with the same instructions"""
        results = []
        
        for image_id in image_ids:
            # This would typically call the image editing API
            # Placeholder implementation
            result = {
                'original_image_id': image_id,
                'edited_image_id': f"{image_id}-EDIT-1",
                'status': "success",
                'instructions': edit_instructions
            }
            results.append(result)
        
        return results

if __name__ == "__main__":
    # Example usage
    enhancer = AmazonProductImageEnhancer()
    
    # Test language detection
    test_texts = [
        "Stainless Steel Tumbler",
        "不锈钢保温杯",
        "Verre isotherme en acier inoxydable",
        "ステンレススチールの断熱タンブラー"
    ]
    
    print("Language detection test:")
    for text in test_texts:
        lang = enhancer.detect_language(text)
        print(f"'{text}' -> {lang}")
    
    # Test style mapping
    print("\nStyle mapping test:")
    test_styles = ["极简现代", "日系柔和", "奢华编辑"]
    for style in test_styles:
        mapped = enhancer.map_style(style, "zh")
        print(f"'{style}' -> {mapped}")
    
    # Test prompt compression
    print("\nPrompt compression test:")
    long_prompt = """Please make sure to generate a high-quality product image for a Stainless Steel Tumbler. The tumbler should be placed on a clean white background. Ensure that the product is well-lit and all details are clearly visible. Remember to include the brand logo on the tumbler. Be sure to render the text 'Keeps drinks cold for 24 hours' clearly with no typos."""
    compressed = enhancer.compress_prompt(long_prompt)
    print(f"Original length: {len(long_prompt)}")
    print(f"Compressed length: {len(compressed)}")
    print(f"Compressed: {compressed}")
    
    # Test prompt caching
    print("\nPrompt caching test:")
    test_images = ["oss://image1.jpg"]
    cached_prompt = enhancer.get_cached_prompt(long_prompt, test_images)
    print(f"Cached prompt before caching: {cached_prompt}")
    
    optimized = enhancer.generate_optimized_prompt(long_prompt, test_images)
    cached_prompt_after = enhancer.get_cached_prompt(long_prompt, test_images)
    print(f"Cached prompt after caching: {cached_prompt_after is not None}")
    
    # Test batch editing
    print("\nBatch editing test:")
    test_image_ids = ["IMG-001", "IMG-002"]
    edit_results = enhancer.batch_edit_images(test_image_ids, "Move text to top-left")
    for result in edit_results:
        print(f"{result['original_image_id']} -> {result['edited_image_id']}")