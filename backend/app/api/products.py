"""
Product search API endpoints.
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status

from app.schemas.product import SearchResults
from app.services.search_service import ProductSearchService
from app.dependencies import get_current_user_id, get_optional_current_user_id
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/search", response_model=SearchResults)
async def search_products(
    q: str = Query(..., min_length=1, description="Search query"),
    max_results: int = Query(40, ge=1, le=100, description="Maximum results per platform"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    sort_by: str = Query("best_match", description="Sort: best_match, price_asc, price_desc"),
    user_id: str = Depends(get_optional_current_user_id)
):
    """
    Search for products across all supported e-commerce platforms.
    
    - **q**: Search query (required)
    - **max_results**: Maximum results per platform (1-100, default 40)
    - **page**: Page number for pagination (default 1)
    - **sort_by**: Sort option - best_match, price_asc, price_desc
    
    Returns search results from Lazada, Shopee, and TikTok Shop.
    Requires authentication.
    """
    logger.info(f"User {user_id} searching for: {q} (page={page}, sort={sort_by})")
    
    search_service = ProductSearchService()
    results = await search_service.search_all_platforms(q, max_results, page, sort_by)
    
    return results
