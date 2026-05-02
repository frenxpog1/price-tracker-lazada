"""
Lazada scraper that calls external Render API service.
This avoids running Selenium in Vercel's serverless environment.
"""
from typing import List, Tuple
from decimal import Decimal
import httpx
from datetime import datetime

from app.scrapers.base_scraper import (
    BaseScraper,
    ProductSearchResult,
    PriceCheckResult
)
from app.core.exceptions import ScraperError, PlatformUnavailableError
from app.config import settings


class LazadaAPIScraper(BaseScraper):
    """
    Lazada scraper that calls external Render API service.
    This is optimized for Vercel deployment where Selenium cannot run.
    """
    
    def __init__(self):
        super().__init__("lazada")
        self.api_url = settings.LAZADA_API_URL
        if not self.api_url:
            raise ValueError("LAZADA_API_URL environment variable is not set")
        
        # Remove trailing slash
        self.api_url = self.api_url.rstrip('/')
        
        self.logger.info(f"Initialized LazadaAPIScraper with API URL: {self.api_url}")
    
    async def __aenter__(self):
        """No initialization needed for API scraper."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """No cleanup needed for API scraper."""
        pass
    
    async def search(
        self, 
        query: str, 
        max_results: int = 20,
        page: int = 1,
        sort_by: str = "best_match"
    ) -> Tuple[List[ProductSearchResult], int]:
        """
        Search for products on Lazada via external API.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            page: Page number (1-indexed)
            sort_by: Sort option - "best_match", "price_asc", or "price_desc"
        
        Returns:
            Tuple of (List of ProductSearchResult objects, total count)
        """
        try:
            self.logger.info(f"Calling Lazada API: {query} (page={page}, sort={sort_by})")
            
            # Build API request
            params = {
                'q': query,
                'page': page,
                'per_page': max_results,
                'sort_by': sort_by
            }
            
            # Call external API
            async with httpx.AsyncClient(timeout=120.0) as client:  # 120 second timeout for slow Render
                response = await client.get(
                    f"{self.api_url}/search",
                    params=params
                )
                
                # Check response status
                if response.status_code == 503:
                    raise PlatformUnavailableError(
                        "Lazada API service is temporarily unavailable",
                        platform="lazada"
                    )
                elif response.status_code != 200:
                    raise ScraperError(
                        f"API returned status {response.status_code}: {response.text}",
                        platform="lazada"
                    )
                
                # Parse response
                data = response.json()
                
                # Convert API response to ProductSearchResult objects
                products = []
                for item in data.get('results', []):
                    try:
                        product = ProductSearchResult(
                            platform='lazada',
                            product_url=item['product_url'],
                            product_name=item['product_name'],
                            current_price=Decimal(str(item['current_price'])),
                            currency=item['currency'],
                            image_url=item.get('image_url'),
                            availability=item.get('availability', True),
                            scraped_at=datetime.fromisoformat(item['scraped_at']) if item.get('scraped_at') else datetime.utcnow()
                        )
                        products.append(product)
                    except Exception as e:
                        self.logger.warning(f"Failed to parse product: {e}")
                        continue
                
                total_count = data.get('total_results', len(products))
                
                self.logger.info(f"Successfully fetched {len(products)} products from Lazada API")
                return products, total_count
                
        except httpx.TimeoutException:
            self.logger.error("Lazada API request timeout")
            raise ScraperError("Request timeout", platform="lazada")
        except httpx.RequestError as e:
            self.logger.error(f"Lazada API request error: {e}")
            raise PlatformUnavailableError(
                f"Cannot connect to Lazada API: {str(e)}",
                platform="lazada"
            )
        except Exception as e:
            self.logger.error(f"Lazada API scraper error: {e}")
            self._handle_scraper_error(e, "search")
    
    async def get_current_price(self, product_url: str) -> PriceCheckResult:
        """
        Get the current price of a specific product.
        Note: This feature is not yet implemented in the external API.
        
        Args:
            product_url: URL of the product page
        
        Returns:
            PriceCheckResult object with current price information
        """
        # For now, return unavailable since the external API doesn't support this yet
        return PriceCheckResult(
            product_url=product_url,
            current_price=None,
            currency='PHP',
            availability=False,
            error="Price check not supported via API yet"
        )
    
    def _validate_url(self, url: str) -> bool:
        """Validate that a URL belongs to Lazada."""
        return 'lazada.com' in url.lower()
