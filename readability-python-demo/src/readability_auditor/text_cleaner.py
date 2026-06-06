"""Clean scraped documentation text to extract only prose content."""

import re
from typing import Optional


def clean_human_documentation(text: str) -> str:
    """
    Clean human documentation text by removing non-prose content.
    
    Removes:
    - Code blocks (```...```)
    - Inline code (`...`)
    - Navigation lists (lines that are just links)
    - Image links
    - Short lines (likely navigation/UI elements)
    - URL-only lines
    
    Keeps:
    - Paragraphs of prose text
    - Headers (for structure)
    - Lists with descriptive text
    """
    if not text:
        return ""
    
    lines = text.split('\n')
    cleaned_lines = []
    
    in_code_block = False
    
    for line in lines:
        # Skip code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        
        if in_code_block:
            continue
        
        # Skip empty lines
        if not line.strip():
            cleaned_lines.append('')
            continue
        
        # Skip lines that are just images
        if re.match(r'^!\[.*?\]\(.*?\)$', line.strip()):
            continue
        
        # Skip lines that are just links (navigation)
        if re.match(r'^\[.*?\]\(.*?\)$', line.strip()):
            continue
        
        # Skip lines that are mostly links (e.g., "[Link1](url) [Link2](url)")
        link_count = len(re.findall(r'\[.*?\]\(.*?\)', line))
        if link_count > 2 and len(line) < 200:
            continue
        
        # Skip very short lines (likely UI elements)
        if len(line.strip()) < 10:
            continue
        
        # Skip lines that start with common navigation patterns
        if line.strip().startswith(('⌘', 'Ctrl', 'Cmd', 'Alt', 'Shift')):
            continue
        
        # Skip lines that look like breadcrumbs or version info
        if re.match(r'^v?\d+\.\d+(\.\d+)?', line.strip()):
            continue
        
        # Clean inline code but keep the line
        line = re.sub(r'`[^`]+`', '', line)
        
        # Clean image references but keep surrounding text
        line = re.sub(r'!\[.*?\]\(.*?\)', '', line)
        
        # Clean link URLs but keep link text
        line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)
        
        # Skip if line is now empty after cleaning
        if not line.strip():
            continue
        
        cleaned_lines.append(line)
    
    # Join and clean up multiple blank lines
    cleaned_text = '\n'.join(cleaned_lines)
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    
    return cleaned_text.strip()


def calculate_word_count(text: str) -> int:
    """Calculate word count of text."""
    return len(text.split())
