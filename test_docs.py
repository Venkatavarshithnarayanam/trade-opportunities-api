#!/usr/bin/env python3
"""
Quick test to verify documentation endpoints are accessible
"""

import requests
import sys

API_HOST = "localhost"
API_PORT = 8001
API_KEY = "trade-api-key-2024"

def test_docs():
    """Test documentation endpoints"""
    
    print("\n" + "="*80)
    print("Testing Documentation Endpoints")
    print("="*80 + "\n")
    
    # Test /docs
    print("1. Testing /docs (Swagger UI)...")
    try:
        response = requests.get(f"http://{API_HOST}:{API_PORT}/docs", timeout=5)
        if response.status_code == 200:
            print(f"   ✓ /docs is accessible (status: {response.status_code})")
            if "swagger" in response.text.lower():
                print("   ✓ Swagger UI content detected")
            else:
                print("   ⚠ Response received but Swagger UI content not found")
        else:
            print(f"   ✗ /docs returned status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error accessing /docs: {e}")
    
    # Test /redoc
    print("\n2. Testing /redoc (ReDoc)...")
    try:
        response = requests.get(f"http://{API_HOST}:{API_PORT}/redoc", timeout=5)
        if response.status_code == 200:
            print(f"   ✓ /redoc is accessible (status: {response.status_code})")
            if "redoc" in response.text.lower():
                print("   ✓ ReDoc content detected")
        else:
            print(f"   ✗ /redoc returned status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error accessing /redoc: {e}")
    
    # Test /openapi.json
    print("\n3. Testing /openapi.json (OpenAPI Schema)...")
    try:
        response = requests.get(f"http://{API_HOST}:{API_PORT}/openapi.json", timeout=5)
        if response.status_code == 200:
            print(f"   ✓ /openapi.json is accessible (status: {response.status_code})")
            data = response.json()
            if "openapi" in data:
                print(f"   ✓ Valid OpenAPI schema (version: {data.get('info', {}).get('version')})")
            if "paths" in data:
                print(f"   ✓ Found {len(data['paths'])} API endpoints")
        else:
            print(f"   ✗ /openapi.json returned status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error accessing /openapi.json: {e}")
    
    # Test health endpoint
    print("\n4. Testing /health (API Health Check)...")
    try:
        response = requests.get(
            f"http://{API_HOST}:{API_PORT}/health",
            headers={"X-API-Key": API_KEY},
            timeout=5
        )
        if response.status_code == 200:
            print(f"   ✓ /health is accessible (status: {response.status_code})")
            data = response.json()
            print(f"   ✓ Response: {data}")
        else:
            print(f"   ✗ /health returned status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error accessing /health: {e}")
    
    print("\n" + "="*80)
    print("Documentation Endpoints Test Complete")
    print("="*80 + "\n")
    print("Access the API documentation at:")
    print(f"  • Swagger UI: http://{API_HOST}:{API_PORT}/docs")
    print(f"  • ReDoc: http://{API_HOST}:{API_PORT}/redoc")
    print(f"  • OpenAPI Schema: http://{API_HOST}:{API_PORT}/openapi.json")
    print()

if __name__ == "__main__":
    test_docs()
