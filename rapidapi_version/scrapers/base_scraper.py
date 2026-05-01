"""
Base scraper classes for RapidAPI version.
Simplified version without database dependencies.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class ProductResult(BaseModel):
    """Product search result"""
    platform: str
    product_name: str
    current_price: Decimal
    currency: str
    product_url: str
    image_url: Optional[str] = None
    availability: bool = True
    scraped_at: Optional[datetime] = None

class ScraperError(Exception):
    """Custom exception for scraper errors"""
    def __init__(self, message: str, platform: str = None, status_code: int = None):
        self.message = message
        self.platform = platform
        self.status_code = status_code
        super().__init__(self.message)

class BaseScraper(ABC):
    """Base class for all e-commerce scrapers"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.logger = logging.getLogger(f"{__name__}.{platform_name}")
    
    @abstractmethod
    async def search(
        self, 
        query: str, 
        max_results: int = 20,
        page: int = 1,
        sort_by: str = "best_match"
    ) -> Tuple[List[ProductResult], int]:
        """
        Search for products on the platform.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            page: Page number (1-indexed)
            sort_by: Sort option
        
        Returns:
            Tuple of (List of ProductResult objects, total count)
        """
        pass
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        pass
    
    def _handle_scraper_error(self, error: Exception, operation: str):
        """Handle and log scraper errors"""
        error_msg = f"{self.platform_name} {operation} error: {str(error)}"
        self.logger.error(error_msg)
        
        if "timeout" in str(error).lower():
            raise ScraperError(f"Request timeout for {self.platform_name}", self.platform_name, 408)
        elif "connection" in str(error).lower():
            raise ScraperError(f"Connection error for {self.platform_name}", self.platform_name, 503)
        else:
            raise ScraperError(error_msg, self.platform_name, 500)