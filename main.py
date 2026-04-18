"""
Trade Opportunities API - Main Entry Point
FastAPI service for analyzing market data and generating trade opportunity insights
"""

import logging
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not required, but recommended

# Determine log level from environment (default: INFO for production)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logging FIRST before any imports
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Only show initialization logs in DEBUG mode
if LOG_LEVEL == "DEBUG":
    logger.info("=" * 80)
    logger.info("Trade Opportunities API - Initializing")
    logger.info("=" * 80)

# Import components with error handling
try:
    if LOG_LEVEL == "DEBUG":
        logger.info("Importing auth module...")
    from auth import verify_api_key
    if LOG_LEVEL == "DEBUG":
        logger.info("✓ Auth module imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import auth module: {str(e)}", exc_info=True)
    sys.exit(1)

try:
    if LOG_LEVEL == "DEBUG":
        logger.info("Importing rate_limiter module...")
    from rate_limiter import RateLimiter
    if LOG_LEVEL == "DEBUG":
        logger.info("✓ Rate limiter module imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import rate_limiter module: {str(e)}", exc_info=True)
    sys.exit(1)

try:
    if LOG_LEVEL == "DEBUG":
        logger.info("Importing session_manager module...")
    from session_manager import SessionManager
    if LOG_LEVEL == "DEBUG":
        logger.info("✓ Session manager module imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import session_manager module: {str(e)}", exc_info=True)
    sys.exit(1)

try:
    if LOG_LEVEL == "DEBUG":
        logger.info("Importing data_collector service...")
    from services.data_collector import DataCollector
    if LOG_LEVEL == "DEBUG":
        logger.info("✓ Data collector service imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import data_collector service: {str(e)}", exc_info=True)
    sys.exit(1)

try:
    if LOG_LEVEL == "DEBUG":
        logger.info("Importing ai_analyzer service...")
    from services.ai_analyzer import AIAnalyzer
    if LOG_LEVEL == "DEBUG":
        logger.info("✓ AI analyzer service imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import ai_analyzer service: {str(e)}", exc_info=True)
    sys.exit(1)

try:
    if LOG_LEVEL == "DEBUG":
        logger.info("Importing markdown_formatter utility...")
    from utils.markdown_formatter import MarkdownFormatter
    if LOG_LEVEL == "DEBUG":
        logger.info("✓ Markdown formatter utility imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import markdown_formatter utility: {str(e)}", exc_info=True)
    sys.exit(1)

# Initialize components with error handling
if LOG_LEVEL == "DEBUG":
    logger.info("Initializing components...")

try:
    if LOG_LEVEL == "DEBUG":
        logger.info("Initializing rate limiter...")
    rate_limiter = RateLimiter(max_requests=5, window_seconds=60)
    if LOG_LEVEL == "DEBUG":
        logger.info("✓ Rate limiter initialized")
except Exception as e:
    logger.error(f"✗ Failed to initialize rate limiter: {str(e)}", exc_info=True)
    sys.exit(1)

try:
    if LOG_LEVEL == "DEBUG":
        logger.info("Initializing session manager...")
    session_manager = SessionManager()
    if LOG_LEVEL == "DEBUG":
        logger.info("✓ Session manager initialized")
except Exception as e:
    logger.error(f"✗ Failed to initialize session manager: {str(e)}", exc_info=True)
    sys.exit(1)

try:
    if LOG_LEVEL == "DEBUG":
        logger.info("Initializing data collector...")
    data_collector = DataCollector()
    if LOG_LEVEL == "DEBUG":
        logger.info("✓ Data collector initialized")
except Exception as e:
    logger.error(f"✗ Failed to initialize data collector: {str(e)}", exc_info=True)
    sys.exit(1)

try:
    if LOG_LEVEL == "DEBUG":
        logger.info("Initializing AI analyzer...")
    ai_analyzer = AIAnalyzer()
    if LOG_LEVEL == "DEBUG":
        logger.info("✓ AI analyzer initialized")
except Exception as e:
    logger.error(f"✗ Failed to initialize AI analyzer: {str(e)}", exc_info=True)
    sys.exit(1)

try:
    if LOG_LEVEL == "DEBUG":
        logger.info("Initializing markdown formatter...")
    markdown_formatter = MarkdownFormatter()
    if LOG_LEVEL == "DEBUG":
        logger.info("✓ Markdown formatter initialized")
except Exception as e:
    logger.error(f"✗ Failed to initialize markdown formatter: {str(e)}", exc_info=True)
    sys.exit(1)

