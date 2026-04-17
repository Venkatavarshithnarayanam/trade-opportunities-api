# Trade Opportunities API - Startup Guide

## Quick Start

The API uses standard `uvicorn` for startup with no custom port management logic.

### Option 1: Default Port (8000)
```bash
python main.py
```

### Option 2: Custom Port via Environment Variable
```bash
PORT=8001 python main.py
```

### Option 3: Using uvicorn Directly
```bash
uvicorn main:app --reload --port 8001
```

## Port Conflict Handling

If port 8000 is already in use:
- **Option A**: Use a different port (see Option 2 or 3 above)
- **Option B**: Kill the process using port 8000 on your system
- **Option C**: The API will fail with a clear error message from uvicorn

## Validation

To validate the API is working correctly:

```bash
# Terminal 1: Start the API on port 8001
PORT=8001 python main.py

# Terminal 2: Run validation tests
python validate_api.py
```

The validation script will:
1. Start the API on port 8001
2. Wait for it to be ready
3. Run comprehensive tests
4. Report results

## Expected Output

When the API starts successfully, you should see:
```
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Troubleshooting

### "Address already in use" Error
- The port is occupied by another process
- Use a different port: `PORT=8001 python main.py`
- Or kill the process using that port

### API doesn't respond to requests
- Check that the API is running: `curl http://localhost:8000/health`
- Verify the port matches your startup command
- Check logs for import or initialization errors

### Validation tests fail
- Ensure the API is running on the correct port
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify the API key in validate_api.py matches your configuration

## Architecture

The simplified startup approach:
- Uses standard `uvicorn.run()` with no custom retry logic
- Supports port configuration via `PORT` environment variable
- Lets uvicorn handle port binding errors naturally
- No pre-checks or exception-driven retries (unreliable on Windows)

This keeps the system simple, predictable, and production-aligned.
