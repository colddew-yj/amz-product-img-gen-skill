#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Image Editing Script

This script provides batch editing functionality for the amazon-product-image-wan27 skill,
allowing users to apply the same edits to multiple images at once.
"""

import os
import json
import time
from typing import List, Dict, Any, Optional

class BatchImageEditor:
    def __init__(self):
        self.edit_history = {}
        self.history_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "edit_history.json")
        self._load_history()
    
    def _load_history(self):
        """Load edit history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.edit_history = json.load(f)
            except Exception:
                pass
    
    def _save_history(self):
        """Save edit history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.edit_history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def batch_edit(self, image_ids: List[str], edit_instructions: str) -> List[Dict[str, Any]]:
        """Batch edit multiple images with the same instructions"""
        results = []
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        for image_id in image_ids:
            # Generate edit ID
            edit_count = len(self.edit_history.get(image_id, [])) + 1
            edit_id = f"{image_id}-EDIT-{edit_count}"
            
            # Create edit record
            edit_record = {
                "edit_id": edit_id,
                "original_image_id": image_id,
                "instructions": edit_instructions,
                "timestamp": timestamp,
                "status": "success"  # Placeholder for actual API response
            }
            
            # Add to history
            if image_id not in self.edit_history:
                self.edit_history[image_id] = []
            self.edit_history[image_id].append(edit_record)
            
            results.append(edit_record)
        
        # Save history
        self._save_history()
        
        return results
    
    def get_edit_history(self, image_id: str) -> List[Dict[str, Any]]:
        """Get edit history for a specific image"""
        return self.edit_history.get(image_id, [])
    
    def get_all_history(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all edit history"""
        return self.edit_history
    
    def revert_to_version(self, edit_id: str) -> Optional[Dict[str, Any]]:
        """Revert to a specific edit version"""
        # Find the edit record
        for image_id, edits in self.edit_history.items():
            for edit in edits:
                if edit.get("edit_id") == edit_id:
                    # Create a new edit that reverts to this version
                    revert_count = len(edits) + 1
                    revert_id = f"{image_id}-EDIT-{revert_count}"
                    
                    revert_record = {
                        "edit_id": revert_id,
                        "original_image_id": image_id,
                        "instructions": f"Revert to version {edit_id}",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "success",
                        "reverted_from": edit_id
                    }
                    
                    edits.append(revert_record)
                    self._save_history()
                    
                    return revert_record
        
        return None
    
    def clear_history(self, image_id: Optional[str] = None):
        """Clear edit history for a specific image or all images"""
        if image_id:
            if image_id in self.edit_history:
                del self.edit_history[image_id]
        else:
            self.edit_history = {}
        
        self._save_history()
    
    def generate_edit_instructions(self, product_type: str, desired_changes: str) -> str:
        """Generate edit instructions based on product type and desired changes"""
        # Simple template for generating edit instructions
        templates = {
            "text": "Modify the text to '{desired_changes}' while maintaining the same style and position",
            "background": "Change the background to '{desired_changes}' while keeping the product in the same position",
            "lighting": "Adjust lighting to '{desired_changes}' while maintaining product details",
            "angle": "Change the viewing angle to '{desired_changes}' while keeping the product in focus",
            "style": "Change the overall style to '{desired_changes}' while preserving product identity"
        }
        
        # Determine change type based on keywords
        change_type = "style"  # Default
        desired_lower = desired_changes.lower()
        
        if any(keyword in desired_lower for keyword in ["text", "copy", "font", "文字", "文案"]):
            change_type = "text"
        elif any(keyword in desired_lower for keyword in ["background", "背景"]):
            change_type = "background"
        elif any(keyword in desired_lower for keyword in ["light", "lighting", "brightness", "lighting", "光线"]):
            change_type = "lighting"
        elif any(keyword in desired_lower for keyword in ["angle", "view", "视角", "角度"]):
            change_type = "angle"
        
        return templates.get(change_type, templates["style"]).format(desired_changes=desired_changes)

def main():
    """Main function for testing"""
    editor = BatchImageEditor()
    
    # Test batch editing
    test_image_ids = ["IMG-001", "IMG-002", "IMG-003"]
    test_instructions = "Move text from top-right to top-left and change font to rounded_bold"
    
    print("Batch editing test:")
    results = editor.batch_edit(test_image_ids, test_instructions)
    
    for result in results:
        print(f"Original: {result['original_image_id']} -> Edited: {result['edit_id']}")
    
    # Test edit history
    print("\nEdit history test:")
    for image_id in test_image_ids:
        history = editor.get_edit_history(image_id)
        print(f"History for {image_id}:")
        for edit in history:
            print(f"  - {edit['edit_id']}: {edit['instructions']} ({edit['timestamp']})")
    
    # Test revert functionality
    if results:
        revert_result = editor.revert_to_version(results[0]['edit_id'])
        if revert_result:
            print(f"\nReverted to version: {revert_result['reverted_from']} -> New version: {revert_result['edit_id']}")
    
    # Test instruction generation
    print("\nInstruction generation test:")
    test_cases = [
        ("tumbler", "Change text to 'Keep cool for 24h'"),
        ("mug", "Change background to wooden table"),
        ("watch", "Adjust lighting to warm tone")
    ]
    
    for product, change in test_cases:
        instruction = editor.generate_edit_instructions(product, change)
        print(f"Product: {product}, Change: {change}")
        print(f"Generated instruction: {instruction}")

if __name__ == "__main__":
    main()