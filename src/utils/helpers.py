import json
import re

def extract_json(text: str):
    """
    Robustly extract JSON from a string.
    Handles markdown code blocks, plain text, and dirty outputs.
    """
    # Try to find JSON block in markdown
    match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # If no markdown, try to find the first likely JSON bracket structure
        # This is a simple heuristic: find first { or [ and last } or ]
        match_obj = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
        if match_obj:
            json_str = match_obj.group(1)
        else:
            json_str = text
            
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {text[:500]}...") # Log first 500 chars
        raise e
