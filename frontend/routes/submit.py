"""
POC submission and similarity checking routes
"""

import uuid
import json
import os
from flask import request, jsonify, session
from datetime import datetime

from frontend.config import UPLOADS_DIR, KNOWLEDGE_BASE_PATH
from frontend.services.file_service import save_idea_to_uploads, save_poc_to_knowledge_base, get_idea_from_uploads
from frontend.services.poc_service import find_similar_pocs, get_poc_details, ingest_poc_to_pinecone


def register_submit_routes(app):
    """Register all submission routes"""
    
    @app.route('/api/submit', methods=['POST'])
    def submit_idea():
        """Submit an idea and check for similar POCs"""
        try:
            data = request.get_json()
            
            # Validate required fields
            empty_fields = []
            for field in ["title", "description", "problem", "outcome", "language", "approach", "stack", "complexity", "timeline", "manager"]:
                if not data.get(field) or not str(data.get(field)).strip():
                    empty_fields.append(field.replace("_", " ").title())
            
            if not data.get("skills") or len(data.get("skills", [])) == 0:
                empty_fields.append("Required Skills / Roles")
            
            if empty_fields:
                return jsonify({
                    "success": False, 
                    "message": f"Please fill in the following required fields: {', '.join(empty_fields)}",
                    "errors": empty_fields
                }), 400
            
            # Generate idea ID
            idea_id = str(uuid.uuid4())[:8]
            submitted_by = session.get('employee_id', 'unknown')
            
            # Create idea data
            summary_data = {
                "id": idea_id,
                "title": data.get("title"),
                "description": data.get("description"),
                "problem": data.get("problem"),
                "outcome": data.get("outcome"),
                "language": data.get("language"),
                "approach": data.get("approach"),
                "stack": data.get("stack"),
                "complexity": data.get("complexity"),
                "boilerplate_enabled": data.get("boilerplate_enabled", False),
                "dev_count": int(data.get("dev_count", 1)),
                "skills": data.get("skills", []),
                "timeline": data.get("timeline"),
                "manager": data.get("manager"),
                "submitted_by": submitted_by,
            }
            
            # Save to uploads
            if not save_idea_to_uploads(idea_id, summary_data):
                return jsonify({
                    "success": False,
                    "message": "❌ Failed to save idea"
                }), 500
            
            print(f"\n📋 Idea Submitted - ID: {idea_id}")
            print(f"    File: {os.path.join(UPLOADS_DIR, f'{idea_id}.json')}")
            
            # Check for similar POCs
            similar_pocs = find_similar_pocs(
                title=data.get("title", ""),
                description=data.get("description", ""),
                problem=data.get("problem", "")
            )
            
            if similar_pocs:
                # Similar POC found
                top_poc = similar_pocs[0]
                poc_id = top_poc.get('poc_id')
                similarity_score = top_poc.get('score')
                
                print(f"✅ Most Similar POC: {poc_id} (Score: {similarity_score})")
                
                matched_poc_details = get_poc_details(poc_id)
                
                if matched_poc_details:
                    print(f"📄 POC Details: {matched_poc_details.get('title')}")
                    similarity_percentage = similarity_score * 100
                    
                    return jsonify({
                        "success": True,
                        "id": idea_id,
                        "message": f"⚠️ Similar POC found: '{matched_poc_details.get('title')}' (ID: {poc_id}) with {similarity_percentage:.1f}% similarity.",
                        "data": summary_data,
                        "similar_poc_found": True,
                        "similar_poc": matched_poc_details,
                        "similarity_score": similarity_score,
                        "similarity_percentage": similarity_percentage,
                        "similar_poc_id": poc_id,
                        "notes_required": True
                    }), 200
                else:
                    print(f"❌ Failed to load POC details")
                    return jsonify({
                        "success": True,
                        "id": idea_id,
                        "message": "⚠️ Similar POC found but details unavailable.",
                        "data": summary_data,
                        "similar_poc_found": True,
                        "similar_poc_id": poc_id,
                        "notes_required": False
                    }), 200
            else:
                # No similar POC
                print(f"✅ No similar POCs found")
                
                # Save to knowledge base
                kb_success, kb_path, kb_msg = save_poc_to_knowledge_base(summary_data)
                print(kb_msg)
                
                # Ingest to Pinecone
                ingestion_success, ingestion_msg = ingest_poc_to_pinecone(summary_data)
                
                response_message = "✅ New POC submitted successfully!"
                if ingestion_success:
                    response_message += f" {ingestion_msg}"
                
                return jsonify({
                    "success": True,
                    "id": idea_id,
                    "message": response_message,
                    "data": summary_data,
                    "similar_poc_found": False,
                    "ingestion_status": ingestion_msg if not ingestion_success else None
                }), 201
        
        except Exception as e:
            print(f"⚠️ Error in submission: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
