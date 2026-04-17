# Trade Opportunities API - Quick Reference

## Start the API

```bash
# Default port (8000)
python main.py

# Custom port
PORT=8001 python main.py

# Using uvicorn directly
uvicorn main:app --reload --port 8000
```

## Access Documentation

| Interface | URL |
|-----------|-----|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| OpenAPI Schema | http://localhost:8000/openapi.json |

## API Endpoints

### Health Check
```bash
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8000/health
```

### Analyze Sector
```bash
curl -H "X-API-Key: trade-api-key-2024" \
     -H "Client-ID: my-client" \
     http://localhost:8000/analyze/technology
```

### Session Statistics
```bash
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8000/session-stats
```

## Authentication

**API Key:** `trade-api-key-2024`

**Header:** `X-API-Key: trade-api-key-2024`

## Validation & Testing

```bash
# Run full validation suite
python validate_api.py

# Test documentation endpoints
python test_docs.py

# Test startup
python debug_startup.py
```

## Common Sectors

- pharmaceuticals
- technology
- agriculture
- finance
- energy
- healthcare
- retail
- manufacturing

## Rate Limiting

- **Limit:** 5 requests per minute per client
- **Tracked by:** Client-ID header (or IP if not provided)
- **Error:** 429 Too Many Requests

## Response Format

### Health Check
```json
{
  "status": "healthy",
  "service": "Trade Opportunities API"
}
```

### Analysis
```markdown
# Market Analysis: [Sector]

## Executive Summary
...

## Key Trends
...

## Investment Opportunities
...
```

### Session Stats
```json
{
  "total_requests": 5,
  "unique_clients": 2,
  "sectors_analyzed": ["technology", "pharmaceuticals"],
  "requests_by_client": {...}
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Use different port: `PORT=8001 python main.py` |
| 401 Unauthorized | Check API key: `trade-api-key-2024` |
| 400 Bad Request | Sector must contain only letters |
| 429 Too Many Requests | Wait 60 seconds or use different client ID |
| /docs not accessible | Restart API: `python main.py` |

## Environment Variables

```bash
# Set custom port
PORT=8001

# Set Gemini API key (optional)
GEMINI_API_KEY=your-key-here
```

## Files

| File | Purpose |
|------|---------|
| main.py | API entry point |
| auth.py | Authentication logic |
| rate_limiter.py | Rate limiting |
| session_manager.py | Session tracking |
| services/data_collector.py | Market data collection |
| services/ai_analyzer.py | AI analysis |
| utils/markdown_formatter.py | Report formatting |
| validate_api.py | Validation suite |
| test_docs.py | Documentation tests |

## Documentation

- `STARTUP_GUIDE.md` - How to start the API
- `DOCS_ACCESS_GUIDE.md` - How to access documentation
- `VERIFY_STARTUP.md` - Verification steps
- `API_REFERENCE.md` - Full API reference

## Status

✅ API is production-ready
✅ All endpoints functional
✅ Documentation accessible
✅ Validation suite available
✅ Error handling complete
✅ Rate limiting active
✅ Session management enabled
