# API Startup - Exact Commands to Run

## Problem Summary

The API was failing to start during validation with error: **"API failed to start within 30 seconds"**

## Root Cause

1. Subprocess output buffering prevented detection of startup completion
2. 30-second timeout was too short
3. No visibility into startup errors

## Solution Applied

✅ Enhanced startup logging in `services/ai_analyzer.py`
✅ Enhanced startup logging in `services/data_collector.py`
✅ Created `debug_startup.py` - Comprehensive startup checker
✅ Created `simple_start.py` - Minimal startup script
✅ Created `validate_api.py` - Improved validation script

## Step-by-Step Instructions

### Step 1: Verify Setup (Run This First)

```bash
python debug_startup.py
```

**What it does:**
- Checks Python version (3.8+)
- Verifies all dependencies installed
- Tests all module imports
- Tests component initialization
- Shows exact error if any step fails

**Expected output:**
```
✓ ALL STARTUP CHECKS PASSED - API SHOULD START SUCCESSFULLY
```

**If it fails:**
- Read the error message carefully
- Install missing dependencies: `pip install -r requirements.txt`
- Run again

---

### Step 2: Start the API (Choose One)

#### Option A: Direct Python (Recommended)
```bash
python main.py
```

#### Option B: Using simple_start.py
```bash
python simple_start.py
```

#### Option C: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Option D: Production with gunicorn
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**If it fails:**
- Check if port 8000 is in use: `lsof -i :8000` (Mac/Linux) or `netstat -ano | findstr :8000` (Windows)
- Kill existing process or use different port
- Run `python debug_startup.py` to check for errors

---

### Step 3: Test the API (In Another Terminal)

#### Test 1: Health Check
```bash
curl -X GET "http://localhost:8000/health" \
  -H "X-API-Key: trade-api-key-2024"
```

**Expected response:**
```json
{"status":"healthy","service":"Trade Opportunities API"}
```

#### Test 2: Analyze a Sector
```bash
curl -X GET "http://localhost:8000/analyze/pharmaceuticals" \
  -H "X-API-Key: trade-api-key-2024" \
  -H "Client-ID: test-user"
```

**Expected response:**
- Markdown formatted report starting with `# Market Analysis: Pharmaceuticals`
- Takes 2-5 seconds

#### Test 3: View API Documentation
```
http://localhost:8000/docs
```

Open in browser to see interactive API documentation

---

### Step 4: Run Full Validation (Optional)

Once API is confirmed working:

```bash
python validate_api.py
```

**What it does:**
- Starts API automatically
- Runs 6 tests:
  - Health check
  - Invalid API key rejection
  - Invalid sector rejection
  - Pharmaceuticals analysis
  - Technology analysis
  - Agriculture analysis
- Stops API when done
- Shows summary

**Expected output:**
```
✓ Health Check: PASS
✓ Invalid API Key: PASS
✓ Invalid Sector: PASS
✓ Pharmaceuticals: PASS
✓ Technology: PASS
✓ Agriculture: PASS

Total: 6/6 tests passed
✓ All tests passed! API is ready for deployment.
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'google.generativeai'"

**Solution:**
```bash
pip install google-generativeai
```

Or reinstall all:
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: "Address already in use" or "Port 8000 already in use"

**Solution:**

**Mac/Linux:**
```bash
lsof -i :8000
kill -9 <PID>
```

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Or use different port:
```bash
python -c "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8001)"
```

### Issue: "API failed to start within 60 seconds"

**Solution:**
1. Run `python debug_startup.py` to check setup
2. Check console output for error messages
3. Verify all dependencies: `pip install -r requirements.txt`
4. Check if port is in use: `lsof -i :8000`

### Issue: "Connection refused" when testing

**Solution:**
- Make sure API is running: `python main.py`
- Check if it's on port 8000: `lsof -i :8000`
- Wait a few seconds after starting before testing
- Check for error messages in API console

---

## Verified Working Commands

These commands have been tested and verified to work:

```bash
# 1. Check setup
python debug_startup.py

# 2. Start API
python main.py

# 3. Test in another terminal
curl -X GET "http://localhost:8000/health" \
  -H "X-API-Key: trade-api-key-2024"

# 4. Run full validation
python validate_api.py
```

---

## Expected Startup Logs

When you run `python main.py`, you should see:

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

---

## Success Criteria

✅ `python debug_startup.py` completes without errors
✅ `python main.py` starts and shows "Application startup complete"
✅ Health check returns `{"status":"healthy",...}`
✅ Analysis endpoint returns markdown report
✅ `python validate_api.py` shows all 6 tests passing

Once all criteria are met, the API is production-ready.

---

## Next Steps After Startup Works

1. **Test with real Gemini API key** (optional):
   ```bash
   export GEMINI_API_KEY="your_api_key"
   python main.py
   ```

2. **Deploy to production** (Render/Railway):
   - See `DEPLOYMENT.md` for instructions

3. **Monitor logs**:
   - Check for `[GEMINI]`, `[SEARCH]`, `[PIPELINE]` prefixes
   - Verify fallback mechanisms work

---

## Files Created/Modified

**New files:**
- `debug_startup.py` - Startup verification script
- `simple_start.py` - Minimal startup script
- `validate_api.py` - Improved validation script
- `STARTUP_FIX.md` - Detailed debugging guide
- `STARTUP_COMMANDS.md` - This file

**Modified files:**
- `services/ai_analyzer.py` - Added detailed startup logging
- `services/data_collector.py` - Added initialization logging

---

## Quick Reference

| Task | Command |
|------|---------|
| Check setup | `python debug_startup.py` |
| Start API | `python main.py` |
| Test health | `curl http://localhost:8000/health -H "X-API-Key: trade-api-key-2024"` |
| Test analysis | `curl http://localhost:8000/analyze/pharmaceuticals -H "X-API-Key: trade-api-key-2024"` |
| View docs | `http://localhost:8000/docs` |
| Run validation | `python validate_api.py` |
| Kill API | `Ctrl+C` in terminal |
| Kill port 8000 | `lsof -i :8000 \| grep LISTEN \| awk '{print $2}' \| xargs kill -9` |

---

## Support

If you encounter issues:

1. **Run `python debug_startup.py`** - Shows exact error
2. **Check console output** - Look for error messages
3. **Verify dependencies** - `pip install -r requirements.txt`
4. **Check port** - `lsof -i :8000`
5. **Read error message carefully** - It usually tells you what's wrong

The API should start successfully within 5 seconds on a normal system.
