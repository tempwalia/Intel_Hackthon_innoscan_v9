import json
import os
import sys
sys.path.insert(0, '/Users/aditikothiyal/Code/intel')

# Check if managers.json exists
managers_path = "/Users/aditikothiyal/Code/intel/frontend/managers.json"
print(f"Managers file exists: {os.path.exists(managers_path)}")

if os.path.exists(managers_path):
    with open(managers_path, 'r') as f:
        data = json.load(f)
    print(f"Current managers.json content:")
    print(json.dumps(data, indent=2))
else:
    print("File doesn't exist - will be created on first app init")
    
# Now test the full flow
from frontend.landing_page import create_app
from frontend.services.user_service import authenticate_manager, load_managers

print("\n--- After app creation ---")
print(f"Managers file now exists: {os.path.exists(managers_path)}")
if os.path.exists(managers_path):
    with open(managers_path, 'r') as f:
        data = json.load(f)
    print(f"Managers.json content:")
    print(json.dumps(data, indent=2))

# Test authentication
print("\n--- Testing authentication ---")
managers = load_managers()
print(f"Loaded managers: {managers}")

result = authenticate_manager("manager1", "password123")
print(f"Auth result for manager1/password123: {result}")
