"""
File I/O operations for InnoScan
"""

import json
import os
from frontend.config import EXCEPTION_DIR, UPLOADS_DIR, KNOWLEDGE_BASE_PATH


def load_json_file(filepath):
    """Load JSON file safely"""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading {filepath}: {e}")
        return None


def save_json_file(filepath, data):
    """Save JSON file safely"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"⚠️ Error saving {filepath}: {e}")
        return False


def save_poc_to_knowledge_base(poc_record):
    """
    Save a POC record to the local knowledge base
    
    Args:
        poc_record: Dictionary with 'id' field
        
    Returns:
        tuple: (success: bool, file_path: str, message: str)
    """
    try:
        poc_id = poc_record.get("id")
        if not poc_id:
            return False, None, "❌ POC record missing 'id' field"
        
        kb_file_path = os.path.join(KNOWLEDGE_BASE_PATH, f"{poc_id}.json")
        
        if save_json_file(kb_file_path, poc_record):
            message = f"✅ POC ingested to Knowledge Base (ID: {poc_id})"
            print(message)
            return True, kb_file_path, message
        else:
            return False, None, "❌ Failed to save POC to knowledge base"
    
    except Exception as e:
        return False, None, f"❌ Error saving POC: {str(e)}"


def get_idea_from_uploads(idea_id):
    """Load idea from uploads folder"""
    idea_file = os.path.join(UPLOADS_DIR, f"{idea_id}.json")
    return load_json_file(idea_file)


def save_idea_to_uploads(idea_id, idea_data):
    """Save idea to uploads folder"""
    idea_file = os.path.join(UPLOADS_DIR, f"{idea_id}.json")
    return save_json_file(idea_file, idea_data)


def get_exception(exception_id):
    """Load exception from exception folder"""
    exception_file = os.path.join(EXCEPTION_DIR, f"{exception_id}.json")
    return load_json_file(exception_file)


def save_exception(exception_id, exception_data):
    """Save exception to exception folder"""
    exception_file = os.path.join(EXCEPTION_DIR, f"{exception_id}.json")
    return save_json_file(exception_file, exception_data)


def list_exceptions():
    """Get all exception files"""
    exceptions = []
    if not os.path.exists(EXCEPTION_DIR):
        return exceptions
    
    for filename in os.listdir(EXCEPTION_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(EXCEPTION_DIR, filename)
            data = load_json_file(filepath)
            if data:
                exceptions.append(data)
    
    return exceptions
