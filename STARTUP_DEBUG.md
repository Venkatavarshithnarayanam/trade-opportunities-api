# API Startup Debugging Guide

## Issue: API Failed to Start Within 30 Seconds

This guide helps you debug and fix API startup issues.

---

## Step 1: Test Direct Startup

First, test if the API can start directly without the validation script:

```bash
python main.py
```

**Expected output:**
```
================================================================================
Trade Opportunities API - Initializing
================================================================================
Importing auth module...
✓ Auth module imported successfully
Importing rate_limiter module...
✓ Rate limiter module imported successfully
Importing session_manager module...
✓ Session manager module imported successfully
Importing data_collector service...
✓ Data collector service imported successfully
Importing ai_analyzer service...
✓ AI analyzer service imported successfully
Importing markdown_formatter utility...
✓ Markdown formatter utility imported successfully
================================================================================
All components initialized successfully!
================================================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**If you see errors**, note them and proceed to Step 2.

---

## Step 2: Check for Import Errors

### Check each module individually:

```bash
# Test auth module
python -c "from auth import verify_api_key; print('✓ auth module OK')"

# Test rate_limiter module
python -c "from rate_limiter import RateLimiter; print('✓ rate_limiter module OK')"

# Test session_manager module
python -c "from session_manager import SessionManager; print('✓ session_manager module OK')"

# Test data_collector service
python -c "from services.data_collector import DataCollector; print('✓ data_collector service OK')"

# Test ai_analyzer service
python -c "from services.ai_analyzer import AIAnalyzer; print('✓ ai_analyzer service OK')"

# Test markdown_formatter utility
python -c "from utils.markdown_formatter import MarkdownFormatter; print('✓ markdown_formatter utility OK')"
```

**If any of these fail**, the error message will tell you what's wrong.

---

## Step 3: Check Dependencies

Verify all required packages are installed:

```bash
pip list | grep -E "fastapi|uvicorn|pydantic|google-generativeai|duckduckgo-search|httpx"
```

**Expected output:**
```
fastapi                    0.104.1
google-generativeai        0.3.0
httpx                      0.25.2
pydantic                   2.5.0
pydantic-settings          2.1.0
python-dotenv              1.0.0
duckduckgo-search          3.9.10
uvicorn                    0.24.0
```

**If any are missing**, install them:

```bash
pip install -r requirements.txt --force-reinstall
```

---

## Step 4: Check Port Availability

Verify port 8000 is not in use:

```bash
# Check if port 8000 is in use
lsof -i :8000

# If it shows a process, kill it
kill -9 <PID>

# Or use a different port
python main.py --port 8001
```

---

## Step 5: Check Environment Variables

Verify environment variables are set correctly:

```bash
# Check if Gemini API key is set (optional)
echo $GEMINI_API_KEY

# Check if valid API keys are set (optional)
echo $VALID_API_KEYS

# Check Python version
python --version  # Should be 3.8+
```

---

## Step 6: Run Startup Test

Use the dedicated startup test script:

```bash
python test_startup.py
```

**Expected output:**
```
================================================================================
TRADE OPPORTUNITIES API - STARTUP TEST
================================================================================

Starting API server...
✓ Process started (PID: 12345)

Waiting for API to be ready...
✓ API is ready!

Testing API endpoint...
✓ API endpoint works!

Response preview (first 500 chars):
# Market Analysis: Pharmaceuticals

**Generated:** 2024-01-15 14:32:18

---

## Overview

The Indian pharmaceutical sector is a global leader...

✓ STARTUP TEST PASSED
```

---

## Common Issues & Solutions

### Issue 1: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'services'
```

**Solution:**
```bash
# Ensure you're in the project root directory
pwd  # Should show the project directory

# Verify services/__init__.py exists
ls -la services/__init__.py

# If missing, create it
touch services/__init__.py
touch utils/__init__.py
```

### Issue 2: ImportError in services

**Error:**
```
ImportError: cannot import name 'DataCollector' from 'services.data_collector'
```

**Solution:**
```bash
# Check if the file exists
ls -la services/data_collector.py

# Check for syntax errors
python -m py_compile services/data_collector.py

# If there are errors, fix them
```

### Issue 3: Gemini API Import Error

**Error:**
```
ModuleNotFoundError: No module named 'google.generativeai'
```

**Solution:**
```bash
# Install the package
pip install google-generativeai

# Or reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue 4: Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
python main.py --port 8001
```

### Issue 5: Timeout During Startup

**Error:**
```
API failed to start within 60 seconds
```

**Solution:**
1. Run `python main.py` directly to see what's happening
2. Check for import errors (Step 2)
3. Check dependencies (Step 3)
4. Check port availability (Step 4)
5. Increase timeout in run_validation.py

---

## Step 7: Run Validation Script

Once the startup test passes, run the validation script:

```bash
python run_validation.py
```

---

## Debugging Checklist

- [ ] Python version is 3.8+
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] No import errors (`python -c "from main import app"`)
- [ ] Port 8000 is available (`lsof -i :8000`)
- [ ] All module files exist (auth.py, rate_limiter.py, etc.)
- [ ] services/__init__.py exists
- [ ] utils/__init__.py exists
- [ ] Direct startup works (`python main.py`)
- [ ] Startup test passes (`python test_startup.py`)
- [ ] Validation script runs (`python run_validation.py`)

---

## Detailed Startup Logging

The API now logs detailed startup information:

```
================================================================================
Trade Opportunities API - Initializing
================================================================================
Importing auth module...
✓ Auth module imported successfully
Importing rate_limiter module...
✓ Rate limiter module imported successfully
Importing session_manager module...
✓ Session manager module imported successfully
Importing data_collector service...
✓ Data collector service imported successfully
Importing ai_analyzer service...
✓ AI analyzer service imported successfully
Importing markdown_formatter utility...
✓ Markdown formatter utility imported successfully
================================================================================
All components initialized successfully!
================================================================================
```

This tells you exactly which module failed to import if there's an error.

---

## Safe Fallback Behavior

The API is designed to start safely even if:

- ✓ Gemini API key is missing (uses rule-based analysis)
- ✓ DuckDuckGo is unavailable (uses mock data)
- ✓ Network is slow (uses timeouts)
- ✓ Port 8000 is in use (can use different port)

---

## Next Steps

1. **Test direct startup**: `python main.py`
2. **Run startup test**: `python test_startup.py`
3. **Run validation**: `python run_validation.py`
4. **Review report**: `cat validation_reports/validation_report_*.md`

---

## Support

If you still have issues:

1. Check the detailed startup logs
2. Run each import test individually
3. Verify all files exist
4. Check Python version
5. Reinstall dependencies

