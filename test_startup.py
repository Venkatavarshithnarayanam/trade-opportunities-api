#!/usr/bin/env python3
"""
Simple startup test script
Tests if the API can start without errors
"""

import subprocess
import sys
import time
import requests

def test_startup():
    """Test if API starts correctly"""
    
    print("\n" + "="*80)
    print("TRADE OPPORTUNITIES API - STARTUP TEST")
    print("="*80 + "\n")
    
    print("Starting API server...")
    
    try:
        # Start the API
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        print(f"✓ Process started (PID: {process.pid})\n")
        
        # Wait for startup
        print("Waiting for API to be ready...")
        start_time = time.time()
        
        while time.time() - start_time < 60:
            try:
                response = requests.get("http://localhost:8001/health", timeout=2)
                if response.status_code == 200:
                    print("✓ API is ready!\n")
                    
                    # Test the API
                    print("Testing API endpoint...")
                    response = requests.get(
                        "http://localhost:8001/analyze/pharmaceuticals",
                        headers={
                            "X-API-Key": "trade-api-key-2024",
                            "Client-ID": "test"
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        print("✓ API endpoint works!\n")
                        print("Response preview (first 500 chars):")
                        print(response.text[:500])
                        print("\n✓ STARTUP TEST PASSED\n")
                        return True
                    else:
                        print(f"✗ API returned status {response.status_code}")
                        print(response.text[:500])
                        return False
                        
            except requests.exceptions.ConnectionError:
                elapsed = time.time() - start_time
                if elapsed % 5 < 1:
                    print(f"  Waiting... ({int(elapsed)}s)")
                time.sleep(0.5)
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                return False
        
        print("✗ API failed to start within 60 seconds")
        return False
        
    except Exception as e:
        print(f"✗ Failed to start API: {str(e)}")
        return False
    
    finally:
        try:
            process.terminate()
            process.wait(timeout=5)
            print("\n✓ API stopped gracefully")
        except:
            process.kill()
            print("\n✓ API force-terminated")


if __name__ == "__main__":
    success = test_startup()
    sys.exit(0 if success else 1)
