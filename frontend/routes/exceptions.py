"""
Exception request handling and exception list routes
"""

import uuid
import json
import os
from flask import request, jsonify
from datetime import datetime

from frontend.config import EXCEPTION_DIR, UPLOADS_DIR, KNOWLEDGE_BASE_PATH
from frontend.services.file_service import save_exception, get_exception, list_exceptions, get_idea_from_uploads, save_poc_to_knowledge_base
from frontend.services.poc_service import get_poc_details, process_approved_poc


def register_exception_routes(app):
    """Register all exception-related routes"""
    
    @app.route('/api/request-exception', methods=['POST'])
    def request_exception():
        """Handle exception request when user wants to proceed with similar idea"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ["idea_id", "manager", "similar_poc_id", "similarity_score"]
            missing_fields = [f for f in required_fields if not data.get(f)]
            
            notes = data.get("notes", "").strip()
            if not notes:
                missing_fields.append("Notes")
            
            if missing_fields:
                return jsonify({
                    "success": False,
                    "message": f"Missing required fields: {', '.join(missing_fields)}"
                }), 400
            
            # Get idea details
            idea_id = data.get("idea_id")
            idea_data = get_idea_from_uploads(idea_id)
            idea_title = idea_data.get("title", "N/A") if idea_data else "N/A"
            submitted_by = idea_data.get("submitted_by", "N/A") if idea_data else "N/A"
            
            # Generate exception ID
            exception_id = str(uuid.uuid4())[:8]
            
            # Create exception data
            exception_data = {
                "id": exception_id,
                "idea_id": idea_id,
                "title": idea_title,
                "submitted_by": submitted_by,
                "manager": data.get("manager"),
                "similar_poc_id": data.get("similar_poc_id"),
                "similarity_score": float(data.get("similarity_score")),
                "similarity_percentage": float(data.get("similarity_score")) * 100,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "notes": notes
            }
            
            # Save exception
            if not save_exception(exception_id, exception_data):
                return jsonify({
                    "success": False,
                    "message": "❌ Failed to save exception request"
                }), 500
            
            print(f"\n📋 Exception Request Created: {exception_id}")
            print(f"   Manager: {data.get('manager')}")
            
            return jsonify({
                "success": True,
                "exception_id": exception_id,
                "message": f"✅ Exception request submitted (ID: {exception_id})",
                "data": exception_data
            }), 201
        
        except Exception as e:
            print(f"⚠️ Error in exception request: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    @app.route('/api/get-exception-status', methods=['GET'])
    def get_exception_status():
        """Retrieve exception request status by exception ID with similar POC details"""
        try:
            exception_id = request.args.get('exception_id', '').strip()
            
            if not exception_id:
                return jsonify({
                    "success": False,
                    "message": "Exception ID is required"
                }), 400
            
            exception_data = get_exception(exception_id)
            
            if not exception_data:
                return jsonify({
                    "success": False,
                    "message": f"❌ Exception ID '{exception_id}' not found."
                }), 404
            
            # Fetch similar POC details if available
            similar_pocs = []
            similar_poc_id = exception_data.get("similar_poc_id")
            
            if similar_poc_id:
                poc_details = get_poc_details(similar_poc_id)
                if poc_details:
                    similar_pocs.append({
                        "poc_id": similar_poc_id,
                        "poc_data": poc_details
                    })
            
            return jsonify({
                "success": True,
                "message": "✅ Exception request found",
                "data": exception_data,
                "similar_pocs": similar_pocs
            }), 200
        
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    @app.route('/api/exceptions', methods=['GET'])
    def get_exceptions():
        """Get list of all exceptions"""
        try:
            exceptions = list_exceptions()
            
            # Sort by creation date (newest first)
            exceptions.sort(
                key=lambda x: x.get("created_at", ""),
                reverse=True
            )
            
            return jsonify({
                "success": True,
                "data": exceptions
            }), 200
        
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    @app.route('/api/exception/<exception_id>', methods=['GET'])
    def get_exception_detail(exception_id):
        """Get full details of a specific exception including similar POC details"""
        try:
            exception_data = get_exception(exception_id)
            
            if not exception_data:
                return jsonify({
                    "success": False,
                    "message": f"Exception '{exception_id}' not found"
                }), 404
            
            # Fetch similar POC details if available
            similar_pocs = []
            similar_poc_id = exception_data.get("similar_poc_id")
            
            if similar_poc_id:
                poc_details = get_poc_details(similar_poc_id)
                if poc_details:
                    similar_pocs.append({
                        "poc_id": similar_poc_id,
                        "poc_data": poc_details
                    })
            
            return jsonify({
                "success": True,
                "data": {
                    "exception": exception_data,
                    "similar_pocs": similar_pocs
                }
            }), 200
        
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    @app.route('/api/exception/<exception_id>', methods=['PUT'])
    def update_exception(exception_id):
        """Update exception status (especially for approval and ingestion)"""
        try:
            exception_data = get_exception(exception_id)
            
            if not exception_data:
                return jsonify({
                    "success": False,
                    "message": f"Exception '{exception_id}' not found"
                }), 404
            
            # Get update data
            update_data = request.get_json()
            new_status = update_data.get('status')
            
            print(f"\n📋 Updating exception {exception_id}")
            print(f"   Status: {new_status}")
            
            # Update status and notes
            if 'status' in update_data:
                exception_data['status'] = update_data['status']
            
            if 'notes' in update_data:
                exception_data['notes'] = update_data['notes']
            
            exception_data['updated_at'] = datetime.utcnow().isoformat()
            
            # If approved, process the POC
            ingestion_status = None
            if new_status and new_status.lower() == "approved":
                print(f"\n⚙️ Exception approved - Processing POC...")
                idea_id = exception_data.get("idea_id")
                
                if idea_id:
                    success, msg = process_approved_poc(idea_id)
                    ingestion_status = msg
                    print(ingestion_status)
                else:
                    ingestion_status = "⚠️ No idea_id found"
            
            # Save updated exception
            if not save_exception(exception_id, exception_data):
                return jsonify({
                    "success": False,
                    "message": "❌ Failed to save exception update"
                }), 500
            
            response_message = "✅ Exception updated successfully"
            if ingestion_status:
                response_message += f" | {ingestion_status}"
            
            return jsonify({
                "success": True,
                "message": response_message,
                "data": exception_data,
                "ingestion_status": ingestion_status
            }), 200
        
        except Exception as e:
            print(f"⚠️ Error updating exception: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
