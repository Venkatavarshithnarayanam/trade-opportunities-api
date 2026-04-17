# Trade Opportunities API

A production-ready FastAPI service that analyzes market data and generates trade opportunity insights for specific sectors in India.

## Features

- **Single Endpoint Analysis**: `GET /analyze/{sector}` - Analyze any sector for trade opportunities
- **AI-Powered Insights**: Integrates Google Gemini API with intelligent fallback to rule-based analysis
- **Market Data Collection**: Gathers real-time market data using DuckDuckGo search with mock data fallback
- **Security**: API key authentication, input validation, and rate limiting
- **Rate Limiting**: 5 requests per minute per client
- **Session Management**: In-memory tracking of API usage and request history
- **Structured Output**: Returns professional markdown reports with analysis

## Project Structure

```
.
├── main.py                      # FastAPI application entry point
├── auth.py                      # API key authentication
├── rate_limiter.py             # Rate limiting implementation
├── session_manager.py          # Session tracking
├── services/
│   ├── data_collector.py       # Market data collection
│   └── ai_analyzer.py          # AI analysis with Gemini integration
├── utils/
│   └── markdown_formatter.py   # Markdown report formatting
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   VALID_API_KEYS=trade-api-key-2024,your-custom-key
   ```
   
   - **GEMINI_API_KEY**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **VALID_API_KEYS**: Comma-separated list of valid API keys (default: `trade-api-key-2024`)

## Running the Application

### Development Mode

```bash
python main.py
```

The API will start at `http://localhost:8000`

### Production Mode (using Uvicorn)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Trade Opportunities API"
}
```

### Analyze a Sector

```bash
curl -X GET "http://localhost:8000/analyze/pharmaceuticals" \
  -H "X-API-Key: trade-api-key-2024" \
  -H "Client-ID: user-123"
```

**Parameters:**
- `sector` (path): Sector name (e.g., pharmaceuticals, technology, agriculture)
- `X-API-Key` (header): Required API key for authentication
- `Client-ID` (header): Optional client identifier for session tracking

**Response:** Markdown formatted market analysis report

### Example Request with cURL

```bash
# Analyze pharmaceuticals sector
curl -X GET "http://localhost:8000/analyze/pharmaceuticals" \
  -H "X-API-Key: trade-api-key-2024" \
  -H "Client-ID: investor-001"

# Analyze technology sector
curl -X GET "http://localhost:8000/analyze/technology" \
  -H "X-API-Key: trade-api-key-2024" \
  -H "Client-ID: investor-001"

# Analyze agriculture sector
curl -X GET "http://localhost:8000/analyze/agriculture" \
  -H "X-API-Key: trade-api-key-2024" \
  -H "Client-ID: investor-001"
```

### Example Response

```markdown
# Market Analysis: Pharmaceuticals

**Generated:** 2024-01-15 10:30:45

---

## Overview

The Indian pharmaceutical sector is a global leader in generic drug manufacturing and API production. With strong government support and growing healthcare spending, the sector presents significant opportunities for expansion and innovation.

---

## Key Trends

- Shift towards specialty drugs and biosimilars
- Increasing focus on API manufacturing and exports
- Digital health and telemedicine integration
- Rising healthcare spending in India

---

## Trade Opportunities

1. Export of generic drugs to regulated markets (US, EU)
2. Biosimilar development and manufacturing
3. Contract manufacturing for global pharma companies
4. Healthcare infrastructure development

---

## Risks & Challenges

- Regulatory compliance and pricing pressures
- Competition from other generic manufacturers
- Supply chain disruptions
- Patent litigation risks

---

## Future Outlook (2-3 Years)

The Indian pharmaceutical sector is expected to grow at 8-10% CAGR through 2025. Opportunities in specialty drugs, biosimilars, and contract manufacturing will drive growth. Government initiatives and rising healthcare spending will support expansion.

---

## Recommendations

### For Investors:
- Focus on sectors with strong government support and policy tailwinds
- Consider long-term growth potential in emerging technologies
- Diversify across multiple opportunities to mitigate risks

### For Entrepreneurs:
- Identify gaps in the market and develop innovative solutions
- Leverage government schemes and incentives
- Build partnerships with established players for market access

### For Businesses:
- Invest in technology and digital transformation
- Expand into high-growth segments
- Develop sustainable and compliant operations

### Key Success Factors:
- Strong regulatory compliance and governance
- Continuous innovation and adaptation
- Strategic partnerships and collaborations
- Focus on quality and customer satisfaction

---

*Report generated by Trade Opportunities API*
```

### Get Session Statistics

```bash
curl -X GET "http://localhost:8000/session-stats" \
  -H "X-API-Key: trade-api-key-2024"
