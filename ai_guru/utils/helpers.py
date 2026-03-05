import json
import re


def extract_json(text: str):
    """
    Robustly extract JSON from a string.
    Handles markdown code blocks, trailing commas, plain LLM text, and dirty outputs.
    Priority order:
      1. Explicit ```json ... ``` block
      2. Any ``` ... ``` block
      3. Outermost [ ] or { } bracket pair
      4. Full text fallback
    """
    json_str = None

    # Priority 1: explicit ```json block
    match = re.search(r'```json\s*([\[\{][\s\S]*?[\]\}])\s*```', text, re.DOTALL)
    if match:
        json_str = match.group(1)

    # Priority 2: any generic ``` block that looks like JSON
    if not json_str:
        match = re.search(r'```\s*([\[\{][\s\S]*?[\]\}])\s*```', text, re.DOTALL)
        if match:
            json_str = match.group(1)

    # Priority 3: outermost [ ] or { } — find first open bracket to last close bracket
    if not json_str:
        # Find array: from first [ to last ]
        arr_match = re.search(r'(\[[\s\S]*\])', text, re.DOTALL)
        # Find object: from first { to last }
        obj_match = re.search(r'(\{[\s\S]*\})', text, re.DOTALL)

        if arr_match and obj_match:
            # Pick whichever appears first in the text
            json_str = arr_match.group(1) if arr_match.start() < obj_match.start() else obj_match.group(1)
        elif arr_match:
            json_str = arr_match.group(1)
        elif obj_match:
            json_str = obj_match.group(1)
        else:
            json_str = text

    # Attempt 1: parse as-is
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    # Attempt 2: clean common LLM JSON artifacts
    try:
        # Remove trailing commas before ] or }
        cleaned = re.sub(r',\s*(\]|\})', r'\1', json_str)
        # Remove single-line comments (// ...)
        cleaned = re.sub(r'//[^\n]*', '', cleaned)
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        # Log clearly for debugging — never silent fail
        short_text = text[:600].replace('\n', ' ')
        print(f"[extract_json] FATAL: Could not parse JSON. Raw snippet: {short_text!r}")
        raise ValueError(
            f"AI menghasilkan output yang tidak bisa diproses (bukan JSON valid). "
            f"Coba generate ulang. Detail: {e}"
        ) from e
