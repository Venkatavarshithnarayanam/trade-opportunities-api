# Fix Port Conflict and Start API - Action Plan

## Current Situation

- **Port 8000:** Occupied by Splunk (process 3240)
- **Port 8001:** Available
- **API Status:** Not running

## What You Need to Do

### Step 1: Open a New Terminal

Open PowerShell or Command Prompt in your project directory.

### Step 2: Start the API on Port 8001

```bash
PORT=8001 python main.py
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Step 3: Verify API is Running

Open another terminal and run:

```bash
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8001/health
```

Expected response:
```json
{"status":"healthy","service":"Trade Opportunities API"}
```

### Step 4: Access Documentation

Open your browser and go to:
```
http://localhost:8001/docs
```

You should see the Swagger UI interface.

## If You Want to Use Port 8000

If you want to use port 8000 instead of 8001, you need to stop Splunk first:

```powershell
# Stop Splunk
Stop-Process -Name splunkd -Force

# Start API on port 8000
python main.py
```

Then access:
```
http://localhost:8000/docs
```

## Quick Commands

### Start API on port 8001
```bash
PORT=8001 python main.py
```

### Test health endpoint
```bash
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8001/health
```

### Run validation suite
```bash
python validate_api.py
```

### Test documentation endpoints
```bash
python test_docs.py
```

## Expected Results

Once the API is running on port 8001:

✅ Health check returns: `{"status":"healthy","service":"Trade Opportunities API"}`
✅ Swagger UI loads at: http://localhost:8001/docs
✅ ReDoc loads at: http://localhost:8001/redoc
✅ OpenAPI schema at: http://localhost:8001/openapi.json
✅ Analysis endpoint works: http://localhost:8001/analyze/technology

## Troubleshooting

### API still won't start
- Check if port 8001 is free: `netstat -ano | findstr ":8001"`
- Try port 8002: `PORT=8002 python main.py`

### Still getting Splunk page
- You're accessing the wrong port
- Make sure you're using port 8001, not 8000
- Check the URL: http://localhost:8001/docs (not 8000)

### Can't access /docs
- Verify API is running: `curl http://localhost:8001/health`
- Check browser console for errors
- Try a different browser

## Summary

The issue was that **Splunk was using port 8000**. Your API couldn't start because that port was already in use.

**Solution:** Start the API on port 8001 instead.

```bash
PORT=8001 python main.py
```

Then access the documentation at:
```
http://localhost:8001/docs
```

That's it! The API will work perfectly on port 8001.
