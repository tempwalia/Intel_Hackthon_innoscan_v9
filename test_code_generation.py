#!/usr/bin/env python3
"""
Test script to verify code generation after SRS generation
"""

import os
import sys
import json
import time

# Setup paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from frontend.services.poc_service import ingest_poc_to_pinecone

def test_code_generation():
    """Test code generation with boilerplate enabled"""
    
    print("=" * 80)
    print("TEST: Code Generation After SRS")
    print("=" * 80)
    
    # Load a POC with boilerplate enabled
    poc_file = "/Users/aditikothiyal/Code/intel/frontend/uploads/50a1cc24.json"
    
    with open(poc_file, 'r', encoding='utf-8') as f:
        poc_data = json.load(f)
    
    print(f"\n📋 POC Details:")
    print(f"   ID: {poc_data.get('id')}")
    print(f"   Title: {poc_data.get('title')}")
    print(f"   Boilerplate Enabled: {poc_data.get('boilerplate_enabled')}")
    
    # Ingest to Pinecone (this triggers SRS generation, which now triggers code generation)
    print(f"\n🎯 Starting ingestion pipeline...")
    success, message = ingest_poc_to_pinecone(poc_data)
    print(f"   {message}")
    
    if success:
        print(f"\n⏳ Waiting for background tasks to complete (SRS + Code Generation)...")
        # Wait for background threads to complete
        for i in range(120):  # Wait up to 120 seconds
            time.sleep(1)
            
            # Check if SRS file exists
            srs_file = f"/Users/aditikothiyal/Code/intel/srs_gen/srs/{poc_data.get('id')}_SRS.md"
            code_file = f"/Users/aditikothiyal/Code/intel/code_gen/code/{poc_data.get('id')}_GENERATED_CODE.py"
            
            srs_exists = os.path.exists(srs_file)
            code_exists = os.path.exists(code_file)
            
            if i % 10 == 0:  # Print status every 10 seconds
                print(f"   [{i}s] SRS: {'✓' if srs_exists else '✗'}, Code: {'✓' if code_exists else '✗'}")
            
            if srs_exists and code_exists:
                print(f"\n✅ SUCCESS! Both files generated:")
                print(f"   ✓ SRS: {srs_file}")
                print(f"   ✓ Code: {code_file}")
                
                # Check file sizes
                srs_size = os.path.getsize(srs_file)
                code_size = os.path.getsize(code_file)
                print(f"\n📊 File Sizes:")
                print(f"   SRS: {srs_size} bytes")
                print(f"   Code: {code_size} bytes")
                break
            elif i == 119:
                print(f"\n⚠️  Timeout waiting for files (2 minutes)")
                if srs_exists:
                    print(f"   ✓ SRS: {srs_file}")
                else:
                    print(f"   ✗ SRS not found: {srs_file}")
                if code_exists:
                    print(f"   ✓ Code: {code_file}")
                else:
                    print(f"   ✗ Code not found: {code_file}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_code_generation()

