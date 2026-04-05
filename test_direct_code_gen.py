#!/usr/bin/env python3
"""
Simple test to verify code generation with existing SRS file
"""

import os
import sys
import json
import time

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "code_gen"))

from code_gen.qwen import generate_code

def test_direct_code_generation():
    """Test code generation directly with existing SRS file"""
    
    print("=" * 80)
    print("TEST: Direct Code Generation from Existing SRS")
    print("=" * 80)
    
    # Use an existing SRS file
    srs_file = "/Users/aditikothiyal/Code/intel/srs_gen/srs/88ad0380_SRS.md"
    poc_id = "88ad0380"
    
    print(f"\n📋 SRS File Details:")
    print(f"   Path: {srs_file}")
    print(f"   Exists: {os.path.exists(srs_file)}")
    print(f"   POC ID: {poc_id}")
    
    if not os.path.exists(srs_file):
        print(f"\n❌ SRS file not found!")
        return
    
    # Check code file path
    code_file = f"/Users/aditikothiyal/Code/intel/code_gen/code/{poc_id}_GENERATED_CODE.py"
    print(f"\n📝 Code Generation Details:")
    print(f"   POC ID: {poc_id}")
    print(f"   Output Path: {code_file}")
    print(f"   Exists (before): {os.path.exists(code_file)}")
    
    # Remove existing code file to test fresh generation
    if os.path.exists(code_file):
        os.remove(code_file)
        print(f"   Removed existing file")
    
    # Call generate_code directly
    print(f"\n🎯 Calling generate_code()...")
    try:
        success, output_file, message = generate_code(srs_file, poc_id)
        print(f"\n✅ Result:")
        print(f"   Success: {success}")
        print(f"   Output File: {output_file}")
        print(f"   Message: {message}")
        
        if success and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"   File Size: {file_size} bytes")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_direct_code_generation()
