"""
User authentication and profile management
"""

import json
import os
from frontend.config import MANAGERS_FILE, EMPLOYEES_FILE, DEFAULT_MANAGERS, DEFAULT_EMPLOYEES
from frontend.services.file_service import load_json_file, save_json_file


def init_default_managers():
    """Initialize default manager credentials if file doesn't exist"""
    if not os.path.exists(MANAGERS_FILE):
        if save_json_file(MANAGERS_FILE, DEFAULT_MANAGERS):
            print("✅ Default managers file created")


def init_default_employees():
    """Initialize default employee credentials if file doesn't exist"""
    if not os.path.exists(EMPLOYEES_FILE):
        if save_json_file(EMPLOYEES_FILE, DEFAULT_EMPLOYEES):
            print("✅ Default employees file created")


def load_managers():
    """Load manager credentials"""
    data = load_json_file(MANAGERS_FILE)
    return data if data else {"managers": []}


def load_employees():
    """Load employee credentials"""
    data = load_json_file(EMPLOYEES_FILE)
    return data if data else {"employees": []}


def authenticate_manager(manager_id, password):
    """Authenticate manager credentials"""
    managers_data = load_managers()
    managers = managers_data.get('managers', [])
    
    for manager in managers:
        if manager.get('id') == manager_id and manager.get('password') == password:
            return {
                "id": manager.get('id'),
                "name": manager.get('name', 'Manager')
            }
    
    return None


def authenticate_employee(employee_id, password):
    """Authenticate employee credentials"""
    employees_data = load_employees()
    employees = employees_data.get('employees', [])
    
    for employee in employees:
        if employee.get('id') == employee_id and employee.get('password') == password:
            return {
                "id": employee.get('id'),
                "name": employee.get('name', 'Employee')
            }
    
    return None


def get_managers_list():
    """Get list of managers (without passwords)"""
    managers_data = load_managers()
    managers = managers_data.get('managers', [])
    
    return [
        {"id": m.get('id'), "name": m.get('name', 'Unknown')} 
        for m in managers
    ]
