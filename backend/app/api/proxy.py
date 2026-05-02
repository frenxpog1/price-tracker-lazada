"""
CORS proxy endpoint for client-side scraping.
Allows frontend to fetch Lazada pages without CORS issues.
"""
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import Response
import httpx

from app.dependencies import get_current_user_id
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/lazada")
async def proxy_lazada(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, description="Page number"),
    sortBy: str = Query(None, description="Sort option"),
    user_id: str = None  # Optional auth - allow unauthenticated for faster response
):
    """
    Proxy endpoint to fetch Lazada search pages.
    This bypasses CORS restrictions for client-side scraping.
    
    - **q**: Search query (required)
    - **page**: Page number (default 1)
    - **sortBy**: Sort option (optional: priceasc, pricedesc)
    
    Returns the raw HTML from Lazada search page.
    """
    try:
        # Build Lazada URL
        params = {'q': q, 'page': page}
        if sortBy:
            params['sortBy'] = sortBy
        
        url_params = '&'.join([f"{k}={v}" for k, v in params.items()])
        lazada_url = f"https://www.lazada.com.ph/catalog/?{url_params}"
        
        logger.info(f"Proxying Lazada request: {lazada_url}")
        
        # Fetch from Lazada
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                lazada_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Lazada returned status {response.status_code}"
                )
            
            # Return HTML with CORS headers
            return Response(
                content=response.text,
                media_type="text/html",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "*",
                }
            )
            
    except httpx.TimeoutException:
        logger.error("Timeout fetching from Lazada")
        raise HTTPException(status_code=504, detail="Request timeout")
    except Exception as e:
        logger.error(f"Proxy error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
