"""
Authentication routes (login, logout, profiles)
"""

from flask import request, jsonify, session
from frontend.services.user_service import (
    authenticate_manager, authenticate_employee, get_managers_list
)


def register_auth_routes(app):
    """Register all authentication routes"""
    
    @app.route('/api/manager-login', methods=['POST'])
    def manager_login():
        """Authenticate manager and create session"""
        try:
            data = request.get_json()
            manager_id = data.get('manager_id', '').strip()
            password = data.get('password', '').strip()
            
            if not manager_id or not password:
                return jsonify({
                    "success": False,
                    "message": "Manager ID and password are required"
                }), 400
            
            manager = authenticate_manager(manager_id, password)
            if manager:
                session.permanent = True
                session['manager_id'] = manager['id']
                session['manager_name'] = manager['name']
                print(f"✅ Manager '{manager_id}' logged in")
                return jsonify({
                    "success": True,
                    "message": "Login successful"
                }), 200
            else:
                print(f"❌ Failed login attempt for manager_id: {manager_id}")
                return jsonify({
                    "success": False,
                    "message": "Invalid manager ID or password"
                }), 401
        
        except Exception as e:
            print(f"⚠️ Error in manager login: {e}")
            return jsonify({
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }), 500
    
    @app.route('/api/employee-login', methods=['POST'])
    def employee_login():
        """Authenticate employee and create session"""
        try:
            data = request.get_json()
            employee_id = data.get('employee_id', '').strip()
            password = data.get('password', '').strip()
            
            if not employee_id or not password:
                return jsonify({
                    "success": False,
                    "message": "Employee ID and password are required"
                }), 400
            
            employee = authenticate_employee(employee_id, password)
            if employee:
                session.permanent = True
                session['employee_id'] = employee['id']
                session['employee_name'] = employee['name']
                print(f"✅ Employee '{employee_id}' logged in")
                return jsonify({
                    "success": True,
                    "message": "Login successful"
                }), 200
            else:
                print(f"❌ Failed login attempt for employee_id: {employee_id}")
                return jsonify({
                    "success": False,
                    "message": "Invalid employee ID or password"
                }), 401
        
        except Exception as e:
            print(f"⚠️ Error in employee login: {e}")
            return jsonify({
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }), 500
    
    @app.route('/api/logout', methods=['POST'])
    def logout():
        """Logout and clear session"""
        user_id = session.get('manager_id') or session.get('employee_id')
        session.clear()
        print(f"✅ User logged out")
        return jsonify({
            "success": True,
            "message": "Logged out successfully"
        }), 200
    
    @app.route('/api/manager-profile', methods=['GET'])
    def manager_profile():
        """Get current logged-in manager's profile"""
        try:
            if 'manager_id' not in session:
                return jsonify({
                    "success": False,
                    "message": "Not logged in"
                }), 401
            
            return jsonify({
                "success": True,
                "data": {
                    "manager_id": session.get('manager_id'),
                    "manager_name": session.get('manager_name', 'Manager')
                }
            }), 200
        
        except Exception as e:
            print(f"⚠️ Error getting manager profile: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    @app.route('/api/employee-profile', methods=['GET'])
    def employee_profile():
        """Get current logged-in employee's profile"""
        try:
            if 'employee_id' not in session:
                return jsonify({
                    "success": False,
                    "message": "Not logged in"
                }), 401
            
            return jsonify({
                "success": True,
                "data": {
                    "employee_id": session.get('employee_id'),
                    "employee_name": session.get('employee_name', 'Employee')
                }
            }), 200
        
        except Exception as e:
            print(f"⚠️ Error getting employee profile: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    @app.route('/api/managers', methods=['GET'])
    def get_managers():
        """Get list of all managers for dropdown selection"""
        try:
            manager_list = get_managers_list()
            return jsonify({
                "success": True,
                "data": manager_list
            }), 200
        except Exception as e:
            print(f"⚠️ Error getting managers: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
