"""
Test script for Trade Opportunities API
Run this after starting the API server
"""

import requests
import json
from typing import Dict

BASE_URL = "http://localhost:8001"
API_KEY = "trade-api-key-2024"


def test_health_check():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        print("✓ PASSED")
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")


def test_invalid_api_key():
    """Test with invalid API key"""
    print("\n" + "="*60)
    print("TEST 2: Invalid API Key")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/analyze/pharmaceuticals",
            headers={"X-API-Key": "invalid-key"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 401
        print("✓ PASSED")
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")


def test_invalid_sector():
    """Test with invalid sector name"""
    print("\n" + "="*60)
    print("TEST 3: Invalid Sector Input")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/analyze/pharma123",
            headers={"X-API-Key": API_KEY}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 400
        print("✓ PASSED")
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")


def test_analyze_sector(sector: str):
    """Test sector analysis"""
    print("\n" + "="*60)
    print(f"TEST: Analyze {sector.title()} Sector")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/analyze/{sector}",
            headers={
                "X-API-Key": API_KEY,
                "Client-ID": f"test-user-{sector}"
            }
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Print first 500 characters of markdown report
            report = response.text
            print(f"\nReport Preview (first 500 chars):\n")
            print(report[:500])
            print("\n... [Report continues] ...\n")
            print("✓ PASSED")
        else:
            print(f"Response: {response.json()}")
            print("✗ FAILED")
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")


def test_rate_limiting():
    """Test rate limiting (5 requests per minute)"""
    print("\n" + "="*60)
    print("TEST: Rate Limiting (5 requests per minute)")
    print("="*60)
    
    try:
        client_id = "rate-limit-test"
        
        # Make 5 successful requests
        for i in range(5):
            response = requests.get(
                f"{BASE_URL}/analyze/technology",
                headers={
                    "X-API-Key": API_KEY,
                    "Client-ID": client_id
                }
            )
            print(f"Request {i+1}: Status {response.status_code}")
            assert response.status_code == 200
        
        # 6th request should be rate limited
        response = requests.get(
            f"{BASE_URL}/analyze/agriculture",
            headers={
                "X-API-Key": API_KEY,
                "Client-ID": client_id
            }
        )
        print(f"Request 6 (should be rate limited): Status {response.status_code}")
        
        if response.status_code == 429:
            print(f"Response: {response.json()}")
            print("✓ PASSED - Rate limiting working correctly")
        else:
            print("✗ FAILED - Rate limiting not working")
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")


def test_session_stats():
    """Test session statistics endpoint"""
    print("\n" + "="*60)
    print("TEST: Session Statistics")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/session-stats",
            headers={"X-API-Key": API_KEY}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        print("✓ PASSED")
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("TRADE OPPORTUNITIES API - TEST SUITE")
    print("="*60)
    
    try:
        # Basic tests
        test_health_check()
        test_invalid_api_key()
        test_invalid_sector()
        
        # Sector analysis tests
        test_analyze_sector("pharmaceuticals")
        test_analyze_sector("technology")
        test_analyze_sector("agriculture")
        
        # Advanced tests
        test_rate_limiting()
        test_session_stats()
        
        print("\n" + "="*60)
        print("TEST SUITE COMPLETED")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to API server")
        print("Make sure the API is running: python main.py")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")


if __name__ == "__main__":
    main()
