"""
POC (Proof of Concept) business logic and operations
"""

import sys
import os
import traceback
import threading
import json
import importlib.util
import logging
from datetime import datetime

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "similarity_check"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "srs_gen"))

from frontend.config import KNOWLEDGE_BASE_PATH, RETRIEVER_CONFIG, INGESTION_CONFIG
from frontend.services.file_service import save_poc_to_knowledge_base, get_idea_from_uploads


def _setup_execution_logger():
    """Create date-based log folder and return configured logger."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    date_folder = datetime.now().strftime("%Y-%m-%d")
    log_dir = os.path.join(project_root, "logs", date_folder)
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("poc_execution")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        log_file = os.path.join(log_dir, "execution.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(process)d | %(threadName)s | %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


EXEC_LOGGER = _setup_execution_logger()


def _log_event(level, message):
    """Log to both file and terminal using configured logger handlers."""
    if level == "error":
        EXEC_LOGGER.error(message)
    elif level == "warning":
        EXEC_LOGGER.warning(message)
    else:
        EXEC_LOGGER.info(message)

# Import SRS generation
try:
    from qwen_api_v2 import generate_srs
    srs_generator_available = True
except ImportError:
    _log_event("warning", "⚠️ SRS generator not available")
    srs_generator_available = False

# Import code generation using importlib to avoid naming conflict
code_generator_available = False
generate_code = None
try:
    code_gen_path = os.path.join(os.path.dirname(__file__), "..", "..", "code_gen", "qwen_api_v2.py")
    spec = importlib.util.spec_from_file_location("code_gen_qwen", code_gen_path)
    code_gen_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(code_gen_module)
    generate_code = code_gen_module.generate_code
    code_generator_available = True
    _log_event("info", "✅ Code generator loaded successfully")
except Exception as e:
    _log_event("warning", f"⚠️ Code generator not available: {e}")
    traceback.print_exc()
    code_generator_available = False

try:
    from retrieval import POCRetriever
    retriever = POCRetriever(
        index_name=RETRIEVER_CONFIG['index_name'],
        knowledge_base_path=RETRIEVER_CONFIG['knowledge_base_path']
    )
    _log_event("info", "✅ POCRetriever initialized successfully")
except Exception as e:
    _log_event("warning", f"⚠️ POCRetriever unavailable: {e}")
    retriever = None

try:
    from embedding import download_hugging_face_embeddings
    from ingestion import chunk_documents, ingest_documents
    embeddings_model = download_hugging_face_embeddings()
    _log_event("info", "✅ Embeddings model loaded for ingestion")
except Exception as e:
    _log_event("warning", f"⚠️ Embeddings model unavailable: {e}")
    embeddings_model = None


def find_similar_pocs(title, description, problem):
    """Find similar POCs in the knowledge base"""
    if not retriever:
        return []
    
    try:
        _log_event("info", f"[START] Similarity search started for title='{title}'")
        similar_pocs = retriever.find_similar_pocs(
            title=title,
            description=description,
            problem=problem,
            score_threshold=RETRIEVER_CONFIG['score_threshold'],
            top_k=RETRIEVER_CONFIG['top_k']
        )
        _log_event("info", f"[DONE] Similarity search completed. Matches found: {len(similar_pocs)}")
        return similar_pocs
    except Exception as e:
        _log_event("error", f"⚠️ Retriever error: {e}")
        traceback.print_exc()
        return []


def get_poc_details(poc_id):
    """Get full POC details from knowledge base"""
    import json
    
    poc_data = None
    
    # Try retriever first if available
    if retriever:
        try:
            poc_data = retriever.get_poc_from_knowledge_base(poc_id)
        except Exception as e:
            _log_event("warning", f"⚠️ Retriever error getting POC {poc_id}: {e}")
    
    # Always try to load full POC JSON file as fallback or supplement
    try:
        poc_file = os.path.join(KNOWLEDGE_BASE_PATH, f"{poc_id}.json")
        if os.path.exists(poc_file):
            with open(poc_file, 'r', encoding='utf-8') as f:
                full_poc_data = json.load(f)
            if poc_data:
                # Merge with retriever data, prioritizing file data
                poc_data.update(full_poc_data)
            else:
                # Use file data if no retriever data
                poc_data = full_poc_data
    except Exception as e:
        _log_event("warning", f"⚠️ Error loading POC JSON file {poc_id}: {e}")
    
    return poc_data


def generate_srs_async(poc_id):
    """Generate SRS asynchronously in background thread after ingestion"""
    def _generate():
        if not srs_generator_available:
            _log_event("warning", f"⚠️ SRS generator not available for POC {poc_id}")
            return
        
        try:
            poc_file_path = os.path.join(KNOWLEDGE_BASE_PATH, f"{poc_id}.json")
            if not os.path.exists(poc_file_path):
                _log_event("warning", f"⚠️ POC file not found: {poc_file_path}")
                return
            
            # Load POC to check boilerplate_enabled flag
            with open(poc_file_path, 'r', encoding='utf-8') as f:
                poc_data = json.load(f)
            boilerplate_enabled = poc_data.get("boilerplate_enabled", False)
            _log_event("info", f"[SRS] Boilerplate enabled={boilerplate_enabled} for POC {poc_id}")
            
            _log_event("info", f"[SRS] Generating SRS for POC {poc_id}")
            success, output_file, message = generate_srs(poc_file_path)
            _log_event("info", f"[SRS] Generation result success={success}, output={output_file}")
            
            if success:
                _log_event("info", f"✅ {message}")
                _log_event("info", f"[SRS] File saved: {output_file}")
                
                # Check if code generation is enabled
                if boilerplate_enabled:
                    _log_event("info", f"[CODE] Triggering boilerplate code generation for POC {poc_id}")
                    generate_code_async(poc_id, output_file)
                else:
                    _log_event("info", f"⏭️  Boilerplate code generation disabled for POC {poc_id}")
            else:
                _log_event("error", f"❌ SRS generation failed: {message}")
        
        except Exception as e:
            _log_event("error", f"❌ Error generating SRS for {poc_id}: {e}")
            traceback.print_exc()
    
    # Run in background thread to not block ingestion
    thread = threading.Thread(target=_generate, daemon=True)
    thread.start()


def generate_code_async(poc_id, srs_file_path):
    """Generate boilerplate code asynchronously from SRS"""
    def _generate():
        if not code_generator_available:
            _log_event("warning", f"⚠️ Code generator not available for POC {poc_id}")
            return
        
        try:
            _log_event("info", f"[CODE] Generating boilerplate code for POC {poc_id}")
            success, output_file, message = generate_code(srs_file_path, poc_id)
            
            if success:
                _log_event("info", f"✅ {message}")
                _log_event("info", f"[CODE] File saved: {output_file}")
            else:
                _log_event("error", f"❌ Code generation failed: {message}")
        
        except Exception as e:
            _log_event("error", f"❌ Error generating code for {poc_id}: {e}")
            traceback.print_exc()
    
    # Run in background thread to not block SRS generation
    thread = threading.Thread(target=_generate, daemon=True)
    thread.start()



def ingest_poc_to_pinecone(poc_record):
    """Ingest POC record to Pinecone"""
    if not embeddings_model:
        return False, "⚠️ Embeddings model not available"
    
    try:
        idea_id = poc_record.get("id")
        _log_event("info", f"[INGEST] Starting Pinecone ingestion for POC {idea_id}")
        chunks = chunk_documents(
            [poc_record],
            chunk_size=INGESTION_CONFIG['chunk_size'],
            chunk_overlap=INGESTION_CONFIG['chunk_overlap']
        )
        
        if chunks:
            docsearch = ingest_documents(
                chunks,
                index_name=INGESTION_CONFIG['index_name'],
                embeddings=embeddings_model
            )
            message = f"✅ POC ingested to Pinecone (POC ID: {idea_id}, {len(chunks)} chunks)"
            _log_event("info", message)
            
            # Trigger SRS generation asynchronously after successful ingestion
            generate_srs_async(idea_id)
            
            return True, message
        else:
            return False, "⚠️ Failed to create chunks for ingestion"
    
    except Exception as e:
        error_msg = f"⚠️ Ingestion failed: {str(e)}"
        _log_event("error", error_msg)
        traceback.print_exc()
        return False, error_msg


def process_approved_poc(idea_id):
    """Process approved POC: save to KB and ingest to Pinecone"""
    try:
        _log_event("info", f"[PROCESS] Started approved POC flow for idea_id={idea_id}")
        # Load POC from uploads
        poc_record = get_idea_from_uploads(idea_id)
        if not poc_record:
            _log_event("warning", f"[PROCESS] POC not found in uploads for idea_id={idea_id}")
            return False, "⚠️ POC not found in uploads"
        
        poc_id = poc_record.get("id")
        _log_event("info", f"📁 Processing Approved POC (ID: {poc_id})")
        
        # Save to knowledge base
        kb_success, kb_path, kb_msg = save_poc_to_knowledge_base(poc_record)
        
        # Ingest to Pinecone
        ingestion_success, ingestion_msg = ingest_poc_to_pinecone(poc_record)
        
        final_msg = kb_msg
        if ingestion_msg:
            final_msg += f" | {ingestion_msg}"

        _log_event("info", f"[PROCESS] Completed approved POC flow for poc_id={poc_id} success={kb_success and ingestion_success}")
        
        return kb_success and ingestion_success, final_msg
    
    except Exception as e:
        error_msg = f"❌ Error processing approved POC: {str(e)}"
        _log_event("error", error_msg)
        return False, error_msg
