# Quick Start Guide - Trade Opportunities API

Get the Trade Opportunities API running in 5 minutes.

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set Up Environment (Optional)

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Gemini API key (optional)
# If not set, the API will use fallback analysis
```

## 3. Run the API

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 4. Test the API

### Option A: Using cURL

```bash
curl -X GET "http://localhost:8000/analyze/pharmaceuticals" \
  -H "X-API-Key: trade-api-key-2024" \
  -H "Client-ID: user-1"
```

### Option B: Using Python

```python
import requests

response = requests.get(
    "http://localhost:8000/analyze/pharmaceuticals",
    headers={
        "X-API-Key": "trade-api-key-2024",
        "Client-ID": "user-1"
    }
)

print(response.text)
```

### Option C: Using Swagger UI

Open http://localhost:8000/docs in your browser

## 5. Run Test Suite

```bash
python test_api.py
```

## Example Requests

### Analyze Pharmaceuticals
```bash
curl -X GET "http://localhost:8000/analyze/pharmaceuticals" \
  -H "X-API-Key: trade-api-key-2024"
```

### Analyze Technology
```bash
curl -X GET "http://localhost:8000/analyze/technology" \
  -H "X-API-Key: trade-api-key-2024"
```

### Analyze Agriculture
```bash
curl -X GET "http://localhost:8000/analyze/agriculture" \
  -H "X-API-Key: trade-api-key-2024"
```

### Check Health
```bash
curl http://localhost:8000/health
```

### Get Session Stats
```bash
curl -X GET "http://localhost:8000/session-stats" \
  -H "X-API-Key: trade-api-key-2024"
```

## API Response

The API returns a markdown formatted report:

```markdown
# Market Analysis: Pharmaceuticals

**Generated:** 2024-01-15 10:30:45

---

## Overview

The Indian pharmaceutical sector is a global leader...

---

## Key Trends

- Shift towards specialty drugs and biosimilars
- Increasing focus on API manufacturing and exports
- ...

---

## Trade Opportunities

1. Export of generic drugs to regulated markets
2. Biosimilar development and manufacturing
3. ...

---

## Risks & Challenges

- Regulatory compliance and pricing pressures
- ...

---

## Future Outlook (2-3 Years)

The Indian pharmaceutical sector is expected to grow...

---

## Recommendations

### For Investors:
- Focus on sectors with strong government support
- ...
```

## Default API Key

The default API key is: `trade-api-key-2024`

To use a custom key, set the environment variable:
```bash
export VALID_API_KEYS="my-custom-key"
```

## Rate Limiting

- **Limit**: 5 requests per minute per client
- **Header**: Use `Client-ID` header to identify clients
- **Error**: Returns 429 status if limit exceeded

## Supported Sectors

- pharmaceuticals
- technology
- agriculture
- renewable_energy
- Any other sector (uses generic analysis)

## Troubleshooting

### Port 8000 already in use
```bash
python main.py --port 8001
```

### Import errors
```bash
pip install -r requirements.txt --force-reinstall
```

### API key not working
```bash
# Check if using correct key
# Default: trade-api-key-2024
```

## Next Steps

1. **Read the full README**: `README.md`
2. **Deploy to production**: `DEPLOYMENT.md`
3. **Customize the API**: Edit `main.py`, `services/`, `utils/`
4. **Add Gemini API key**: Get from https://makersuite.google.com/app/apikey

## Documentation

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **README**: `README.md`
- **Deployment**: `DEPLOYMENT.md`

---

**That's it! Your Trade Opportunities API is ready to use.**
