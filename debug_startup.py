#!/usr/bin/env python3
"""
Debug startup script - Tests each import and initialization step
Run this to identify exactly where startup fails
"""

import sys
import logging

# Configure logging to see all messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("\n" + "="*80)
print("TRADE OPPORTUNITIES API - DEBUG STARTUP")
print("="*80 + "\n")

# Step 1: Check Python version
print("[STEP 1] Checking Python version...")
print(f"Python version: {sys.version}")
if sys.version_info < (3, 8):
    print("✗ Python 3.8+ required")
    sys.exit(1)
print("✓ Python version OK\n")

# Step 2: Check imports
print("[STEP 2] Testing module imports...")

try:
    print("  - Importing fastapi...")
    import fastapi
    print("    ✓ fastapi imported")
except Exception as e:
    print(f"    ✗ fastapi import failed: {e}")
    sys.exit(1)

try:
    print("  - Importing uvicorn...")
    import uvicorn
    print("    ✓ uvicorn imported")
except Exception as e:
    print(f"    ✗ uvicorn import failed: {e}")
    sys.exit(1)

try:
    print("  - Importing pydantic...")
    import pydantic
    print("    ✓ pydantic imported")
except Exception as e:
    print(f"    ✗ pydantic import failed: {e}")
    sys.exit(1)

try:
    print("  - Importing duckduckgo_search...")
    import duckduckgo_search
    print("    ✓ duckduckgo_search imported")
except Exception as e:
    print(f"    ✗ duckduckgo_search import failed: {e}")
    sys.exit(1)

try:
    print("  - Importing google.generativeai...")
    import google.generativeai
    print("    ✓ google.generativeai imported")
except Exception as e:
    print(f"    ⚠ google.generativeai import failed (optional): {e}")

print("\n✓ All required imports successful\n")

# Step 3: Test local module imports
print("[STEP 3] Testing local module imports...")

try:
    print("  - Importing auth...")
    from auth import verify_api_key
    print("    ✓ auth imported")
except Exception as e:
    print(f"    ✗ auth import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  - Importing rate_limiter...")
    from rate_limiter import RateLimiter
    print("    ✓ rate_limiter imported")
except Exception as e:
    print(f"    ✗ rate_limiter import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  - Importing session_manager...")
    from session_manager import SessionManager
    print("    ✓ session_manager imported")
except Exception as e:
    print(f"    ✗ session_manager import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  - Importing services.data_collector...")
    from services.data_collector import DataCollector
    print("    ✓ services.data_collector imported")
except Exception as e:
    print(f"    ✗ services.data_collector import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  - Importing services.ai_analyzer...")
    from services.ai_analyzer import AIAnalyzer
    print("    ✓ services.ai_analyzer imported")
except Exception as e:
    print(f"    ✗ services.ai_analyzer import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  - Importing utils.markdown_formatter...")
    from utils.markdown_formatter import MarkdownFormatter
    print("    ✓ utils.markdown_formatter imported")
except Exception as e:
    print(f"    ✗ utils.markdown_formatter import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All local modules imported successfully\n")

# Step 4: Test component initialization
print("[STEP 4] Testing component initialization...")

try:
    print("  - Initializing RateLimiter...")
    rate_limiter = RateLimiter(max_requests=5, window_seconds=60)
    print("    ✓ RateLimiter initialized")
except Exception as e:
    print(f"    ✗ RateLimiter initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  - Initializing SessionManager...")
    session_manager = SessionManager()
    print("    ✓ SessionManager initialized")
except Exception as e:
    print(f"    ✗ SessionManager initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  - Initializing DataCollector...")
    data_collector = DataCollector()
    print("    ✓ DataCollector initialized")
except Exception as e:
    print(f"    ✗ DataCollector initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  - Initializing AIAnalyzer...")
    ai_analyzer = AIAnalyzer()
    print("    ✓ AIAnalyzer initialized")
except Exception as e:
    print(f"    ✗ AIAnalyzer initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  - Initializing MarkdownFormatter...")
    markdown_formatter = MarkdownFormatter()
    print("    ✓ MarkdownFormatter initialized")
except Exception as e:
    print(f"    ✗ MarkdownFormatter initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All components initialized successfully\n")

# Step 5: Test FastAPI app creation
print("[STEP 5] Testing FastAPI app creation...")

try:
    print("  - Creating FastAPI app...")
    from fastapi import FastAPI
    from contextlib import asynccontextmanager
    
    @asynccontextmanager
    async def lifespan(app):
        logger.info("App startup")
        yield
        logger.info("App shutdown")
    
    app = FastAPI(
        title="Trade Opportunities API",
        description="Test app",
        version="1.0.0",
        lifespan=lifespan
    )
    print("    ✓ FastAPI app created")
except Exception as e:
    print(f"    ✗ FastAPI app creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("✓ ALL STARTUP CHECKS PASSED - API SHOULD START SUCCESSFULLY")
print("="*80 + "\n")

print("Next steps:")
print("1. Run: python main.py")
print("2. In another terminal, test: curl http://localhost:8001/health -H 'X-API-Key: trade-api-key-2024'")
print("\n")
