"""
Product search service for searching across multiple e-commerce platforms.
"""
import asyncio
import time
from typing import List
from decimal import Decimal

from app.scrapers import ScraperFactory, ProductSearchResult
from app.schemas.product import ProductResult, SearchResults
from app.core.logging import get_logger
from app.core.exceptions import ScraperError, PlatformUnavailableError

logger = get_logger(__name__)


class ProductSearchService:
    """Service for searching products across multiple platforms."""
    
    SEARCH_TIMEOUT = 45  # seconds per platform (Selenium scraping takes 20-30s)
    
    def __init__(self):
        self.supported_platforms = ScraperFactory.get_supported_platforms()
    
    async def search_all_platforms(
        self,
        query: str,
        max_results_per_platform: int = 10,
        page: int = 1,
        sort_by: str = "best_match"
    ) -> SearchResults:
        """
        Search for products across all supported platforms concurrently.
        
        Args:
            query: Search query string
            max_results_per_platform: Maximum results to return per platform
            page: Page number (1-indexed)
            sort_by: Sort option - "best_match", "price_asc", or "price_desc"
        
        Returns:
            SearchResults with products from all platforms
        """
        start_time = time.time()
        
        logger.info(f"Searching all platforms for: {query} (page={page}, sort={sort_by})")
        
        # Create search tasks for all platforms
        search_tasks = []
        for platform in self.supported_platforms:
            task = self._search_platform_with_timeout(
                platform,
                query,
                max_results_per_platform,
                page,
                sort_by
            )
            search_tasks.append(task)
        
        # Execute all searches concurrently
        results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # Process results
        all_products = []
        platforms_searched = []
        platforms_failed = []
        total_count = 0
        
        for platform, result in zip(self.supported_platforms, results):
            platforms_searched.append(platform)
            
            if isinstance(result, Exception):
                logger.warning(f"Search failed for {platform}: {str(result)}")
                platforms_failed.append(platform)
            elif isinstance(result, tuple):
                # New format: (products, total_count)
                products, count = result
                total_count += count
                for product in products:
                    all_products.append(self._convert_to_product_result(product))
            elif isinstance(result, list):
                # Old format: just products list
                for product in result:
                    all_products.append(self._convert_to_product_result(product))
                total_count += len(result)
        
        search_time = time.time() - start_time
        
        logger.info(
            f"Search completed: {len(all_products)} products found "
            f"from {len(platforms_searched) - len(platforms_failed)} platforms "
            f"in {search_time:.2f}s"
        )
        
        return SearchResults(
            query=query,
            results=all_products,
            total_results=total_count,
            platforms_searched=platforms_searched,
            platforms_failed=platforms_failed,
            search_time_seconds=round(search_time, 2)
        )
    
    async def _search_platform_with_timeout(
        self,
        platform: str,
        query: str,
        max_results: int,
        page: int = 1,
        sort_by: str = "best_match"
    ) -> List[ProductSearchResult]:
        """
        Search a single platform with timeout.
        
        Args:
            platform: Platform name
            query: Search query
            max_results: Maximum results to return
            page: Page number
            sort_by: Sort option
        
        Returns:
            List of ProductSearchResult
        
        Raises:
            asyncio.TimeoutError: If search exceeds timeout
            ScraperError: If scraping fails
        """
        try:
            scraper = ScraperFactory.create_scraper(platform)
            
            # Execute search with timeout
            async with scraper:
                # Try calling with pagination parameters
                try:
                    results = await asyncio.wait_for(
                        scraper.search(query, max_results, page, sort_by),
                        timeout=self.SEARCH_TIMEOUT
                    )
                except TypeError:
                    # Scraper doesn't support pagination, use basic search
                    logger.info(f"Scraper {platform} doesn't support pagination")
                    results = await asyncio.wait_for(
                        scraper.search(query, max_results),
                        timeout=self.SEARCH_TIMEOUT
                    )
            
            return results
            
        except asyncio.TimeoutError:
            logger.warning(f"Search timeout for {platform} after {self.SEARCH_TIMEOUT}s")
            raise ScraperError(
                f"Search timeout after {self.SEARCH_TIMEOUT} seconds",
                platform=platform
            )
        except PlatformUnavailableError as e:
            logger.warning(f"Platform {platform} unavailable: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error searching {platform}: {str(e)}", exc_info=True)
            raise ScraperError(str(e), platform=platform)
    
    def _convert_to_product_result(self, product: ProductSearchResult) -> ProductResult:
        """
        Convert scraper ProductSearchResult to API ProductResult schema.
        
        Args:
            product: ProductSearchResult from scraper
        
        Returns:
            ProductResult schema
        """
        return ProductResult(
            platform=product.platform,
            product_url=product.product_url,
            product_name=product.product_name,
            current_price=product.current_price,
            currency=product.currency,
            image_url=product.image_url,
            availability=product.availability,
            scraped_at=product.scraped_at
        )
