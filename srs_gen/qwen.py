import warnings
import json
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer

warnings.filterwarnings("ignore")

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


def generate_srs(poc_file_path):
    """
    Generate SRS document from POC file
    
    Args:
        poc_file_path (str or Path): Path to POC JSON file
        
    Returns:
        tuple: (success: bool, output_file: str, message: str)
    """
    try:
        poc_file = Path(poc_file_path)
        if not poc_file.exists():
            return False, None, f"❌ POC file not found"
        
        # Load data and prompts
        system_prompt, user_prompt = _load_poc_and_prompts(poc_file)
        
        # Load model
        model, tokenizer = _load_model()
        
        # Generate
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        generated_ids = model.generate(**model_inputs, max_new_tokens=2048)
        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Save
        output_dir = Path(__file__).parent / "srs"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{poc_file.stem}_SRS.md"
        output_file.write_text(response)
        
        return True, str(output_file), f"✅ SRS generated: {output_file.name}"
    
    except Exception as e:
        return False, None, f"❌ Error: {str(e)}"


if __name__ == "__main__":
    poc_file = Path(__file__).parent.parent / "knowledge_base" / "poc_files" / "poc2.json"
    success, output_file, message = generate_srs(poc_file)
    print(message)
    if success:
        print(f"Output: {output_file}")