#!/usr/bin/env python3
"""
Prompt management utility for Vision AI Box Counting
"""

import os
import sys
from pathlib import Path

PROMPT_FILE = "prompt.txt"

def show_current_prompt():
    """Display the current prompt"""
    print("🤖 Current OpenAI Vision AI Prompt")
    print("=" * 60)
    
    if not os.path.exists(PROMPT_FILE):
        print("❌ prompt.txt file not found!")
        return
    
    try:
        with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
            prompt = f.read().strip()
        
        print(prompt)
        print("=" * 60)
        print(f"📏 Prompt length: {len(prompt)} characters")
        print(f"📄 Lines: {len(prompt.split(chr(10)))}")
        print(f"📁 File: {os.path.abspath(PROMPT_FILE)}")
        
    except Exception as e:
        print(f"❌ Error reading prompt: {e}")

def edit_prompt():
    """Open prompt file for editing"""
    if not os.path.exists(PROMPT_FILE):
        print(f"❌ {PROMPT_FILE} not found!")
        return
    
    # Try different editors
    editors = ['code', 'nano', 'vim', 'open']
    
    for editor in editors:
        try:
            os.system(f"{editor} {PROMPT_FILE}")
            print(f"✅ Opened {PROMPT_FILE} with {editor}")
            return
        except:
            continue
    
    print(f"⚠️  Could not open editor. Edit {PROMPT_FILE} manually.")

def create_prompt_template():
    """Create a new prompt template"""
    template = """You are an expert computer vision AI specialized in counting boxes and extracting text labels from images.

Please analyze the provided image and:

1. **Count all visible boxes/packages/containers** in the image
2. **Extract any visible text labels, barcodes, or identifying information** on the boxes
3. **Identify the type of boxes** (shipping boxes, product boxes, containers, etc.)
4. **Note the arrangement/stacking** of boxes if relevant

Return your analysis in the following JSON format:
{
    "total_count": <number>,
    "box_details": [
        {
            "box_id": <sequential_number>,
            "type": "<box_type>",
            "labels": ["<text1>", "<text2>"],
            "confidence": <0.0-1.0>,
            "position": "<general_position_description>"
        }
    ],
    "summary": {
        "total_boxes": <number>,
        "boxes_with_labels": <number>,
        "common_labels": ["<frequent_labels>"],
        "arrangement": "<description_of_arrangement>"
    },
    "confidence_score": <overall_confidence_0.0-1.0>
}

Be thorough and accurate. If you cannot clearly see a box or are unsure, indicate lower confidence. If no text is visible on a box, use an empty array for labels."""

    try:
        with open(PROMPT_FILE, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"✅ Created prompt template: {PROMPT_FILE}")
    except Exception as e:
        print(f"❌ Error creating template: {e}")

def backup_prompt():
    """Create a backup of the current prompt"""
    if not os.path.exists(PROMPT_FILE):
        print(f"❌ {PROMPT_FILE} not found!")
        return
    
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"prompt_backup_{timestamp}.txt"
    
    try:
        with open(PROMPT_FILE, 'r', encoding='utf-8') as src:
            content = src.read()
        
        with open(backup_name, 'w', encoding='utf-8') as dst:
            dst.write(content)
        
        print(f"✅ Backup created: {backup_name}")
    except Exception as e:
        print(f"❌ Error creating backup: {e}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("🔧 Prompt Management Utility")
        print("=" * 40)
        print("Usage:")
        print("  python prompt_manager.py show      # Display current prompt")
        print("  python prompt_manager.py edit      # Edit prompt file")
        print("  python prompt_manager.py create    # Create new template")
        print("  python prompt_manager.py backup    # Backup current prompt")
        print()
        print("💡 Quick view:")
        show_current_prompt()
        return
    
    command = sys.argv[1].lower()
    
    if command == "show":
        show_current_prompt()
    elif command == "edit":
        edit_prompt()
    elif command == "create":
        create_prompt_template()
    elif command == "backup":
        backup_prompt()
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: show, edit, create, backup")

if __name__ == "__main__":
    main()