# API Startup Fix - Complete Debugging Guide

## Problem Identified

The API fails to start within 30 seconds during validation. Root causes:

1. **Subprocess buffering** - `run_validation.py` can't detect when API is ready
2. **Port conflicts** - Port 8000 might be in use
3. **Timing issues** - 30-second timeout too short for first startup
4. **Missing error output** - Subprocess errors not visible

## Solution

### Step 1: Verify Setup (Run First)

```bash
python debug_startup.py
```

This will:
- Check Python version
- Verify all dependencies installed
- Test all module imports
- Test component initialization
- Show exact error if any step fails

**Expected output:**
```
✓ ALL STARTUP CHECKS PASSED - API SHOULD START SUCCESSFULLY
```

### Step 2: Start API Directly (Simplest Method)

```bash
python simple_start.py
```

Or:

```bash
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 3: Test API in Another Terminal

```bash
# Health check
curl -X GET "http://localhost:8000/health" \
  -H "X-API-Key: trade-api-key-2024"

# Analyze a sector
curl -X GET "http://localhost:8000/analyze/pharmaceuticals" \
  -H "X-API-Key: trade-api-key-2024" \
  -H "Client-ID: test-user"
```

### Step 4: If Port 8000 is Already in Use

Find and kill the process:

**On Linux/Mac:**
```bash
lsof -i :8000
kill -9 <PID>
```

**On Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Or use a different port:

```bash
python -c "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8001)"
```

## Troubleshooting

### Issue: "API failed to start within 30 seconds"

**Solution:**
1. Run `python debug_startup.py` to check setup
2. Run `python simple_start.py` to start API directly
3. Check if port 8000 is in use: `lsof -i :8000`
4. Check for error messages in console output

### Issue: "ModuleNotFoundError: No module named 'google.generativeai'"

**Solution:**
```bash
pip install google-generativeai
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: "ModuleNotFoundError: No module named 'duckduckgo_search'"

**Solution:**
```bash
pip install duckduckgo-search
```

### Issue: "Address already in use"

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
python -c "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8001)"
```

## Verified Startup Commands

### Command 1: Direct Python (Recommended)
```bash
python main.py
```

### Command 2: Using simple_start.py
```bash
python simple_start.py
```

### Command 3: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Command 4: Using gunicorn (Production)
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## Startup Sequence (What Happens)

1. **Import phase** (< 1 second)
   - FastAPI imports
   - Local modules imported
   - Dependencies checked

2. **Initialization phase** (< 2 seconds)
   - RateLimiter initialized
   - SessionManager initialized
   - DataCollector initialized (loads mock data)
   - AIAnalyzer initialized (checks Gemini API key)
   - MarkdownFormatter initialized

3. **FastAPI startup** (< 1 second)
   - App created
   - Routes registered
   - Lifespan context manager started

4. **Uvicorn startup** (< 2 seconds)
   - Server binds to port 8000
   - Event loop starts
   - Ready to accept requests

**Total startup time: 2-5 seconds**

## Logs to Expect

When starting with `python main.py`, you should see:

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
Initializing components...
Initializing rate limiter...
✓ Rate limiter initialized
Initializing session manager...
✓ Session manager initialized
Initializing data collector...
[INIT] Initializing DataCollector...
[INIT] ✓ DataCollector initialized successfully
✓ Data collector initialized
Initializing AI analyzer...
[INIT] Initializing AIAnalyzer...
[INIT] GEMINI_API_KEY not set, will use fallback rule-based analysis
✓ AI analyzer initialized
Initializing markdown formatter...
✓ Markdown formatter initialized
================================================================================
All components initialized successfully!
================================================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
================================================================================
Trade Opportunities API - Startup Complete
================================================================================
API is ready to accept requests
Health check: GET /health
API Docs: GET /docs
================================================================================
```

## Next Steps

1. **Run debug_startup.py** to verify setup
2. **Run simple_start.py** or **python main.py** to start API
3. **Test with curl** to verify it works
4. **Then run validation** once API is confirmed working

## Files Modified

- `services/ai_analyzer.py` - Added detailed startup logging
- `services/data_collector.py` - Added initialization logging
- `debug_startup.py` - NEW: Comprehensive startup checker
- `simple_start.py` - NEW: Minimal startup script
- `STARTUP_FIX.md` - NEW: This file

## Success Criteria

✅ `python debug_startup.py` completes without errors
✅ `python main.py` starts and shows "Application startup complete"
✅ `curl http://localhost:8000/health -H "X-API-Key: trade-api-key-2024"` returns `{"status":"healthy",...}`
✅ `curl http://localhost:8000/analyze/pharmaceuticals -H "X-API-Key: trade-api-key-2024"` returns markdown report

Once all 4 criteria are met, the API is ready for validation and deployment.
