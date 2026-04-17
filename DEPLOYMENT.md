# Deployment Guide - Trade Opportunities API

This guide covers deploying the Trade Opportunities API to production environments.

## Table of Contents

1. [Local Deployment](#local-deployment)
2. [Render Deployment](#render-deployment)
3. [Railway Deployment](#railway-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## Local Deployment

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd trade-opportunities-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

---

## Render Deployment

### Prerequisites

- Render account (https://render.com)
- GitHub repository with the code

### Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Render account**
   - Go to https://render.com
   - Sign up with GitHub

3. **Create new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

4. **Configure service**
   - **Name**: `trade-opportunities-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`

5. **Set environment variables**
   - Click "Environment"
   - Add variables:
     - `GEMINI_API_KEY`: Your Gemini API key
     - `VALID_API_KEYS`: Your API keys (comma-separated)

6. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy
   - Your API will be available at: `https://<service-name>.onrender.com`

### Render Configuration File (Optional)

Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: trade-opportunities-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port 8000
    envVars:
      - key: GEMINI_API_KEY
        scope: build,runtime
      - key: VALID_API_KEYS
        scope: build,runtime
```

### Render Deployment Tips

- **Free tier**: Limited to 0.5 CPU, 512MB RAM
- **Paid tier**: Better performance and reliability
- **Auto-deploy**: Automatically deploys on push to main branch
- **Logs**: View in Render dashboard

---

## Railway Deployment

### Prerequisites

- Railway account (https://railway.app)
- GitHub repository with the code

### Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Railway account**
   - Go to https://railway.app
   - Sign up with GitHub

3. **Create new project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

4. **Configure service**
   - Railway will auto-detect Python
   - Set start command in `railway.json`:

   ```json
   {
     "build": {
       "builder": "nixpacks"
     },
     "deploy": {
       "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT"
     }
   }
   ```

5. **Set environment variables**
   - Go to "Variables"
   - Add:
     - `GEMINI_API_KEY`: Your Gemini API key
     - `VALID_API_KEYS`: Your API keys

6. **Deploy**
   - Railway will automatically build and deploy
   - Your API will be available at the provided URL

### Railway Deployment Tips

- **Pricing**: Pay-as-you-go model
- **Auto-deploy**: Deploys on push to main branch
- **Logs**: Real-time logs in dashboard
- **Database**: Can add PostgreSQL if needed

---

## Docker Deployment

### Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - VALID_API_KEYS=${VALID_API_KEYS}
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t trade-api .

# Run container
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e VALID_API_KEYS=trade-api-key-2024 \
  trade-api

# Or use docker-compose
docker-compose up
```

---

## Environment Configuration

### Required Variables

```bash
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key

# Valid API Keys (comma-separated)
VALID_API_KEYS=trade-api-key-2024,key1,key2
```

### Optional Variables

```bash
# Logging level
LOG_LEVEL=INFO

# Application port (default: 8000)
PORT=8000

# Number of workers (for production)
WORKERS=4
```

### Getting Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to environment variables

---

## Production Deployment Best Practices

### 1. Use Environment Variables

Never hardcode sensitive information:

```python
# ✓ Good
api_key = os.getenv("GEMINI_API_KEY")

# ✗ Bad
api_key = "sk-1234567890"
```

### 2. Enable HTTPS

Use a reverse proxy (Nginx) or CDN:

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

### 3. Use Production ASGI Server

```bash
# Gunicorn with Uvicorn workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Or Uvicorn with multiple workers
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
```

### 4. Implement Monitoring

- Use application monitoring tools (e.g., Sentry, New Relic)
- Set up log aggregation (e.g., ELK Stack, Datadog)
- Monitor API response times and error rates

### 5. Set Up Rate Limiting

Already implemented in the application:
- 5 requests per minute per client
- Configurable in `main.py`

### 6. Enable CORS (if needed)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 7. Use Health Checks

Render and Railway support health checks:

```bash
# Health check endpoint
GET /health
```

### 8. Implement Logging

Already implemented with Python logging:
- Logs to console
- Includes timestamps and severity levels
- Can be configured to write to files

---

## Monitoring and Maintenance

### Health Monitoring

```bash
# Check API health
curl https://api.example.com/health

# Check session stats
curl -H "X-API-Key: your-key" https://api.example.com/session-stats
```

### Log Monitoring

Monitor these key events:
- API requests and responses
- Authentication failures
- Rate limit violations
- External API failures
- Errors and exceptions

### Performance Optimization

1. **Caching**: Implement caching for frequently requested sectors
2. **Database**: Consider adding PostgreSQL for persistent storage
3. **CDN**: Use CDN for static content
4. **Load Balancing**: Use load balancer for multiple instances

### Scaling

For high traffic:

1. **Horizontal Scaling**: Deploy multiple instances
2. **Load Balancing**: Use Nginx or cloud load balancer
3. **Caching**: Implement Redis for session/data caching
4. **Database**: Add PostgreSQL for persistent storage

---

## Troubleshooting

### Application won't start

```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port already in use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

### Gemini API not working

1. Verify API key is correct
2. Check API quota in Google Cloud Console
3. Verify network connectivity
4. Check API response in logs

### Rate limiting not working

1. Verify rate limiter is initialized in `main.py`
2. Check client ID is being passed correctly
3. Review rate limiter logic in `rate_limiter.py`

---

## Rollback Procedure

### Render

1. Go to Render dashboard
2. Select the service
3. Click "Deployments"
4. Select previous deployment
5. Click "Redeploy"

### Railway

1. Go to Railway dashboard
2. Select the service
3. Click "Deployments"
4. Select previous deployment
5. Click "Redeploy"

### Docker

```bash
# Tag previous image
docker tag trade-api:latest trade-api:v1.0.0

# Rollback to previous version
docker run -p 8000:8000 trade-api:v1.0.0
```

---

## Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test API locally first
4. Review deployment platform documentation

---

**Last Updated:** January 2024
**Version:** 1.0.0
