# Verify API Startup - Step by Step

## Prerequisites

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure no process is using port 8001:
```bash
# On Windows (PowerShell)
Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue

# On Linux/Mac
lsof -i :8001
```

## Test 1: Start API on Default Port (8000)

```bash
python main.py
```

**Expected Output:**
```
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify in another terminal:**
```bash
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8000/health
```

**Expected Response:**
```json
{"status":"healthy","service":"Trade Opportunities API"}
```

## Test 2: Start API on Custom Port (8001)

```bash
PORT=8001 python main.py
```

**Expected Output:**
```
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify in another terminal:**
```bash
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8001/health
```

## Test 3: Run Full Validation Suite

```bash
python validate_api.py
```

**Expected Output:**
```
================================================================================
                    STARTING API SERVER
================================================================================

ℹ Launching API with: PORT=8001 python main.py
ℹ Process started, waiting for API on port 8001...
✓ API is ready on port 8001

================================================================================
                    TESTING HEALTH CHECK
================================================================================

✓ Health check passed
ℹ Response: {'status': 'healthy', 'service': 'Trade Opportunities API'}

[... more tests ...]

================================================================================
                    VALIDATION SUMMARY
================================================================================

  Health Check: PASS
  Invalid API Key: PASS
  Invalid Sector: PASS
  Pharmaceuticals: PASS
  Technology: PASS
  Agriculture: PASS

Total: 6/6 tests passed
API running on: http://localhost:8001
✓ All tests passed! API is ready for deployment.
```

## Test 4: Port Conflict Handling

If port 8000 is already in use:

```bash
# This will fail with clear error
python main.py

# Expected error:
# ERROR:    [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Solution: Use different port**
```bash
PORT=8001 python main.py
```

## Troubleshooting

### API doesn't start
- Check logs for import errors
- Verify all dependencies: `pip install -r requirements.txt`
- Check if port is in use: `PORT=8001 python main.py`

### Validation tests fail
- Ensure API is running on port 8001
- Check API logs for errors
- Verify API key is correct: `trade-api-key-2024`

### Port already in use
- Use different port: `PORT=8002 python main.py`
- Or kill process using the port

## Success Criteria

✅ API starts without errors
✅ Health check responds with 200 status
✅ Analysis endpoint returns markdown report
✅ Invalid API key returns 401
✅ Invalid sector returns 400
✅ All validation tests pass

When all criteria are met, the API is ready for deployment.
