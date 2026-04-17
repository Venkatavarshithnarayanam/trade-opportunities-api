#!/usr/bin/env python3
"""
Trade Opportunities API - Comprehensive Validation & Testing Script
Runs the API, executes real requests, captures responses, and generates performance report
"""

import subprocess
import time
import requests
import json
import asyncio
import concurrent.futures
from datetime import datetime
from pathlib import Path
import sys
import signal
import os

# Configuration
API_URL = "http://localhost:8001"
API_KEY = "trade-api-key-2024"
STARTUP_TIMEOUT = 30
REQUEST_TIMEOUT = 60

# Test sectors
TEST_SECTORS = ["pharmaceuticals", "technology", "agriculture"]
CONCURRENT_REQUESTS = 5

# Output files
REPORT_DIR = Path("validation_reports")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
REPORT_FILE = REPORT_DIR / f"validation_report_{TIMESTAMP}.md"
LOG_FILE = REPORT_DIR / f"validation_log_{TIMESTAMP}.txt"

# Global process reference
api_process = None


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.ENDC}\n")


def print_section(text):
    """Print formatted section"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{text}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'-'*len(text)}{Colors.ENDC}")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")


def setup_report_dir():
    """Create report directory"""
    REPORT_DIR.mkdir(exist_ok=True)
    print_info(f"Report directory: {REPORT_DIR.absolute()}")


def start_api():
    """Start the FastAPI server"""
    global api_process
    
    print_section("Starting API Server")
    
    try:
        print_info("Launching FastAPI server...")
        api_process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        print_info(f"API process started (PID: {api_process.pid})")
        
        # Wait for API to be ready with better logging
        print_info("Waiting for API to be ready...")
        start_time = time.time()
        max_wait = 60  # Increased timeout
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(f"{API_URL}/health", timeout=2)
                if response.status_code == 200:
                    print_success("API is ready!")
                    time.sleep(1)  # Give it a moment to fully initialize
                    return True
            except requests.exceptions.ConnectionError:
                elapsed = time.time() - start_time
                if elapsed % 5 < 1:  # Print every 5 seconds
                    print_info(f"Still waiting... ({int(elapsed)}s elapsed)")
                time.sleep(0.5)
            except Exception as e:
                elapsed = time.time() - start_time
                if elapsed % 5 < 1:
                    print_warning(f"Connection attempt failed: {str(e)}")
                time.sleep(0.5)
        
        # If we get here, timeout occurred
        print_error(f"API failed to start within {max_wait} seconds")
        
        # Try to get any error output
        try:
            api_process.terminate()
            stdout, stderr = api_process.communicate(timeout=5)
            if stdout:
                print_error("API stdout:")
                print(stdout[-1000:])  # Last 1000 chars
            if stderr:
                print_error("API stderr:")
                print(stderr[-1000:])
        except:
            pass
        
        return False
        
    except Exception as e:
        print_error(f"Failed to start API: {str(e)}")
        return False


def stop_api():
    """Stop the FastAPI server"""
    global api_process
    
    if api_process:
        print_section("Stopping API Server")
        print_info("Sending termination signal...")
        api_process.terminate()
        
        try:
            api_process.wait(timeout=5)
            print_success("API stopped gracefully")
        except subprocess.TimeoutExpired:
            print_warning("API did not stop gracefully, forcing termination...")
            api_process.kill()
            api_process.wait()
            print_success("API force-terminated")


def test_single_request(sector, client_id):
    """Test a single API request"""
    try:
        start_time = time.time()
        
        response = requests.get(
            f"{API_URL}/analyze/{sector}",
            headers={
                "X-API-Key": API_KEY,
                "Client-ID": client_id
            },
            timeout=REQUEST_TIMEOUT
        )
        
        elapsed_time = time.time() - start_time
        
        return {
            "sector": sector,
            "client_id": client_id,
            "status_code": response.status_code,
            "elapsed_time": elapsed_time,
            "response_length": len(response.text),
            "response": response.text,
            "success": response.status_code == 200,
            "error": None
        }
    except requests.exceptions.Timeout:
        return {
            "sector": sector,
            "client_id": client_id,
            "status_code": None,
            "elapsed_time": REQUEST_TIMEOUT,
            "response_length": 0,
            "response": None,
            "success": False,
            "error": "Request timeout"
        }
    except Exception as e:
        return {
            "sector": sector,
            "client_id": client_id,
            "status_code": None,
            "elapsed_time": 0,
            "response_length": 0,
            "response": None,
            "success": False,
            "error": str(e)
        }


def test_sequential_requests():
    """Test sequential requests"""
    print_section("Sequential Request Testing")
    
    results = []
    
    for sector in TEST_SECTORS:
        print_info(f"Testing sector: {sector}")
        result = test_single_request(sector, f"sequential-{sector}")
        results.append(result)
        
        if result["success"]:
            print_success(f"{sector}: {result['elapsed_time']:.2f}s ({result['response_length']} bytes)")
        else:
            print_error(f"{sector}: {result['error']}")
        
        time.sleep(1)  # Small delay between requests
    
    return results


def test_concurrent_requests():
    """Test concurrent requests"""
    print_section("Concurrent Request Testing")
    
    print_info(f"Launching {CONCURRENT_REQUESTS} concurrent requests...")
    
    results = []
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        futures = []
        
        for i in range(CONCURRENT_REQUESTS):
            sector = TEST_SECTORS[i % len(TEST_SECTORS)]
            future = executor.submit(test_single_request, sector, f"concurrent-{i}")
            futures.append(future)
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            result = future.result()
            results.append(result)
            
            if result["success"]:
                print_success(f"Request {i+1}: {result['sector']} - {result['elapsed_time']:.2f}s")
            else:
                print_error(f"Request {i+1}: {result['error']}")
    
    total_time = time.time() - start_time
    print_info(f"Total concurrent time: {total_time:.2f}s")
    
    return results, total_time


def extract_gemini_status(response_text):
    """Extract Gemini API status from response"""
    if not response_text:
        return "FAILED", "No response"
    
    # Check for Gemini-specific indicators in markdown
    if "Market Analysis:" in response_text:
        # Check if it looks like real Gemini output vs fallback
        if len(response_text) > 2000:  # Real Gemini responses tend to be longer
            return "SUCCESS", "Gemini API returned structured response"
        else:
            return "FALLBACK", "Using rule-based analysis"
    
    return "UNKNOWN", "Could not determine analysis source"


def generate_report(sequential_results, concurrent_results, concurrent_time):
    """Generate comprehensive validation report"""
    
    report = []
    report.append("# Trade Opportunities API - Validation Report\n")
    report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**API URL**: {API_URL}\n")
    report.append(f"**Test Sectors**: {', '.join(TEST_SECTORS)}\n\n")
    
    # Sequential Results
    report.append("## Sequential Request Testing\n\n")
    report.append("| Sector | Status | Time (s) | Size (bytes) | Gemini Status |\n")
    report.append("|--------|--------|----------|-------------|---------------|\n")
    
    seq_success = 0
    seq_total_time = 0
    
    for result in sequential_results:
        status = "✓ Success" if result["success"] else "✗ Failed"
        gemini_status, gemini_msg = extract_gemini_status(result["response"])
        
        report.append(
            f"| {result['sector']} | {status} | {result['elapsed_time']:.2f} | "
            f"{result['response_length']} | {gemini_status} |\n"
        )
        
        if result["success"]:
            seq_success += 1
            seq_total_time += result["elapsed_time"]
    
    report.append(f"\n**Sequential Summary**: {seq_success}/{len(sequential_results)} successful\n")
    report.append(f"**Average Response Time**: {seq_total_time/len(sequential_results):.2f}s\n\n")
    
    # Concurrent Results
    report.append("## Concurrent Request Testing\n\n")
    report.append(f"**Concurrent Requests**: {CONCURRENT_REQUESTS}\n")
    report.append(f"**Total Time**: {concurrent_time:.2f}s\n\n")
    
    report.append("| Request # | Sector | Status | Time (s) | Size (bytes) | Gemini Status |\n")
    report.append("|-----------|--------|--------|----------|-------------|---------------|\n")
    
    conc_success = 0
    conc_times = []
    
    for i, result in enumerate(concurrent_results, 1):
        status = "✓ Success" if result["success"] else "✗ Failed"
        gemini_status, gemini_msg = extract_gemini_status(result["response"])
        
        report.append(
            f"| {i} | {result['sector']} | {status} | {result['elapsed_time']:.2f} | "
            f"{result['response_length']} | {gemini_status} |\n"
        )
        
        if result["success"]:
            conc_success += 1
            conc_times.append(result["elapsed_time"])
    
    report.append(f"\n**Concurrent Summary**: {conc_success}/{len(concurrent_results)} successful\n")
    if conc_times:
        report.append(f"**Average Response Time**: {sum(conc_times)/len(conc_times):.2f}s\n")
        report.append(f"**Min Response Time**: {min(conc_times):.2f}s\n")
        report.append(f"**Max Response Time**: {max(conc_times):.2f}s\n\n")
    
    # Performance Metrics
    report.append("## Performance Metrics\n\n")
    
    total_requests = len(sequential_results) + len(concurrent_results)
    total_success = seq_success + conc_success
    success_rate = (total_success / total_requests * 100) if total_requests > 0 else 0
    
    report.append(f"**Total Requests**: {total_requests}\n")
    report.append(f"**Successful Requests**: {total_success}\n")
    report.append(f"**Success Rate**: {success_rate:.1f}%\n")
    report.append(f"**Failed Requests**: {total_requests - total_success}\n\n")
    
    # Gemini API Status
    report.append("## Gemini API Status\n\n")
    
    gemini_success = 0
    gemini_fallback = 0
    
    for result in sequential_results + concurrent_results:
        if result["success"]:
            status, msg = extract_gemini_status(result["response"])
            if status == "SUCCESS":
                gemini_success += 1
            elif status == "FALLBACK":
                gemini_fallback += 1
    
    report.append(f"**Gemini API Success**: {gemini_success} requests\n")
    report.append(f"**Fallback Analysis**: {gemini_fallback} requests\n")
    report.append(f"**Gemini Success Rate**: {(gemini_success/(gemini_success+gemini_fallback)*100 if (gemini_success+gemini_fallback) > 0 else 0):.1f}%\n\n")
    
    # Sample Response
    if sequential_results and sequential_results[0]["success"]:
        report.append("## Sample API Response\n\n")
        report.append("### Request\n")
        report.append(f"```\nGET /analyze/{sequential_results[0]['sector']}\n")
        report.append(f"X-API-Key: {API_KEY}\n")
        report.append(f"Client-ID: {sequential_results[0]['client_id']}\n```\n\n")
        
        report.append("### Response (First 1000 characters)\n")
        report.append("```markdown\n")
        report.append(sequential_results[0]["response"][:1000])
        report.append("\n...\n```\n\n")
    
    # Recommendations
    report.append("## Recommendations\n\n")
    
    if success_rate == 100:
        report.append("✓ **All tests passed successfully**\n")
        report.append("✓ **API is ready for production deployment**\n")
    elif success_rate >= 80:
        report.append("⚠ **Most tests passed, but some failures detected**\n")
        report.append("⚠ **Investigate failures before production deployment**\n")
    else:
        report.append("✗ **Significant failures detected**\n")
        report.append("✗ **Do not deploy to production until issues are resolved**\n")
    
    report.append("\n### Next Steps\n\n")
    report.append("1. Review this report for any failures\n")
    report.append("2. Check API logs for error details\n")
    report.append("3. Verify Gemini API key is set correctly\n")
    report.append("4. Test with different sectors if needed\n")
    report.append("5. Deploy to Render or Railway when ready\n\n")
    
    report.append("---\n\n")
    report.append(f"*Report generated by validation script*\n")
    
    return "".join(report)


def save_report(report_content):
    """Save report to file"""
    with open(REPORT_FILE, "w") as f:
        f.write(report_content)
    print_success(f"Report saved to: {REPORT_FILE}")


def main():
    """Main validation flow"""
    
    print_header("Trade Opportunities API - Validation & Testing")
    
    setup_report_dir()
    
    # Start API
    if not start_api():
        print_error("Failed to start API. Exiting.")
        return False
    
    try:
        # Run tests
        print_header("Running Validation Tests")
        
        # Sequential tests
        sequential_results = test_sequential_requests()
        
        time.sleep(2)  # Pause between test phases
        
        # Concurrent tests
        concurrent_results, concurrent_time = test_concurrent_requests()
        
        # Generate report
        print_section("Generating Report")
        report = generate_report(sequential_results, concurrent_results, concurrent_time)
        save_report(report)
        
        # Print summary
        print_section("Validation Summary")
        
        total_requests = len(sequential_results) + len(concurrent_results)
        total_success = sum(1 for r in sequential_results + concurrent_results if r["success"])
        success_rate = (total_success / total_requests * 100) if total_requests > 0 else 0
        
        print_info(f"Total Requests: {total_requests}")
        print_info(f"Successful: {total_success}")
        print_info(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate == 100:
            print_success("All tests passed! API is ready for deployment.")
            return True
        elif success_rate >= 80:
            print_warning("Most tests passed. Review failures before deployment.")
            return True
        else:
            print_error("Significant failures detected. Do not deploy.")
            return False
        
    finally:
        stop_api()


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_warning("\nValidation interrupted by user")
        stop_api()
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        stop_api()
        sys.exit(1)
