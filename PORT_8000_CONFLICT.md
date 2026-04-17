# Port 8000 Conflict - Splunk is Running

## Problem

Port 8000 is already in use by **Splunk** (process ID: 3240).

When you ran `python main.py`, the API tried to bind to port 8000 but failed silently because Splunk was already listening on that port.

## Solution

### Option 1: Use a Different Port (Recommended)

Start the API on port 8001 instead:

```bash
PORT=8001 python main.py
```

Then access:
- API: http://localhost:8001
- Docs: http://localhost:8001/docs
- Health: http://localhost:8001/health

### Option 2: Stop Splunk and Use Port 8000

If you don't need Splunk running:

```powershell
# Stop Splunk
Stop-Process -Name splunkd -Force

# Start the API on port 8000
python main.py
```

Then access:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Verification

### Check if API is running on port 8001

```bash
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8001/health
```

Expected response:
```json
{"status":"healthy","service":"Trade Opportunities API"}
```

### Check if Splunk is still running

```powershell
Get-Process -Name splunkd
```

If it shows a process, Splunk is running on port 8000.

## Recommended Approach

**Use port 8001 for the API** to avoid conflicts with Splunk:

```bash
# Terminal 1: Start API on port 8001
PORT=8001 python main.py

# Terminal 2: Test the API
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8001/health

# Terminal 3: Access documentation
# Open browser: http://localhost:8001/docs
```

## Why This Happened

1. Splunk was already running on port 8000
2. When you ran `python main.py`, uvicorn tried to bind to port 8000
3. The binding failed because Splunk was already using it
4. The API startup logs showed "Application startup complete" but the API never actually started
5. When you accessed http://localhost:8000/docs, you got Splunk's 404 page instead of the API

## Next Steps

1. **Start API on port 8001:**
   ```bash
   PORT=8001 python main.py
   ```

2. **Verify it's running:**
   ```bash
   curl -H "X-API-Key: trade-api-key-2024" http://localhost:8001/health
   ```

3. **Access documentation:**
   - Open http://localhost:8001/docs in your browser

4. **Run validation:**
   ```bash
   python validate_api.py
   ```

The validation script already uses port 8001, so it should work correctly now.
