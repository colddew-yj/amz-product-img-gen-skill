#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Style Mapping and Language Support Script

This script handles style mapping between different languages and provides
language-specific prompt templates for the amazon-product-image-wan27 skill.
"""

import json
import os
from typing import Dict, List, Optional

class StyleMapper:
    def __init__(self):
        self.style_mappings = {
            "zh": {
                "极简现代": "minimal_modern",
                "现代简洁": "minimal_modern",
                "干净电商": "minimal_modern",
                "日系柔和": "japanese_soft",
                "手写风格": "japanese_soft",
                "刷字艺术体": "japanese_soft",
                "奢华编辑": "luxury_editorial",
                "高端杂志": "luxury_editorial",
                "现代衬线": "luxury_editorial",
                "圆润大粗体": "rounded_bold",
                "可爱友好": "rounded_bold",
                "粗壮饱满": "rounded_bold",
                "雅黑light": "yahoma_light",
                "纤细轻量": "yahoma_light",
                "微软雅黑": "yahoma_light"
            },
            "fr": {
                "moderne minimal": "minimal_modern",
                "moderne et propre": "minimal_modern",
                "e-commerce propre": "minimal_modern",
                "japonais doux": "japanese_soft",
                "style manuscrit": "japanese_soft",
                "calligraphie artistique": "japanese_soft",
                "luxueux éditorial": "luxury_editorial",
                "magazine de luxe": "luxury_editorial",
                "serif moderne": "luxury_editorial",
                "épais arrondi": "rounded_bold",
                "charmant et amical": "rounded_bold",
                "gros et plein": "rounded_bold",
                "yahei léger": "yahoma_light",
                "mince et léger": "yahoma_light",
                "microsoft yahei": "yahoma_light"
            },
            "ja": {
                "ミニマルモダン": "minimal_modern",
                "モダンでシンプル": "minimal_modern",
                "クリーンな電子商取引": "minimal_modern",
                "日本の柔らかさ": "japanese_soft",
                "手書きスタイル": "japanese_soft",
                "芸術的な筆文字": "japanese_soft",
                "高級エディトリアル": "luxury_editorial",
                "高級雑誌": "luxury_editorial",
                "モダンセリフ": "luxury_editorial",
                "まるっと太字": "rounded_bold",
                "かわいくて友好的": "rounded_bold",
                "太くて豊か": "rounded_bold",
                "ヤハオライト": "yahoma_light",
                "細くて軽い": "yahoma_light",
                "マイクロソフトヤハオ": "yahoma_light"
            }
        }
        
        self.language_support = {
            "minimal_modern": ["zh", "en", "ja"],
            "japanese_soft": ["ja", "zh", "ko"],
            "luxury_editorial": ["en", "fr", "zh"],
            "rounded_bold": ["zh", "en", "ja"],
            "yahoma_light": ["zh", "en", "ja", "fr"]
        }
    
    def map_style(self, style: str, language: str = "en") -> str:
        """Map style from different languages to English style profile"""
        style_lower = style.lower()
        
        if language in self.style_mappings:
            # Try exact match
            if style in self.style_mappings[language]:
                return self.style_mappings[language][style]
            
            # Try case-insensitive match
            for key, value in self.style_mappings[language].items():
                if key.lower() == style_lower:
                    return value
        
        # Return original if no mapping found
        return style
    
    def get_supported_languages(self, style: str) -> List[str]:
        """Get list of supported languages for a given style"""
        if style in self.language_support:
            return self.language_support[style]
        return ["en"]  # Default to English
    
    def validate_style(self, style: str) -> bool:
        """Validate if style is a supported style profile"""
        return style in self.language_support
    
    def get_recommended_style(self, product_type: str, language: str = "en") -> str:
        """Get recommended style based on product type"""
        # Simple recommendation logic based on product type
        product_type_lower = product_type.lower()
        
        if any(keyword in product_type_lower for keyword in ["luxury", "premium", "high-end", " luxury", "高端", "奢华", "プレミアム"]):
            return "luxury_editorial"
        elif any(keyword in product_type_lower for keyword in ["cute", "friendly", "playful", "可爱", "友好", "かわいい"]):
            return "rounded_bold"
        elif any(keyword in product_type_lower for keyword in ["japanese", "asian", "和风", "日本", "アジアン"]):
            return "japanese_soft"
        elif any(keyword in product_type_lower for keyword in ["modern", "minimal", "clean", "现代", "极简", "クリーン"]):
            return "minimal_modern"
        else:
            return "yahoma_light"  # Default for general products

def main():
    """Main function for testing"""
    mapper = StyleMapper()
    
    # Test style mapping
    test_cases = [
        ("极简现代", "zh"),
        ("japonais doux", "fr"),
        ("高級エディトリアル", "ja"),
        ("minimal_modern", "en")
    ]
    
    print("Style mapping test:")
    for style, lang in test_cases:
        mapped = mapper.map_style(style, lang)
        print(f"'{style}' ({lang}) -> {mapped}")
    
    # Test language support
    print("\nLanguage support test:")
    for style in mapper.language_support:
        langs = mapper.get_supported_languages(style)
        print(f"{style}: {', '.join(langs)}")
    
    # Test style recommendation
    print("\nStyle recommendation test:")
    test_products = [
        "Luxury Watch",
        "Cute Cat Mug",
        "Japanese Tea Set",
        "Modern Desk Lamp",
        "General Smartphone Case"
    ]
    
    for product in test_products:
        recommended = mapper.get_recommended_style(product)
        print(f"{product} -> {recommended}")

if __name__ == "__main__":
    main()