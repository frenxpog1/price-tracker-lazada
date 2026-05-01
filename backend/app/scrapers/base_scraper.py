"""
Base scraper abstract class for e-commerce platforms.
Defines the interface that all platform-specific scrapers must implement.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

from app.core.logging import get_logger
from app.core.exceptions import ScraperError


logger = get_logger(__name__)


@dataclass
class ProductSearchResult:
    """
    Represents a product found during search.
    """
    platform: str
    product_url: str
    product_name: str
    current_price: Decimal
    currency: str
    image_url: Optional[str] = None
    availability: bool = True
    scraped_at: datetime = None
    
    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.utcnow()


@dataclass
class PriceCheckResult:
    """
    Represents the result of checking a product's current price.
    """
    product_url: str
    current_price: Optional[Decimal]
    currency: str
    availability: bool
    scraped_at: datetime = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.utcnow()


class BaseScraper(ABC):
    """
    Abstract base class for e-commerce platform scrapers.
    All platform-specific scrapers must extend this class.
    """
    
    def __init__(self, platform_name: str):
        """
        Initialize the scraper.
        
        Args:
            platform_name: Name of the e-commerce platform (e.g., "lazada", "shopee")
        """
        self.platform_name = platform_name
        self.logger = get_logger(f"{__name__}.{platform_name}")
    
    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> List[ProductSearchResult]:
        """
        Search for products on the platform.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
        
        Returns:
            List of ProductSearchResult objects
        
        Raises:
            ScraperError: If scraping fails
        """
        pass
    
    @abstractmethod
    async def get_current_price(self, product_url: str) -> PriceCheckResult:
        """
        Get the current price of a specific product.
        
        Args:
            product_url: URL of the product page
        
        Returns:
            PriceCheckResult object with current price information
        
        Raises:
            ScraperError: If scraping fails
        """
        pass
    
    def _handle_scraper_error(self, error: Exception, context: str) -> None:
        """
        Handle scraper errors with proper logging.
        
        Args:
            error: The exception that occurred
            context: Context description (e.g., "search", "price_check")
        
        Raises:
            ScraperError: Wrapped error with context
        """
        error_msg = f"{self.platform_name} scraper error during {context}: {str(error)}"
        self.logger.error(error_msg, exc_info=True)
        raise ScraperError(error_msg, platform=self.platform_name)
    
    def _validate_url(self, url: str) -> bool:
        """
        Validate that a URL belongs to this platform.
        
        Args:
            url: URL to validate
        
        Returns:
            True if URL is valid for this platform
        """
        # Basic validation - subclasses should override with platform-specific logic
        return url.startswith("http://") or url.startswith("https://")
    
    def _parse_price(self, price_str: str) -> Optional[Decimal]:
        """
        Parse price string to Decimal.
        Handles various formats like "₱1,234.56", "$1234.56", "1234.56"
        
        Args:
            price_str: Price string to parse
        
        Returns:
            Decimal price or None if parsing fails
        """
        try:
            # Remove currency symbols and whitespace
            cleaned = price_str.strip()
            
            # Remove common currency symbols
            for symbol in ['₱', '$', '€', '£', '¥', 'PHP', 'USD', 'EUR', 'GBP', 'JPY']:
                cleaned = cleaned.replace(symbol, '')
            
            # Remove commas (thousand separators)
            cleaned = cleaned.replace(',', '').strip()
            
            # Convert to Decimal
            return Decimal(cleaned)
        except Exception as e:
            self.logger.warning(f"Failed to parse price '{price_str}': {str(e)}")
            return None
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        # Subclasses can override to cleanup resources (e.g., close browser)
        pass