```

**Response:**
```json
{
  "total_sessions": 5,
  "total_requests": 12,
  "active_clients": ["user-123", "investor-001"]
}
```

## Error Handling

### Invalid API Key
```
Status: 401 Unauthorized
Detail: Invalid API key
```

### Invalid Sector Input
```
Status: 400 Bad Request
Detail: Sector must contain only alphabetic characters
```

### Rate Limit Exceeded
```
Status: 429 Too Many Requests
Detail: Rate limit exceeded: Maximum 5 requests per minute
```

### Server Error
```
Status: 500 Internal Server Error
Detail: Internal server error during analysis
```

## Supported Sectors

The API has built-in data for these sectors:
- **pharmaceuticals** - Pharma industry analysis
- **technology** - Tech sector insights
- **agriculture** - AgriTech and farming opportunities
- **renewable_energy** - Clean energy opportunities
- Any other sector (uses generic analysis)

## Configuration

### Rate Limiting

Edit `main.py` to adjust rate limiting:
```python
rate_limiter = RateLimiter(max_requests=5, window_seconds=60)
```

### API Keys

Set valid API keys via environment variable:
```bash
export VALID_API_KEYS="key1,key2,key3"
```

Or edit `auth.py` to change the default key.

## Deployment

### Deploy on Render

1. **Create a Render account** at https://render.com

2. **Create a new Web Service**
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port 8000`

3. **Set environment variables**
   - Add `GEMINI_API_KEY` in Render dashboard
   - Add `VALID_API_KEYS` if needed

4. **Deploy**
   - Render will automatically deploy on push to main branch

### Deploy on Railway

1. **Create a Railway account** at https://railway.app

2. **Connect your GitHub repository**

3. **Add environment variables**
   - `GEMINI_API_KEY`
   - `VALID_API_KEYS`

4. **Set start command**
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

5. **Deploy**
   - Railway will automatically build and deploy

### Deploy on Local Server

```bash
# Install Gunicorn for production
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

## Testing

### Using Python requests

```python
import requests

API_KEY = "trade-api-key-2024"
BASE_URL = "http://localhost:8000"

# Analyze a sector
response = requests.get(
    f"{BASE_URL}/analyze/pharmaceuticals",
    headers={
        "X-API-Key": API_KEY,
        "Client-ID": "test-user"
    }
)

print(response.text)
```

### Using Postman

1. Create a new GET request
2. URL: `http://localhost:8000/analyze/pharmaceuticals`
3. Headers:
   - `X-API-Key: trade-api-key-2024`
   - `Client-ID: test-user`
4. Send request

## Logging

The application logs all important events:
- API requests and responses
- Authentication attempts
- Rate limit violations
- Data collection and analysis
- Errors and exceptions

Logs are printed to console with timestamps and severity levels.

## Architecture

### Clean Separation of Concerns

- **main.py**: API routing and request handling
- **auth.py**: Authentication logic
- **rate_limiter.py**: Rate limiting implementation
- **session_manager.py**: Session tracking
- **services/data_collector.py**: Market data collection
- **services/ai_analyzer.py**: AI analysis
- **utils/markdown_formatter.py**: Output formatting

### Data Flow

```
Request → Authentication → Rate Limiting → Session Tracking
    ↓
Data Collection (Search/Mock) → AI Analysis (Gemini/Fallback)
    ↓
Markdown Formatting → Response
```

## Performance

- **Response Time**: 2-5 seconds (depending on API availability)
- **Concurrent Requests**: Supports multiple concurrent requests
- **Memory Usage**: Minimal (in-memory storage only)
- **Scalability**: Can be scaled horizontally with load balancing

## Security Considerations

- API key authentication prevents unauthorized access
- Input validation prevents injection attacks
- Rate limiting prevents abuse
- Error messages don't expose sensitive information
- Logging tracks all access attempts

## Troubleshooting

### Gemini API Not Working

If Gemini API fails, the system automatically falls back to rule-based analysis. Check:
1. `GEMINI_API_KEY` environment variable is set correctly
2. API key has sufficient quota
3. Network connectivity to Google API

### Rate Limiting Issues

If you're getting rate limit errors:
1. Wait 60 seconds before making another request
2. Use different `Client-ID` headers for different clients
3. Adjust rate limit settings in `main.py`

### Import Errors

If you get import errors:
1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check Python version is 3.8+
3. Verify virtual environment is activated

## Future Enhancements

- Database integration for persistent storage
- Advanced caching mechanisms
- Multiple LLM support
- Real-time data streaming
- Advanced analytics and reporting
- User authentication and authorization
- API versioning

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs for error details
3. Verify environment configuration
4. Test with curl or Postman

## Author

Built as a production-ready FastAPI service for market analysis and trade opportunity identification.

---

**Last Updated:** January 2024
**Version:** 1.0.0
