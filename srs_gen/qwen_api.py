import os
import warnings
import json
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
    exit(1)

TEMPERATURE = float(os.getenv("QWEN_TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.getenv("QWEN_MAX_TOKENS", "1024"))
DEBUG_OUTPUT = os.getenv("BRD_DEBUG_OUTPUT", "false").lower() in {"1", "true", "yes", "on"}

print(f"✓ Using API: {QWEN_API_URL}")
print(f"✓ Temperature: {TEMPERATURE}, Max Tokens: {MAX_TOKENS}")

# ============================================================
# API INFERENCE FUNCTION
# ============================================================
def call_qwen_api(system_prompt, user_prompt):
    """Call the Qwen API endpoint."""
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
        print("🔄 Sending request to Qwen API...")
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


# ============================================================
# MAIN EXECUTION
# ============================================================
# Load POC data from knowledge_base
poc_file = Path(__file__).parent.parent / "knowledge_base" / "poc_files" / "poc2.json"
with open(poc_file, 'r', encoding='utf-8') as f:
    poc_data = json.load(f)

print(f"✓ POC data loaded from: {poc_file}")

# Load prompts from file
prompt_file = Path(__file__).parent / "prompts" / "brd_prompt.txt"
with open(prompt_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract system and user prompts
lines = content.split('\n')
system_prompt_lines = []
user_prompt_lines = []
current_section = None

for line in lines:
    if "SYSTEM PROMPT" in line:
        current_section = "system"
    elif "USER PROMPT" in line:
        current_section = "user"
    elif current_section == "system" and line.strip() and not line.startswith("="):
        system_prompt_lines.append(line)
    elif current_section == "user" and line.strip() and not line.startswith("="):
        user_prompt_lines.append(line)

system_prompt = "\n".join(system_prompt_lines).strip()
user_prompt_template = "\n".join(user_prompt_lines).strip()

# Format user prompt with POC data
user_prompt = user_prompt_template.format(
    title=poc_data.get("title", ""),
    description=poc_data.get("description", ""),
    problem=poc_data.get("problem", ""),
    approach=poc_data.get("approach", ""),
    stack=poc_data.get("stack", ""),
    timeline=poc_data.get("timeline", ""),
    skills=", ".join(poc_data.get("skills", [])),
    complexity=poc_data.get("complexity", ""),
    dev_count=poc_data.get("dev_count", "1")
)

print("✓ Prompts loaded and formatted")

# Call API
response = call_qwen_api(system_prompt, user_prompt)

if not response:
    print("❌ Failed to generate BRD")
    exit(1)

# Save BRD to brd_gen/brd folder with same name as POC file
poc_filename = poc_file.stem  # Get filename without extension (poc2)

output_dir = Path(__file__).parent / "brd"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / f"{poc_filename}_BRD.md"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(response)

print(f"\n✓ BRD saved to: {output_file}")
print("\n" + "="*80)
print("GENERATED BRD:")
print("="*80)
print(response)
