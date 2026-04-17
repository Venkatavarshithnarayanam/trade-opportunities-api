# Getting Started - Trade Opportunities API

Welcome! This guide will get you up and running in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Terminal/Command prompt

## Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI - Web framework
- Uvicorn - ASGI server
- Pydantic - Data validation
- Google Generative AI - Gemini API
- DuckDuckGo Search - Web search
- httpx - HTTP client

## Step 2: Run the API (30 seconds)

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The API is now running!

## Step 3: Test the API (1 minute)

Open a new terminal and run:

```bash
curl -X GET "http://localhost:8000/analyze/pharmaceuticals" \
  -H "X-API-Key: trade-api-key-2024"
```

You should get a markdown report about the pharmaceutical sector.

## Step 4: View API Documentation (30 seconds)

Open your browser and go to:
```
http://localhost:8000/docs
```

This shows interactive API documentation where you can:
- See all endpoints
- Try out requests
- View response schemas

## Step 5: Run Tests (1 minute)

Open another terminal and run:

```bash
python test_api.py
```

This runs comprehensive tests to verify everything works.

---

## Common First Steps

### Save a Report to File

```bash
curl -X GET "http://localhost:8000/analyze/technology" \
  -H "X-API-Key: trade-api-key-2024" \
  -o tech_report.md
```

This saves the report as `tech_report.md` which you can open in any text editor.

### Analyze Different Sectors

```bash
# Pharmaceuticals
curl -X GET "http://localhost:8000/analyze/pharmaceuticals" \
  -H "X-API-Key: trade-api-key-2024"

# Technology
curl -X GET "http://localhost:8000/analyze/technology" \
  -H "X-API-Key: trade-api-key-2024"

# Agriculture
curl -X GET "http://localhost:8000/analyze/agriculture" \
  -H "X-API-Key: trade-api-key-2024"

# Renewable Energy
curl -X GET "http://localhost:8000/analyze/renewable_energy" \
  -H "X-API-Key: trade-api-key-2024"
```

### Use Python

```python
import requests

response = requests.get(
    "http://localhost:8000/analyze/pharmaceuticals",
    headers={"X-API-Key": "trade-api-key-2024"}
)

print(response.text)
```

### Run Usage Examples

```bash
python example_usage.py
```

This demonstrates 7 different usage patterns.

---

## Configuration (Optional)

### Add Gemini API Key

For better AI analysis, add your Gemini API key:

1. Get a free API key from: https://makersuite.google.com/app/apikey
2. Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Restart the API

Without this, the API uses rule-based analysis (still works great!).

### Custom API Keys

To use custom API keys instead of the default:

```bash
export VALID_API_KEYS="my-key-1,my-key-2,my-key-3"
```

Then use:
```bash
curl -X GET "http://localhost:8000/analyze/pharmaceuticals" \
  -H "X-API-Key: my-key-1"
```

---

## What's Included

### Core Application
- `main.py` - FastAPI application
- `auth.py` - Authentication
- `rate_limiter.py` - Rate limiting
- `session_manager.py` - Session tracking
- `services/` - Data collection and AI analysis
- `utils/` - Markdown formatting

### Documentation
- `README.md` - Complete guide
- `QUICKSTART.md` - Quick start
- `DEPLOYMENT.md` - Deployment guide
- `API_REFERENCE.md` - API documentation
- `PROJECT_SUMMARY.md` - Project overview

### Testing & Examples
- `test_api.py` - Test suite
- `example_usage.py` - Usage examples

---

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Analyze Sector (Main Endpoint)
```bash
curl -X GET "http://localhost:8000/analyze/{sector}" \
  -H "X-API-Key: trade-api-key-2024" \
  -H "Client-ID: user-1"
```

### Session Statistics
```bash
curl -X GET "http://localhost:8000/session-stats" \
  -H "X-API-Key: trade-api-key-2024"
```

---

## Rate Limiting

The API limits requests to **5 per minute per client**.

If you exceed the limit, you'll get:
```
HTTP 429 Too Many Requests
```

Wait 60 seconds and try again, or use a different `Client-ID`.

---

## Troubleshooting

### Port 8000 Already in Use

```bash
python main.py --port 8001
```

Then access at `http://localhost:8001`

### Import Errors

```bash
pip install -r requirements.txt --force-reinstall
```

### API Not Responding

Make sure the API is running:
```bash
curl http://localhost:8000/health
```

If not, start it:
```bash
python main.py
```

### Invalid API Key Error

Use the default key:
```bash
-H "X-API-Key: trade-api-key-2024"
```

---

## Next Steps

1. **Explore the API**
   - Try different sectors
   - Save reports to files
   - Check the documentation at `/docs`

2. **Read the Documentation**
   - `README.md` - Complete guide
   - `API_REFERENCE.md` - API details
   - `DEPLOYMENT.md` - Deployment guide

3. **Deploy to Production**
   - See `DEPLOYMENT.md` for Render/Railway
   - Or deploy locally with Gunicorn

4. **Customize**
   - Add Gemini API key
   - Modify rate limiting
   - Add custom sectors
   - Integrate with database

---

## Example Workflow

### 1. Start the API
```bash
python main.py
```

### 2. Analyze a Sector
```bash
curl -X GET "http://localhost:8000/analyze/pharmaceuticals" \
  -H "X-API-Key: trade-api-key-2024" \
  -o pharma_report.md
```

### 3. View the Report
Open `pharma_report.md` in your text editor or markdown viewer.

### 4. Analyze More Sectors
```bash
curl -X GET "http://localhost:8000/analyze/technology" \
  -H "X-API-Key: trade-api-key-2024" \
  -o tech_report.md

curl -X GET "http://localhost:8000/analyze/agriculture" \
  -H "X-API-Key: trade-api-key-2024" \
  -o agri_report.md
```

### 5. Check Session Stats
```bash
curl -X GET "http://localhost:8000/session-stats" \
  -H "X-API-Key: trade-api-key-2024"
```

---

## Key Features

✅ **Single Endpoint** - GET /analyze/{sector}
✅ **Market Analysis** - Comprehensive reports
✅ **AI-Powered** - Gemini API with fallback
✅ **Secure** - API key authentication
✅ **Rate Limited** - 5 requests/minute
✅ **Session Tracking** - Request history
✅ **Error Handling** - Proper HTTP responses
✅ **Well Documented** - Complete guides

---

## Support

- **API Docs**: http://localhost:8000/docs
- **README**: `README.md`
- **API Reference**: `API_REFERENCE.md`
- **Deployment**: `DEPLOYMENT.md`
- **Troubleshooting**: `README.md` (Troubleshooting section)

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python main.py` | Start the API |
| `python test_api.py` | Run tests |
| `python example_usage.py` | Run examples |
| `curl http://localhost:8000/health` | Check health |
| `curl http://localhost:8000/docs` | View API docs |

---

## That's It!

You're ready to use the Trade Opportunities API. Start with:

```bash
python main.py
```

Then in another terminal:

```bash
curl -X GET "http://localhost:8000/analyze/pharmaceuticals" \
  -H "X-API-Key: trade-api-key-2024"
```

Enjoy analyzing market opportunities!

---

**Need help?** Check the documentation files or run the test suite.

**Ready to deploy?** See `DEPLOYMENT.md` for Render/Railway instructions.

**Want to customize?** Edit the configuration or add your Gemini API key.