if LOG_LEVEL == "DEBUG":
    logger.info("=" * 80)
    logger.info("All components initialized successfully!")
    logger.info("=" * 80)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    logger.info("=" * 80)
    logger.info("Trade Opportunities API - Startup Complete")
    logger.info("=" * 80)
    logger.info("API is ready to accept requests")
    logger.info("Health check: GET /health")
    logger.info("API Docs: GET /docs")
    logger.info("=" * 80)
    yield
    logger.info("=" * 80)
    logger.info("Trade Opportunities API - Shutting down")
    logger.info("=" * 80)


app = FastAPI(
    title="Trade Opportunities API",
    description="Analyze market data and generate trade opportunity insights for sectors",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Valid sectors for analysis
VALID_SECTORS = ["pharmaceuticals", "technology", "agriculture", "healthcare", "finance", "energy"]


class AnalysisRequest(BaseModel):
    """Request model for analysis endpoint"""
    sector: str = Field(..., min_length=1, max_length=50, pattern="^[a-zA-Z\\s]+$")


class AnalysisResponse(BaseModel):
    """Response model for analysis endpoint"""
    sector: str
    report: str
    status: str = "success"


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Trade Opportunities API"}


@app.get("/analyze/{sector}", response_class=PlainTextResponse, tags=["Analysis"])
async def analyze_sector(
    sector: str,
    x_api_key: str = Header(...),
    client_id: str = Header(default="anonymous")
):
    """
    Analyze market opportunities for a given sector.
    
    Args:
        sector: The sector to analyze (pharmaceuticals, technology, agriculture, healthcare, finance, energy)
        x_api_key: API key for authentication (required header)
        client_id: Optional client identifier for session tracking
    
    Returns:
        Markdown formatted market analysis report
    
    Raises:
        HTTPException: For invalid input, authentication failure, or rate limit exceeded
    """
    try:
        logger.info(f"[REQUEST] New analysis request for sector: {sector} from client: {client_id}")
        
        # Validate API key
        if not verify_api_key(x_api_key):
            logger.warning(f"[AUTH] ✗ Unauthorized access attempt with invalid API key from {client_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        logger.info(f"[AUTH] ✓ API key validated for client: {client_id}")
        
        # Normalize and validate sector
        sector_normalized = sector.strip().lower()
        
        if sector_normalized not in VALID_SECTORS:
            logger.warning(f"[VALIDATION] ✗ Invalid sector input: {sector}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sector. Please use a valid sector like {', '.join(VALID_SECTORS)}"
            )
        
        sector = sector_normalized
        logger.info(f"[VALIDATION] ✓ Sector input validated: {sector}")
        
        # Check rate limit
        if not rate_limiter.is_allowed(client_id):
            logger.warning(f"[RATELIMIT] ✗ Rate limit exceeded for client: {client_id}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded: Maximum 5 requests per minute"
            )
        
        logger.info(f"[RATELIMIT] ✓ Rate limit check passed for client: {client_id}")
        
        # Track session
        session_manager.track_request(client_id, sector)
        logger.info(f"[SESSION] ✓ Request tracked for client: {client_id}")
        
        logger.info(f"[PIPELINE] Starting analysis pipeline for sector: {sector}")
        
        # Collect market data
        logger.info(f"[PIPELINE] Step 1/3: Collecting market data...")
        market_data = await data_collector.collect_data(sector)
        logger.info(f"[PIPELINE] ✓ Step 1 complete: Collected {len(market_data)} data items")
        
        # Analyze with AI
        logger.info(f"[PIPELINE] Step 2/3: Running AI analysis...")
        analysis = await ai_analyzer.analyze(sector, market_data)
        logger.info(f"[PIPELINE] ✓ Step 2 complete: Analysis generated")
        
        # Format as markdown
        logger.info(f"[PIPELINE] Step 3/3: Formatting markdown report...")
        report = markdown_formatter.format_report(sector, analysis)
        logger.info(f"[PIPELINE] ✓ Step 3 complete: Report formatted ({len(report)} bytes)")
        
        logger.info(f"[SUCCESS] ✓ Analysis complete for sector: {sector} (client: {client_id})")
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] ✗ Unexpected error during analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during analysis"
        )


@app.get("/session-stats", tags=["Session"])
async def get_session_stats(x_api_key: str = Header(...)):
    """Get session statistics (requires authentication)"""
    if not verify_api_key(x_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return session_manager.get_stats()


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable or use default (8001 to avoid Splunk on 8000)
    port = int(os.getenv("PORT", 8001))
    
    logger.info("=" * 80)
    logger.info(f"Starting API on port {port}")
    logger.info(f"API URL: http://localhost:{port}")
    logger.info(f"API Docs: http://localhost:{port}/docs")
    logger.info("=" * 80)
    
    # Run uvicorn with the specified port
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
