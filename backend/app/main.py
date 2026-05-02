"""
Main FastAPI application entry point.
Configures the application, middleware, and routes.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import time
import uuid
import traceback

from app.config import settings
from app.core.logging import get_logger
from app.core.exceptions import PriceTrackerException

# Initialize logger
logger = get_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Track product prices across multiple e-commerce platforms",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log all incoming requests and outgoing responses.
    Adds request ID for tracing.
    """
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    logger.info(
        "Incoming request",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else "unknown"
        }
    )
    
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2)
            }
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
    except Exception as exc:
        duration = time.time() - start_time
        logger.error(
            "Request failed",
            extra={
                "request_id": request_id,
                "error": str(exc),
                "duration_ms": round(duration * 1000, 2)
            },
            exc_info=True
        )
        raise


# Global Exception Handler
@app.exception_handler(PriceTrackerException)
async def price_tracker_exception_handler(request: Request, exc: PriceTrackerException):
    """Handle custom application exceptions."""
    logger.error(
        "Application error",
        extra={
            "request_id": getattr(request.state, "request_id", "N/A"),
            "error_code": exc.code,
            "error_message": exc.message,
            "path": request.url.path
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": getattr(request.state, "request_id", "N/A")
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    logger.warning(
        "Validation error",
        extra={
            "request_id": getattr(request.state, "request_id", "N/A"),
            "errors": exc.errors(),
            "path": request.url.path
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": exc.errors(),
                "request_id": getattr(request.state, "request_id", "N/A")
            }
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    logger.error(
        "Unhandled exception",
        extra={
            "request_id": getattr(request.state, "request_id", "N/A"),
            "error": str(exc),
            "error_type": type(exc).__name__,
            "path": request.url.path,
            "traceback": traceback.format_exc()
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "request_id": getattr(request.state, "request_id", "N/A")
            }
        }
    )


# Health Check Endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    Returns application status and version.
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Root Endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "E-commerce Price Tracker API",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production"
    }


# Debug Endpoints (only in development)
if settings.DEBUG:
    @app.get("/debug/scrapers/{platform}/test", tags=["Debug"])
    async def test_scraper(platform: str, query: str):
        """
        Test a specific scraper in isolation.
        Only available in development mode.
        """
        # TODO: Implement in Task 5 (Web Scraping)
        return {
            "message": "Scraper testing not yet implemented",
            "platform": platform,
            "query": query
        }
    
    @app.get("/debug/database/health", tags=["Debug"])
    async def database_health():
        """
        Check database connection and status.
        Only available in development mode.
        """
        # TODO: Implement database health check
        return {
            "message": "Database health check not yet implemented"
        }
    
    @app.post("/debug/notifications/test", tags=["Debug"])
    async def test_notification(email: str):
        """
        Send a test notification email.
        Only available in development mode.
        """
        # TODO: Implement in Task 11 (Notifications)
        return {
            "message": "Notification testing not yet implemented",
            "email": email
        }


# Application Startup Event
@app.on_event("startup")
async def startup_event():
    """
    Run on application startup.
    Initialize database, logging, etc.
    """
    logger.info(
        "Application starting",
        extra={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "debug": settings.DEBUG
        }
    )
    
    # Initialize database tables if they don't exist
    try:
        from app.core.database import Base, engine
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")


# Application Shutdown Event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown.
    Clean up resources.
    """
    logger.info("Application shutting down")


# Include API routers
from app.api import auth, products, tracking, proxy
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(tracking.router, prefix="/api/tracking", tags=["Tracking"])
app.include_router(proxy.router, prefix="/api/proxy", tags=["Proxy"])
# from app.api import users
# app.include_router(users.router, prefix="/api/users", tags=["Users"])
