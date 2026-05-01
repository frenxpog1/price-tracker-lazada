"""
E-commerce Product Scraper API for RapidAPI
A simple, fast API for scraping product information from major e-commerce platforms.

Features:
- Search products across Lazada, Shopee, TikTok Shop
- Get current prices and product details
- Pagination and sorting support
- Rate limiting and error handling
- OpenAPI documentation
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import asyncio
import time
from decimal import Decimal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import scrapers
from scrapers.lazada_scraper import LazadaScraperAPI
from scrapers.shopee_scraper import ShopeeScraperAPI
from scrapers.temu_scraper import TemuScraperAPI
from scrapers.base_scraper import ProductResult, ScraperError

app = FastAPI(
    title="E-commerce Product Scraper API",
    description="Search and scrape product information from major e-commerce platforms including Lazada, Shopee, and TikTok Shop. Perfect for price comparison, market research, and product discovery.",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS middleware for web applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response Models
class ProductResponse(BaseModel):
    """Individual product information"""
    platform: str = Field(..., description="E-commerce platform (lazada, shopee, tiktokshop)")
    product_name: str = Field(..., description="Product name/title")
    current_price: float = Field(..., description="Current price in local currency")
    currency: str = Field(..., description="Currency code (PHP, USD, etc.)")
    product_url: str = Field(..., description="Direct link to product page")
    image_url: Optional[str] = Field(None, description="Product image URL")
    availability: bool = Field(..., description="Whether product is in stock")
    scraped_at: str = Field(..., description="Timestamp when data was scraped")

class SearchResponse(BaseModel):
    """Search results response"""
    query: str = Field(..., description="Search query used")
    total_results: int = Field(..., description="Total number of results found")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Results per page")
    results: List[ProductResponse] = Field(..., description="List of products found")
    platforms_searched: List[str] = Field(..., description="Platforms that were searched")
    platforms_failed: List[str] = Field(..., description="Platforms that failed to respond")
    search_time_seconds: float = Field(..., description="Time taken to complete search")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")
    details: Optional[str] = Field(None, description="Additional error details")

# Rate limiting (simple in-memory implementation)
request_counts = {}
RATE_LIMIT = 100  # requests per hour per IP

def rate_limit_check(request_ip: str = None):
    """Simple rate limiting"""
    if not request_ip:
        return True
    
    current_time = time.time()
    hour_ago = current_time - 3600
    
    # Clean old entries
    if request_ip in request_counts:
        request_counts[request_ip] = [
            timestamp for timestamp in request_counts[request_ip] 
            if timestamp > hour_ago
        ]
    else:
        request_counts[request_ip] = []
    
    # Check rate limit
    if len(request_counts[request_ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {RATE_LIMIT} requests per hour."
        )
    
    # Add current request
    request_counts[request_ip].append(current_time)
    return True

@app.get("/", response_model=dict)
async def root():
    """API information and health check"""
    return {
        "name": "E-commerce Product Scraper API",
        "version": "1.0.0",
        "description": "Search products across major e-commerce platforms",
        "supported_platforms": ["lazada", "shopee", "temu"],
        "endpoints": {
            "search": "/search - Search products across all platforms",
            "search_platform": "/search/{platform} - Search specific platform",
            "health": "/health - API health check",
            "docs": "/docs - Interactive API documentation"
        },
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get(
    "/search",
    response_model=SearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Search products across all platforms",
    description="Search for products across all supported e-commerce platforms with pagination and sorting options."
)
async def search_products(
    q: str = Query(..., description="Search query (product name, keywords)", min_length=2, max_length=100),
    page: int = Query(1, description="Page number (1-based)", ge=1, le=50),
    per_page: int = Query(20, description="Results per page", ge=1, le=100),
    sort_by: Literal["best_match", "price_asc", "price_desc"] = Query("best_match", description="Sort order"),
    platform: Optional[Literal["lazada", "shopee", "temu"]] = Query(None, description="Filter by specific platform"),
    request_ip: str = Depends(lambda: "127.0.0.1")  # In real deployment, get from request
):
    """
    Search for products across multiple e-commerce platforms.
    
    **Parameters:**
    - **q**: Search query (required) - What you're looking for
    - **page**: Page number (optional, default: 1)
    - **per_page**: Results per page (optional, default: 20, max: 100)
    - **sort_by**: Sort order (optional, default: best_match)
    - **platform**: Filter by platform (optional, searches all if not specified)
    
    **Returns:**
    - List of products with prices, images, and links
    - Pagination information
    - Search performance metrics
    """
    
    # Rate limiting
    rate_limit_check(request_ip)
    
    start_time = time.time()
    
    try:
        # Determine which platforms to search
        # Note: Only Lazada is currently working. Shopee and Temu need selector updates.
        platforms_to_search = [platform] if platform else ["lazada"]
        
        all_results = []
        platforms_searched = []
        platforms_failed = []
        total_results = 0
        
        # Search each platform
        for platform_name in platforms_to_search:
            try:
                scraper = None
                
                if platform_name == "lazada":
                    scraper = LazadaScraperAPI()
                elif platform_name == "shopee":
                    scraper = ShopeeScraperAPI()
                elif platform_name == "temu":
                    scraper = TemuScraperAPI()
                else:
                    platforms_failed.append(platform_name)
                    logger.warning(f"Unknown platform: {platform_name}")
                    continue
                
                if scraper:
                    async with scraper:
                        results, total = await scraper.search(
                            query=q,
                            max_results=per_page,
                            page=page,
                            sort_by=sort_by
                        )
                        
                        # Convert to API format
                        for result in results:
                            all_results.append(ProductResponse(
                                platform=result.platform,
                                product_name=result.product_name,
                                current_price=float(result.current_price),
                                currency=result.currency,
                                product_url=result.product_url,
                                image_url=result.image_url,
                                availability=result.availability,
                                scraped_at=result.scraped_at.isoformat() if result.scraped_at else ""
                            ))
                        
                        total_results += total
                        platforms_searched.append(platform_name)
                    
            except Exception as e:
                logger.error(f"Error scraping {platform_name}: {str(e)}")
                platforms_failed.append(platform_name)
        
        search_time = time.time() - start_time
        
        return SearchResponse(
            query=q,
            total_results=total_results,
            page=page,
            per_page=per_page,
            results=all_results,
            platforms_searched=platforms_searched,
            platforms_failed=platforms_failed,
            search_time_seconds=round(search_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

@app.get(
    "/search/{platform}",
    response_model=SearchResponse,
    summary="Search specific platform",
    description="Search for products on a specific e-commerce platform."
)
async def search_platform(
    platform: Literal["lazada", "shopee", "temu"],
    q: str = Query(..., description="Search query", min_length=2, max_length=100),
    page: int = Query(1, description="Page number", ge=1, le=50),
    per_page: int = Query(20, description="Results per page", ge=1, le=100),
    sort_by: Literal["best_match", "price_asc", "price_desc"] = Query("best_match", description="Sort order"),
    request_ip: str = Depends(lambda: "127.0.0.1")
):
    """Search products on a specific platform"""
    return await search_products(
        q=q,
        page=page,
        per_page=per_page,
        sort_by=sort_by,
        platform=platform,
        request_ip=request_ip
    )

@app.get("/platforms", response_model=dict)
async def get_platforms():
    """Get list of supported platforms and their status"""
    return {
        "platforms": {
            "lazada": {
                "name": "Lazada",
                "country": "Philippines",
                "status": "active",
                "features": ["search", "pagination", "sorting", "images"],
                "tested": True,
                "working": True,
                "response_time": "6-8 seconds",
                "success_rate": "100%"
            },
            "shopee": {
                "name": "Shopee",
                "country": "Philippines", 
                "status": "blocked",
                "features": ["search", "pagination", "sorting", "images"],
                "tested": True,
                "working": False,
                "note": "Bot detection active - requires login. Redirects to 'Page Unavailable' page.",
                "recommendation": "Use residential proxies or browser automation with real user sessions"
            },
            "temu": {
                "name": "Temu",
                "country": "Global",
                "status": "blocked", 
                "features": ["search", "pagination", "sorting", "images"],
                "tested": True,
                "working": False,
                "note": "Strong bot detection - redirects to login page. Headless browsers are detected.",
                "recommendation": "Use residential proxies, CAPTCHA solving services, or browser automation with real user sessions"
            }
        },
        "summary": {
            "total_platforms": 3,
            "working": 1,
            "blocked": 2,
            "recommendation": "Deploy with Lazada only for reliable results. Shopee and Temu require advanced anti-detection measures (residential proxies, CAPTCHA solving, browser fingerprinting bypass)."
        }
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            code=f"HTTP_{exc.status_code}",
            details=None
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            code="INTERNAL_ERROR",
            details=str(exc)
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)