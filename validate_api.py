#!/usr/bin/env python3
"""
API Validation Script
Starts API on explicit port, waits for it to be ready, then runs tests
"""

import subprocess
import time
import requests
import sys
import os
import signal
from pathlib import Path

# Configuration
API_HOST = "localhost"
API_KEY = "trade-api-key-2024"
API_PORT = 8001  # Use explicit port to avoid conflicts
STARTUP_TIMEOUT = 60
REQUEST_TIMEOUT = 30

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
ENDC = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*80}{ENDC}")
    print(f"{BLUE}{text.center(80)}{ENDC}")
    print(f"{BLUE}{'='*80}{ENDC}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{ENDC}")

def print_error(text):
    print(f"{RED}✗ {text}{ENDC}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{ENDC}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{ENDC}")

def start_api():
    """Start the API server on explicit port"""
    print_header("STARTING API SERVER")
    
    print_info(f"Launching API with: PORT={API_PORT} python main.py")
    
    try:
        # Start the process with explicit port via environment variable
        env = os.environ.copy()
        env["PORT"] = str(API_PORT)
        
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            env=env
        )
        
        print_info(f"Process started, waiting for API on port {API_PORT}...")
        
        # Wait for API to be ready
        start_time = time.time()
        
        while time.time() - start_time < STARTUP_TIMEOUT:
            try:
                response = requests.get(
                    f"http://{API_HOST}:{API_PORT}/health",
                    headers={"X-API-Key": API_KEY},
                    timeout=1
                )
                if response.status_code == 200:
                    print_success(f"API is ready on port {API_PORT}")
                    return process, API_PORT
            except requests.exceptions.ConnectionError:
                pass
            except Exception:
                pass
            
            elapsed = time.time() - start_time
            print_info(f"Waiting for API... ({elapsed:.1f}s)")
            time.sleep(1)
        
        print_error(f"API failed to start within {STARTUP_TIMEOUT} seconds")
        process.terminate()
        return None, None
        
    except Exception as e:
        print_error(f"Failed to start API: {e}")
        return None, None

def find_available_port(start_port=8000, max_attempts=10):
    """Find an available port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(("0.0.0.0", port))
                sock.close()
                return port
        except OSError:
            continue
    return None

def test_health_check(port):
    """Test health check endpoint"""
    print_header("TESTING HEALTH CHECK")
    
    try:
        response = requests.get(
            f"http://{API_HOST}:{port}/health",
            headers={"X-API-Key": API_KEY},
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            print_success("Health check passed")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_analysis(port, sector):
    """Test analysis endpoint"""
    print_header(f"TESTING ANALYSIS: {sector.upper()}")
    
    try:
        response = requests.get(
            f"http://{API_HOST}:{port}/analyze/{sector}",
            headers={
                "X-API-Key": API_KEY,
                "Client-ID": "test-user"
            },
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            print_success(f"Analysis for {sector} succeeded")
            report = response.text
            print_info(f"Report length: {len(report)} characters")
            
            # Check if it's markdown
            if "# Market Analysis" in report or "## " in report:
                print_success("Report is properly formatted markdown")
            else:
                print_warning("Report might not be properly formatted")
            
            # Show first 500 chars
            print_info("Report preview:")
            print(report[:500] + "...\n")
            return True
        else:
            print_error(f"Analysis failed with status {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Analysis error: {e}")
        return False

def test_invalid_key(port):
    """Test with invalid API key"""
    print_header("TESTING INVALID API KEY")
    
    try:
        response = requests.get(
            f"http://{API_HOST}:{port}/analyze/technology",
            headers={"X-API-Key": "invalid-key"},
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 401:
            print_success("Invalid API key correctly rejected")
            return True
        else:
            print_error(f"Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Invalid key test error: {e}")
        return False

def test_invalid_sector(port):
    """Test with invalid sector"""
    print_header("TESTING INVALID SECTOR")
    
    try:
        response = requests.get(
            f"http://{API_HOST}:{port}/analyze/sector123",
            headers={"X-API-Key": API_KEY},
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 400:
            print_success("Invalid sector correctly rejected")
            return True
        else:
            print_warning(f"Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Invalid sector test error: {e}")
        return False

def main():
    """Main validation flow"""
    print_header("TRADE OPPORTUNITIES API - VALIDATION SUITE")
    
    # Start API
    api_process, port = start_api()
    if not api_process or not port:
        print_error("Failed to start API")
        sys.exit(1)
    
    print_success(f"API running on port {port}")
    
    try:
        # Run tests
        results = {
            "Health Check": test_health_check(port),
            "Invalid API Key": test_invalid_key(port),
            "Invalid Sector": test_invalid_sector(port),
            "Pharmaceuticals": test_analysis(port, "pharmaceuticals"),
            "Technology": test_analysis(port, "technology"),
            "Agriculture": test_analysis(port, "agriculture"),
        }
        
        # Summary
        print_header("VALIDATION SUMMARY")
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for test_name, result in results.items():
            status = f"{GREEN}PASS{ENDC}" if result else f"{RED}FAIL{ENDC}"
            print(f"  {test_name}: {status}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        print(f"API running on: http://localhost:{port}")
        
        if passed == total:
            print_success("All tests passed! API is ready for deployment.")
            return 0
        else:
            print_error(f"{total - passed} test(s) failed")
            return 1
            
    except KeyboardInterrupt:
        print_warning("\nValidation interrupted by user")
        return 1
    finally:
        # Stop API
        print_info("Stopping API...")
        api_process.terminate()
        try:
            api_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api_process.kill()
        print_success("API stopped")

if __name__ == "__main__":
    sys.exit(main())
