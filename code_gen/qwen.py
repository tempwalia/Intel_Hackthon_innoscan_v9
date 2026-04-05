import os
import warnings
import json
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore")

from transformers import AutoModelForCausalLM, AutoTokenizer

# Global model cache
_MODEL = None
_TOKENIZER = None


def _load_model():
    """Load and cache Qwen model"""
    global _MODEL, _TOKENIZER
    if _MODEL is None:
        model_name = "Qwen/Qwen2.5-1.5B-Instruct"
        _MODEL = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype="auto", device_map="auto"
        )
        _TOKENIZER = AutoTokenizer.from_pretrained(model_name)
    return _MODEL, _TOKENIZER


def _load_srs_and_prompts(srs_file_path):
    """Load SRS data and prompt template"""
    with open(srs_file_path, 'r', encoding='utf-8') as f:
        srs_content = f.read()
    
    prompt_file = Path(__file__).parent / "prompts" / "code_prompt.txt"
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    # Replace placeholder with SRS content
    user_prompt = prompt_template.replace("[SRS GOES HERE]", srs_content)
    
    return user_prompt


def generate_code(srs_file_path, poc_id=None):
    """
    Generate code from SRS file using Qwen
    
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
        
        # Load model and prompts
        model, tokenizer = _load_model()
        user_prompt = _load_srs_and_prompts(srs_file_path)
        
        # Prepare messages
        messages = [
            {
                "role": "system",
                "content": "You are an expert software architect. Generate production-ready, complete code with no placeholders."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        
        # Generate code
        print(f"✓ Generating code from SRS...")
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=500
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
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
        return True, str(output_file), message
        
    except Exception as e:
        error_msg = f"❌ Code generation failed: {str(e)}"
        print(error_msg)
        return False, None, error_msg
    
generate_code("/Users/aditikothiyal/Code/intel/srs_gen/srs/714be224_SRS.md", poc_id="714be224")