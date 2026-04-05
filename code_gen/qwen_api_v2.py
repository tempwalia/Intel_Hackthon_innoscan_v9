import os
import warnings
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# Import parser to auto-create folder structure
# Ensure code_gen/ directory is in path so code_gen_parse can be found
# regardless of how this module is loaded (direct or via importlib)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from code_gen_parse import parse_and_generate_files
    parser_available = True
except ImportError:
    parser_available = False
    print("⚠️ code_gen_parse module not available. Folder structure won't be created automatically.")

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
MAX_TOKENS = int(os.getenv("QWEN_MAX_TOKENS", "2048"))
DEBUG_OUTPUT = os.getenv("CODE_GEN_DEBUG_OUTPUT", "false").lower() in {"1", "true", "yes", "on"}

if QWEN_API_URL:
    print(f"✓ Using API: {QWEN_API_URL}")
print(f"✓ Temperature: {TEMPERATURE}, Max Tokens: {MAX_TOKENS}")


def call_qwen_api(system_prompt, user_prompt):
    """Call the Qwen API endpoint"""
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
        print("🔄 Sending request to Qwen API for code generation...")
        response = requests.post(
            QWEN_API_URL,
            json=payload,
            headers=headers,
            timeout=1200
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


def generate_code(srs_file_path, poc_id=None):
    """
    Generate code from SRS file using Qwen API
    
    Args:
        srs_file_path: Path to the SRS markdown file
        poc_id: Optional POC ID for output file naming
        
    Returns:
        tuple: (success: bool, output_file: str, message: str)
    """
    try:
        # Validate SRS file exists
        if not os.path.exists(srs_file_path):
            return False, None, f"❌ SRS file not found: {srs_file_path}"
        
        # Load SRS and prompt template
        with open(srs_file_path, 'r', encoding='utf-8') as f:
            srs_content = f.read()
        
        prompt_file = Path(__file__).parent / "prompts" / "code_prompt.txt"
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        
        # Replace placeholder with SRS content
        user_prompt = prompt_template.replace("[SRS GOES HERE]", srs_content)
        
        # Prepare system prompt
        system_prompt = "You are an expert software architect. Generate production-ready, complete code with no placeholders."
        
        # Call API
        response = call_qwen_api(system_prompt, user_prompt)
        
        if not response:
            return False, None, "❌ Failed to generate code from API"
        
        # Save output
        output_dir = Path(__file__).parent / "code"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Use poc_id if provided, else use timestamp
        if poc_id:
            output_file = output_dir / f"{poc_id}_GENERATED_CODE.txt"
        else:
            output_file = output_dir / "GENERATED_CODE.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response)
        
        message = f"✅ Code generated successfully"
        print(f"{message}: {output_file}")
        
        # Automatically trigger parser to create folder structure
        if parser_available :
            print(f"\n🔄 Creating project folder structure...")
            try:
                parse_and_generate_files(str(output_file))
                print(f"✅ Project structure created successfully!")
            except Exception as e:
                print(f"⚠️ Error creating folder structure: {e}")
                print(f"   You can manually run: python code_gen_parse.py {output_file} {poc_id}")
        
        return True, str(output_file), message
        
    except Exception as e:
        error_msg = f"❌ Code generation failed: {str(e)}"
        print(error_msg)
        return False, None, error_msg
    
if __name__ == "__main__":
    generate_code("srs_gen/srs/5da3829e_SRS.md","5da3829e")