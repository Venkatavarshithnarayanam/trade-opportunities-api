#!/usr/bin/env python3
"""
Verify setup script - checks if everything is configured correctly
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("\n1. Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor} (Need 3.8+)")
        return False

def check_files():
    """Check if all required files exist"""
    print("\n2. Checking required files...")
    
    required_files = [
        "main.py",
        "auth.py",
        "rate_limiter.py",
        "session_manager.py",
        "requirements.txt",
        "services/__init__.py",
        "services/data_collector.py",
        "services/ai_analyzer.py",
        "utils/__init__.py",
        "utils/markdown_formatter.py",
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} (MISSING)")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check if all dependencies are installed"""
    print("\n3. Checking dependencies...")
    
    required_packages = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "pydantic": "Pydantic",
        "google.generativeai": "Google Generative AI",
        "duckduckgo_search": "DuckDuckGo Search",
        "httpx": "HTTPX",
    }
    
    all_installed = True
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"   ✓ {name}")
        except ImportError:
            print(f"   ✗ {name} (NOT INSTALLED)")
            all_installed = False
    
    return all_installed

def check_imports():
    """Check if all modules can be imported"""
    print("\n4. Checking module imports...")
    
    modules = [
        ("auth", "verify_api_key"),
        ("rate_limiter", "RateLimiter"),
        ("session_manager", "SessionManager"),
        ("services.data_collector", "DataCollector"),
        ("services.ai_analyzer", "AIAnalyzer"),
        ("utils.markdown_formatter", "MarkdownFormatter"),
    ]
    
    all_importable = True
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"   ✓ {module_name}.{class_name}")
        except Exception as e:
            print(f"   ✗ {module_name}.{class_name} ({str(e)})")
            all_importable = False
    
    return all_importable

def check_port():
    """Check if port 8001 is available"""
    print("\n5. Checking port 8001...")
    
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8001))
    sock.close()
    
    if result != 0:
        print("   ✓ Port 8001 is available")
        return True
    else:
        print("   ✗ Port 8001 is already in use")
        print("   → Kill the process: lsof -i :8001 | grep LISTEN | awk '{print $2}' | xargs kill -9")
        return False

def check_environment():
    """Check environment variables"""
    print("\n6. Checking environment variables...")
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        print(f"   ✓ GEMINI_API_KEY is set")
    else:
        print(f"   ⚠ GEMINI_API_KEY is not set (optional, will use fallback)")
    
    valid_keys = os.getenv("VALID_API_KEYS")
    if valid_keys:
        print(f"   ✓ VALID_API_KEYS is set")
    else:
        print(f"   ⚠ VALID_API_KEYS is not set (will use default)")
    
    return True

def main():
    """Run all checks"""
    print("\n" + "="*80)
    print("TRADE OPPORTUNITIES API - SETUP VERIFICATION")
    print("="*80)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Files", check_files),
        ("Dependencies", check_dependencies),
        ("Module Imports", check_imports),
        ("Port Availability", check_port),
        ("Environment Variables", check_environment),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Error during {name} check: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False
    
    print("="*80)
    
    if all_passed:
        print("\n✓ All checks passed! You're ready to run the API.\n")
        print("Next steps:")
        print("  1. Run: python main.py")
        print("  2. Or run: python test_startup.py")
        print("  3. Or run: python run_validation.py")
        return 0
    else:
        print("\n✗ Some checks failed. Please fix the issues above.\n")
        print("For help, see: STARTUP_DEBUG.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
