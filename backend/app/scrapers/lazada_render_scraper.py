"""
Lazada scraper that calls external Render API service.
This is used for Vercel deployment since Vercel doesn't support Selenium.
"""

from typing import List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
import httpx

from .base_scraper import BaseScraper, ProductSearchResult, PriceCheckResult, ScraperError
from app.core.logging import get_logger
from app.config import settings

logger = get_logger(__name__)


class LazadaRenderScraper(BaseScraper):
    """
    Lazada scraper that calls external Render API service.
    The Render service runs the Selenium scraper and returns results via REST API.
    """
    
    def __init__(self):
        super().__init__("lazada")
        self.api_url = settings.LAZADA_API_URL
        
        if not self.api_url:
            raise ValueError(
                "LAZADA_API_URL not configured. "
                "Please set it in your .env file to your Render service URL."
            )
        
        # Remove trailing slash
        self.api_url = self.api_url.rstrip('/')
        
        logger.info(f"Lazada Render scraper initialized with API: {self.api_url}")
    
    async def __aenter__(self):
        """Initialize HTTP client."""
        self.client = httpx.AsyncClient(timeout=60.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup HTTP client."""
        if hasattr(self, 'client'):
            await self.client.aclose()
    
    async def search(
        self,
        query: str,
        max_results: int = 20,
        page: int = 1,
        sort_by: str = "best_match"
    ) -> Tuple[List[ProductSearchResult], int]:
        """
        Search for products by calling the Render API.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            page: Page number (1-indexed)
            sort_by: Sort option - "best_match", "price_asc", or "price_desc"
        
        Returns:
            Tuple of (List of ProductSearchResult objects, total count)
        """
        try:
            self.logger.info(
                f"Calling Render API: {query} (page={page}, sort={sort_by}, max={max_results})"
            )
            
            # Call Render API
            response = await self.client.get(
                f"{self.api_url}/search",
                params={
                    "q": query,
                    "page": page,
                    "per_page": max_results,
                    "sort_by": sort_by
                }
            )
            
            # Check response status
            if response.status_code != 200:
                error_msg = f"Render API returned status {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', error_data)}"
                except:
                    error_msg += f": {response.text}"
                
                self.logger.error(error_msg)
                raise ScraperError(error_msg, "lazada", response.status_code)
            
            # Parse response
            data = response.json()
            
            # Extract results
            results = data.get("results", [])
            total_count = data.get("total_results", 0)
            
            # Convert to ProductSearchResult objects
            products = []
            for item in results:
                try:
                    # Parse scraped_at timestamp
                    scraped_at = datetime.fromisoformat(
                        item["scraped_at"].replace("Z", "+00:00")
                    )
                    
                    products.append(ProductSearchResult(
                        platform="lazada",
                        product_url=item["product_url"],
                        product_name=item["product_name"],
                        current_price=Decimal(str(item["current_price"])),
                        currency=item.get("currency", "PHP"),
                        image_url=item.get("image_url"),
                        availability=item.get("availability", True),
                        scraped_at=scraped_at
                    ))
                except Exception as e:
                    self.logger.warning(f"Failed to parse product: {e}")
                    continue
            
            self.logger.info(
                f"Render API returned {len(products)} products (total={total_count})"
            )
            
            return products, total_count
            
        except httpx.TimeoutException:
            self.logger.error("Render API timeout")
            raise ScraperError("Request timeout to Render API", "lazada", 408)
        except httpx.RequestError as e:
            self.logger.error(f"Render API request error: {e}")
            raise ScraperError(f"Failed to connect to Render API: {str(e)}", "lazada", 503)
        except Exception as e:
            self.logger.error(f"Render API scraper error: {e}")
            self._handle_scraper_error(e, "search")
    
    async def get_current_price(self, product_url: str) -> PriceCheckResult:
        """
        Get current price for a specific product URL.
        
        Note: This would require a separate endpoint on the Render API.
        For now, we'll return a not implemented error.
        """
        self.logger.warning("get_current_price not implemented for Render API scraper")
        return PriceCheckResult(
            product_url=product_url,
            current_price=None,
            currency="PHP",
            availability=False,
            error="Price check not implemented for Render API scraper"
        )
