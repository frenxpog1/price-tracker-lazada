"""
Scraper factory for creating platform-specific scrapers.
"""
from typing import Dict, Type

from app.scrapers.base_scraper import BaseScraper
from app.core.exceptions import ValidationError
from app.core.logging import get_logger
from app.config import settings


logger = get_logger(__name__)


class ScraperFactory:
    """
    Factory class for creating platform-specific scrapers.
    Only real scrapers are supported - no mock data.
    """
    
    # Registry of real scrapers
    _real_scrapers: Dict[str, Type[BaseScraper]] = {}
    
    @classmethod
    def _load_real_scrapers(cls):
        """Lazy load real scrapers to avoid import errors if dependencies missing."""
        if not cls._real_scrapers:
            # Load Lazada scraper based on configuration
            # If LAZADA_API_URL is set, use Render API scraper (for Vercel deployment)
            # Otherwise, use local Selenium scraper (for local development)
            try:
                from app.scrapers.lazada_scrapling_scraper import LazadaScraplingScraper
                cls._real_scrapers["lazada"] = LazadaScraplingScraper
                logger.info("✅ Loaded LazadaScraplingScraper (Scrapling with Camoufox)")
            except ImportError as e:
                logger.error(f"❌ Could not load LazadaScraplingScraper: {e}")
            
            # Shopee and TikTok Shop scrapers not yet implemented
            logger.info("⚠️  Shopee scraper: Not implemented yet")
            logger.info("⚠️  TikTok Shop scraper: Not implemented yet")
    
    @classmethod
    def create_scraper(cls, platform: str) -> BaseScraper:
        """
        Create a scraper instance for the specified platform.
        
        Args:
            platform: Platform name (e.g., "lazada", "shopee", "tiktokshop")
        
        Returns:
            Instance of the appropriate scraper class
        
        Raises:
            ValidationError: If platform is not supported
        """
        platform_lower = platform.lower()
        
        # Load real scrapers
        cls._load_real_scrapers()
        
        # Check if scraper exists
        if platform_lower not in cls._real_scrapers:
            supported = ", ".join(cls._real_scrapers.keys())
            available_msg = f"Available platforms: {supported}" if supported else "No platforms available yet"
            raise ValidationError(
                f"Platform '{platform}' is not supported yet. {available_msg}",
                field="platform"
            )
        
        scraper_class = cls._real_scrapers[platform_lower]
        logger.info(f"Creating REAL scraper for platform: {platform}")
        return scraper_class()
    
    @classmethod
    def get_supported_platforms(cls) -> list[str]:
        """
        Get list of supported platform names.
        
        Returns:
            List of supported platform names
        """
        cls._load_real_scrapers()
        return list(cls._real_scrapers.keys())
    
    @classmethod
    def is_platform_supported(cls, platform: str) -> bool:
        """
        Check if a platform is supported.
        
        Args:
            platform: Platform name to check
        
        Returns:
            True if platform is supported, False otherwise
        """
        cls._load_real_scrapers()
        return platform.lower() in cls._real_scrapers
    
    @classmethod
    def register_scraper(cls, platform: str, scraper_class: Type[BaseScraper], is_real: bool = True) -> None:
        """
        Register a new scraper class for a platform.
        Useful for adding custom scrapers at runtime.
        
        Args:
            platform: Platform name
            scraper_class: Scraper class that extends BaseScraper
            is_real: Whether this is a real scraper (True) or mock (False)
        
        Raises:
            ValidationError: If scraper_class doesn't extend BaseScraper
        """
        if not issubclass(scraper_class, BaseScraper):
            raise ValidationError(
                "Scraper class must extend BaseScraper",
                field="scraper_class"
            )
        
        platform_lower = platform.lower()
        
        if is_real:
            cls._real_scrapers[platform_lower] = scraper_class
        else:
            cls._mock_scrapers[platform_lower] = scraper_class
        
        logger.info(f"Registered {'real' if is_real else 'mock'} scraper for platform: {platform}")
