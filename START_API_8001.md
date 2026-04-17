# Start the API on Port 8001 - Quick Guide

## The Issue
Port 8000 is occupied by Splunk. The API now uses port 8001 by default.

## Quick Start

### Step 1: Start the API
```bash
python main.py
```

You should see:
```
Starting API on port 8001
API URL: http://localhost:8001
API Docs: http://localhost:8001/docs
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Step 2: Access Swagger UI
Open your browser:
```
http://localhost:8001/docs
```

### Step 3: Test the API
In another terminal:
```bash
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8001/health
```

Expected response:
```json
{"status":"healthy","service":"Trade Opportunities API"}
```

## Common Commands

### Health Check
```bash
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8001/health
```

### Analyze a Sector
```bash
curl -H "X-API-Key: trade-api-key-2024" \
     -H "Client-ID: my-client" \
     http://localhost:8001/analyze/technology
```

### Run Validation Suite
```bash
python validate_api.py
```

### Run Full Validation Report
```bash
python run_validation.py
```

### Test Documentation Endpoints
```bash
python test_docs.py
```

## Port Configuration

### Use Default Port (8001)
```bash
python main.py
```

### Use Custom Port
```bash
PORT=8002 python main.py
```

### Use Port 8000 (if Splunk is stopped)
```bash
PORT=8000 python main.py
```

## Troubleshooting

### API won't start
- Check if port 8001 is in use: `netstat -ano | findstr ":8001"`
- Try a different port: `PORT=8002 python main.py`

### Getting Splunk page
- You're accessing port 8000 instead of 8001
- Use correct URL: http://localhost:8001/docs (not 8000)

### Can't access /docs
- Verify API is running: `curl http://localhost:8001/health`
- Check browser console for errors
- Try a different browser

## Documentation

- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc
- **OpenAPI Schema:** http://localhost:8001/openapi.json

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /health | GET | Health check |
| /analyze/{sector} | GET | Analyze market sector |
| /session-stats | GET | Get session statistics |
| /docs | GET | Swagger UI documentation |
| /redoc | GET | ReDoc documentation |
| /openapi.json | GET | OpenAPI schema |

## Authentication

All endpoints except `/docs`, `/redoc`, and `/openapi.json` require:
- Header: `X-API-Key: trade-api-key-2024`

## That's It!

The API is now running on port 8001 and ready to use. All scripts have been updated to use this port consistently.

No more port conflicts with Splunk. Simple, predictable, production-ready.
