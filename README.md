# Trade Opportunities API

A FastAPI service that analyzes market sectors and generates trade opportunity insights. It pulls market data, runs analysis (with AI or rule-based fallback), and returns formatted reports.

## Quick Start

Install dependencies:
```bash
pip install -r requirements.txt
```

Run locally:
```bash
python main.py
```

The API starts on `http://localhost:8001` by default.

## API Endpoints

**Health Check**
```bash
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8001/health
```

**Analyze a Sector**
```bash
curl -H "X-API-Key: trade-api-key-2024" \
  http://localhost:8001/analyze/technology
```

Valid sectors: `pharmaceuticals`, `technology`, `agriculture`, `healthcare`, `finance`, `energy`

**Interactive Docs**
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## Configuration

Set environment variables in `.env`:

```
PORT=8001
LOG_LEVEL=INFO
GEMINI_API_KEY=your-key-here
API_KEY=trade-api-key-2024
```

Or pass them directly:
```bash
PORT=8000 python main.py
```

## How It Works

1. **Authentication** - Validates API key from `X-API-Key` header
2. **Rate Limiting** - 5 requests per minute per client
3. **Data Collection** - Fetches market data via DuckDuckGo (falls back to mock data)
4. **Analysis** - Uses Gemini API if available, otherwise rule-based analysis
5. **Formatting** - Generates markdown report
6. **Response** - Returns formatted report

## Deployment

Deploy to Render:

1. Push to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Set environment variables
5. Deploy

See `RENDER_DEPLOYMENT_GUIDE.md` for detailed steps.

## Project Structure

```
main.py                 - FastAPI app
auth.py                 - API key validation
rate_limiter.py         - Rate limiting
session_manager.py      - Session tracking
services/
  data_collector.py     - Market data fetching
  ai_analyzer.py        - Analysis logic
utils/
  markdown_formatter.py - Report formatting
requirements.txt        - Dependencies
Procfile               - Render config
```

## Testing

Run the validation suite:
```bash
python validate_api.py
```

This tests all endpoints and reports results.

## Notes

- The API works without Gemini API key (uses fallback analysis)
- DuckDuckGo search is optional (uses mock data if unavailable)
- Rate limiting is per-client based on `Client-ID` header or IP
- All responses are markdown formatted

## License

MIT
