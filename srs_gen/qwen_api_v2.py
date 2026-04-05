import os
import warnings
import json
import re
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Suppress warnings
warnings.filterwarnings("ignore")

# ============================================================
# API CONFIGURATION
# ============================================================
QWEN_API_URL = os.getenv("QWEN_API_URL")
if not QWEN_API_URL:
    print("❌ QWEN_API_URL is not set in .env file")
    QWEN_API_URL = None  # Allow graceful fallback

TEMPERATURE = float(os.getenv("QWEN_TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.getenv("QWEN_MAX_TOKENS", "200"))
DEBUG_OUTPUT = os.getenv("CODE_GEN_DEBUG_OUTPUT", "false").lower() in {"1", "true", "yes", "on"}

if QWEN_API_URL:
    print(f"✓ Using API: {QWEN_API_URL}")
    print(f"✓ Temperature: {TEMPERATURE}, Max Tokens: {MAX_TOKENS}")


def call_qwen_api(system_prompt, user_prompt):
    """Call the Qwen API endpoint"""
    if not QWEN_API_URL:
        return None
    
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_new_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    }
    
    if DEBUG_OUTPUT:
        print(f"[DEBUG] Payload: {json.dumps(payload, indent=2)}")
    
    try:
        print("🔄 Sending request to Qwen API for SRS generation...")
        response = requests.post(
            QWEN_API_URL,
            json=payload,
            headers=headers,
            timeout=300
        )
        
        if DEBUG_OUTPUT:
            print(f"[DEBUG] Response Status: {response.status_code}")
            print(f"[DEBUG] Response: {response.text}")
        
        response.raise_for_status()
        result = response.json()
        
        # Extract text from response (adjust based on your API response format)
        if isinstance(result, dict) and "choices" in result:
            return result["choices"][0]["message"]["content"]
        elif isinstance(result, dict) and "result" in result:
            return result["result"]
        elif isinstance(result, dict) and "response" in result:
            return result["response"]
        else:
            return str(result)
    except requests.RequestException as e:
        print(f"❌ API request failed: {e}")
        return None


def _load_poc_and_prompts(poc_file_path):
    """Load POC data and prompt template"""
    with open(poc_file_path, 'r') as f:
        poc_data = json.load(f)
    
    prompt_file = Path(__file__).parent / "prompts" / "srs_prompt.txt"
    with open(prompt_file, 'r') as f:
        content = f.read()
    
    # Extract system and user prompts
    system_lines = []
    user_lines = []
    section = None
    
    for line in content.split('\n'):
        if "SYSTEM PROMPT" in line:
            section = "system"
        elif "USER PROMPT" in line:
            section = "user"
        elif section and line.strip() and not line.startswith("="):
            (system_lines if section == "system" else user_lines).append(line)
    
    system_prompt = "\n".join(system_lines).strip()
    user_template = "\n".join(user_lines).strip()
    
    # Format user prompt with POC data
    user_prompt = user_template.format(
        title=poc_data.get("title", ""),
        description=poc_data.get("description", ""),
        problem=poc_data.get("problem", ""),
        outcome=poc_data.get("outcome", ""),
        language=poc_data.get("language", ""),
        approach=poc_data.get("approach", ""),
        stack=poc_data.get("stack", ""),
        complexity=poc_data.get("complexity", ""),
        dev_count=poc_data.get("dev_count", "1"),
        skills=", ".join(poc_data.get("skills", [])),
        timeline=poc_data.get("timeline", ""),
        manager=poc_data.get("manager", "")
    )
    
    return system_prompt, user_prompt


def _sanitize_srs_response(response_text):
    """Remove hidden reasoning blocks and keep only structured SRS content."""
    if not response_text:
        return response_text

    cleaned = response_text

    # Remove complete <think>...</think> blocks.
    cleaned = re.sub(r"<think>.*?</think>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)

    # If an opening <think> remains without a close tag, drop everything after it.
    cleaned = re.sub(r"<think>.*$", "", cleaned, flags=re.DOTALL | re.IGNORECASE)

    # Remove any stray tags that may remain.
    cleaned = re.sub(r"</?think>", "", cleaned, flags=re.IGNORECASE)

    return cleaned.strip()


def generate_srs(poc_file_path):
    """
    Generate SRS document from POC file using Qwen API
    
    Args:
        poc_file_path (str or Path): Path to POC JSON file
        
    Returns:
        tuple: (success: bool, output_file: str, message: str)
    """
    try:
        if not QWEN_API_URL:
            return False, None, "❌ QWEN_API_URL not set in .env file"
        
        poc_file = Path(poc_file_path)
        if not poc_file.exists():
            return False, None, f"❌ POC file not found"
        
        # Load data and prompts
        system_prompt, user_prompt = _load_poc_and_prompts(poc_file)
        
        # Call API
        response = call_qwen_api(system_prompt, user_prompt)
        
        if not response:
            return False, None, "❌ Failed to generate SRS from API"

        response = _sanitize_srs_response(response)
        if not response:
            return False, None, "❌ API response contained no valid SRS content after sanitization"
        
        # Save
        output_dir = Path(__file__).parent / "srs"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{poc_file.stem}_SRS.md"
        output_file.write_text(response)
        
        return True, str(output_file), f"✅ SRS generated: {output_file.name}"
    
    except Exception as e:
        return False, None, f"❌ Error: {str(e)}"


if __name__ == "__main__":
    # Setup instructions:
    # 1. Install requests and python-dotenv:
    #    pip install requests python-dotenv
    # 2. Create .env file in the project root with:
    #    QWEN_API_URL=http://localhost:8000/v1/chat/completions (or your API endpoint)
    #    QWEN_TEMPERATURE=0.2
    #    QWEN_MAX_TOKENS=2048
    #    CODE_GEN_DEBUG_OUTPUT=false
    # 3. Run this script
    
    poc_file = Path(__file__).parent.parent / "knowledge_base" / "poc_files" / "poc5.json"
    success, output_file, message = generate_srs(poc_file)
    print(message)
    if success:
        print(f"Output: {output_file}")