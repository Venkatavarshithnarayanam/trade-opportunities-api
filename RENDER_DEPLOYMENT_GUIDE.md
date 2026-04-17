# Render Deployment Guide - Trade Opportunities API

## Overview

This guide provides step-by-step instructions to deploy the Trade Opportunities API to Render.

## Prerequisites

- Render account (https://render.com)
- GitHub repository with the project code
- Gemini API key (optional, but recommended)

## Step 1: Prepare Your Repository

### 1.1 Ensure Files Are Committed

Make sure these files are in your repository:
- `main.py` - Main application
- `requirements.txt` - Python dependencies
- `Procfile` - Deployment configuration
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore rules

### 1.2 Verify requirements.txt

```bash
pip freeze > requirements.txt
```

Ensure it contains:
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
google-generativeai==0.3.0
httpx==0.25.2
duckduckgo-search==3.9.10
```

### 1.3 Commit and Push

```bash
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

## Step 2: Create Render Service

### 2.1 Log In to Render

1. Go to https://render.com
2. Sign in with your account
3. Click "New +" button
4. Select "Web Service"

### 2.2 Connect GitHub Repository

1. Click "Connect a repository"
2. Select your GitHub account
3. Find and select your project repository
4. Click "Connect"

### 2.3 Configure Service

**Name:** `trade-opportunities-api`

**Environment:** `Python 3`

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:** `Free` (or `Starter` for better performance)

## Step 3: Set Environment Variables

### 3.1 Add Environment Variables

In the Render dashboard, go to "Environment" and add:

| Key | Value | Notes |
|-----|-------|-------|
| `PORT` | `8000` | Render assigns this automatically |
| `LOG_LEVEL` | `INFO` | Use `DEBUG` for troubleshooting |
| `GEMINI_API_KEY` | `your-key-here` | Optional - uses fallback if not set |
| `API_KEY` | `trade-api-key-2024` | Your API authentication key |

### 3.2 Save Environment Variables

Click "Save" to apply the environment variables.

## Step 4: Deploy

### 4.1 Start Deployment

1. Click "Create Web Service"
2. Render will automatically start building and deploying
3. Wait for the deployment to complete (usually 2-5 minutes)

### 4.2 Monitor Deployment

- Watch the "Logs" tab for build progress
- Look for "Application startup complete" message
- Check for any errors

### 4.3 Get Your Public URL

Once deployed, Render will provide a public URL like:
```
https://trade-opportunities-api.onrender.com
```

## Step 5: Verify Deployment

### 5.1 Test Health Endpoint

```bash
curl -H "X-API-Key: trade-api-key-2024" \
  https://trade-opportunities-api.onrender.com/health
```

Expected response:
```json
{"status":"healthy","service":"Trade Opportunities API"}
```

### 5.2 Access Swagger UI

Open in browser:
```
https://trade-opportunities-api.onrender.com/docs
```

### 5.3 Test Analysis Endpoint

```bash
curl -H "X-API-Key: trade-api-key-2024" \
  -H "Client-ID: test" \
  https://trade-opportunities-api.onrender.com/analyze/technology
```

## Step 6: Configure Custom Domain (Optional)

### 6.1 Add Custom Domain

1. Go to "Settings" in your Render service
2. Scroll to "Custom Domain"
3. Enter your domain (e.g., `api.yourdomain.com`)
4. Follow DNS configuration instructions

### 6.2 Update DNS Records

Add CNAME record pointing to your Render URL.

## Troubleshooting

### Build Fails

**Check logs:**
- Go to "Logs" tab
- Look for error messages
- Common issues:
  - Missing dependencies in requirements.txt
  - Python version incompatibility
  - Syntax errors in code

**Fix:**
```bash
# Update requirements.txt
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### Application Won't Start

**Check logs for:**
- Import errors
- Missing environment variables
- Port binding issues

**Common fixes:**
- Ensure `LOG_LEVEL` is set to `INFO` or `DEBUG`
- Verify all environment variables are set
- Check that `Procfile` is correct

### Slow Response Times

**Possible causes:**
- Free tier instance is limited
- DuckDuckGo search is slow
- Gemini API is slow

**Solutions:**
- Upgrade to Starter tier
- Set `GEMINI_API_KEY` for faster AI analysis
- Implement caching

### API Key Not Working

**Check:**
- Verify `API_KEY` environment variable is set
- Ensure header is `X-API-Key: your-key`
- Check for typos in the key

## Production Best Practices

### 1. Security

- Use strong API keys
- Restrict CORS origins in production
- Use HTTPS (Render provides this automatically)
- Keep dependencies updated

### 2. Monitoring

- Enable Render's monitoring
- Set up error alerts
- Monitor response times
- Track API usage

### 3. Performance

- Use Starter tier or higher for production
- Enable caching if possible
- Monitor database connections
- Optimize queries

### 4. Maintenance

- Regularly update dependencies
- Monitor logs for errors
- Test new versions before deploying
- Keep backups of configuration

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8001` | Server port (Render sets this) |
| `LOG_LEVEL` | `INFO` | Logging level |
| `GEMINI_API_KEY` | None | Gemini API key (optional) |
| `API_KEY` | `trade-api-key-2024` | API authentication key |

## API Endpoints

Once deployed, access your API at:

| Endpoint | URL |
|----------|-----|
| Health Check | `https://your-domain.onrender.com/health` |
| Swagger UI | `https://your-domain.onrender.com/docs` |
| ReDoc | `https://your-domain.onrender.com/redoc` |
| OpenAPI Schema | `https://your-domain.onrender.com/openapi.json` |
| Analysis | `https://your-domain.onrender.com/analyze/{sector}` |

## Support

For issues:
1. Check Render logs
2. Review this guide
3. Check API documentation at `/docs`
4. Verify environment variables are set correctly

## Next Steps

1. Deploy to Render following this guide
2. Test all endpoints
3. Monitor logs for errors
4. Set up custom domain if needed
5. Configure monitoring and alerts

Your Trade Opportunities API is now production-ready on Render!
