# API Documentation Access Guide

## Overview

The Trade Opportunities API now provides full interactive documentation through multiple interfaces.

## Documentation Endpoints

### 1. Swagger UI (Interactive)
**URL:** `http://localhost:8000/docs`

Features:
- Interactive API explorer
- Try out endpoints directly from the browser
- View request/response examples
- See all available parameters and schemas

### 2. ReDoc (Alternative Documentation)
**URL:** `http://localhost:8000/redoc`

Features:
- Clean, organized API documentation
- Search functionality
- Mobile-friendly layout
- Detailed endpoint descriptions

### 3. OpenAPI Schema (Machine-Readable)
**URL:** `http://localhost:8000/openapi.json`

Features:
- Raw OpenAPI 3.0 specification
- Can be imported into tools like Postman, Insomnia, etc.
- Programmatic access to API schema

## Quick Start

### Step 1: Start the API
```bash
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Step 2: Access Documentation
Open your browser and navigate to:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Step 3: Test Endpoints
In Swagger UI, you can:
1. Click on any endpoint (e.g., `/health` or `/analyze/{sector}`)
2. Click "Try it out"
3. Fill in required parameters
4. Click "Execute"
5. View the response

## Available Endpoints

### Health Check
- **Path:** `GET /health`
- **Description:** Check if API is running
- **Response:** `{"status": "healthy", "service": "Trade Opportunities API"}`

### Analyze Sector
- **Path:** `GET /analyze/{sector}`
- **Parameters:**
  - `sector` (path): Sector name (e.g., "pharmaceuticals", "technology", "agriculture")
  - `X-API-Key` (header): API key for authentication
  - `Client-ID` (header, optional): Client identifier for session tracking
- **Response:** Markdown-formatted market analysis report

### Session Statistics
- **Path:** `GET /session-stats`
- **Parameters:**
  - `X-API-Key` (header): API key for authentication
- **Response:** Session statistics and request history

## Authentication

All endpoints except `/docs`, `/redoc`, and `/openapi.json` require authentication.

**API Key:** `trade-api-key-2024`

**How to use:**
```bash
curl -H "X-API-Key: trade-api-key-2024" http://localhost:8000/health
```

## Testing with Swagger UI

### Example: Test Health Check
1. Go to http://localhost:8000/docs
2. Find the "Health" section
3. Click on `GET /health`
4. Click "Try it out"
5. Click "Execute"
6. View the response

### Example: Test Analysis
1. Go to http://localhost:8000/docs
2. Find the "Analysis" section
3. Click on `GET /analyze/{sector}`
4. Click "Try it out"
5. Enter:
   - `sector`: "technology"
   - `X-API-Key`: "trade-api-key-2024"
   - `Client-ID`: "test-user" (optional)
6. Click "Execute"
7. View the markdown report

## Troubleshooting

### Documentation not loading
- Ensure API is running: `python main.py`
- Check that port 8000 is accessible
- Try a different browser
- Clear browser cache

### Getting 404 errors
- Verify the API is running
- Check the URL is correct (case-sensitive)
- Ensure you're using the correct port

### API key errors
- Use the correct API key: `trade-api-key-2024`
- Include it in the `X-API-Key` header
- Don't include it in the URL

## Importing into Tools

### Postman
1. Go to http://localhost:8000/openapi.json
2. Copy the entire JSON response
3. In Postman: File → Import → Paste Raw Text
4. All endpoints will be imported

### Insomnia
1. Create new request collection
2. Import from URL: `http://localhost:8000/openapi.json`
3. All endpoints will be available

### VS Code REST Client
```
@baseUrl = http://localhost:8000
@apiKey = trade-api-key-2024

### Health Check
GET {{baseUrl}}/health
X-API-Key: {{apiKey}}

### Analyze Technology
GET {{baseUrl}}/analyze/technology
X-API-Key: {{apiKey}}
Client-ID: test-user
```

## API Response Examples

### Health Check Response
```json
{
  "status": "healthy",
  "service": "Trade Opportunities API"
}
```

### Analysis Response (Markdown)
```markdown
# Market Analysis: Technology

## Executive Summary
The technology sector presents significant opportunities...

## Key Trends
- Cloud computing growth
- AI/ML adoption
- Cybersecurity demand

## Investment Opportunities
1. Cloud Infrastructure
2. AI/ML Solutions
3. Cybersecurity
```

## Next Steps

1. **Explore the API:** Visit http://localhost:8000/docs
2. **Test endpoints:** Use Swagger UI to try out the API
3. **Integrate:** Use the OpenAPI schema to integrate with your tools
4. **Deploy:** Follow deployment guidelines for production use

## Support

For issues or questions:
- Check the API logs for error messages
- Review the endpoint documentation in Swagger UI
- Verify API key and authentication headers
- Ensure all required parameters are provided
