"""
Scraper modules for e-commerce platforms.
"""
from app.scrapers.base_scraper import (
    BaseScraper,
    ProductSearchResult,
    PriceCheckResult
)
from app.core.exceptions import ScraperError

# Optional imports for scrapers (may not work in serverless environments)
try:
    from app.scrapers.lazada_selenium_scraper import LazadaSeleniumScraper
except ImportError:
    LazadaSeleniumScraper = None

try:
    from app.scrapers.shopee_scraper import ShopeeScraper
except ImportError:
    ShopeeScraper = None

try:
    from app.scrapers.tiktokshop_scraper import TikTokShopScraper
except ImportError:
    TikTokShopScraper = None

from app.scrapers.scraper_factory import ScraperFactory

__all__ = [
    "BaseScraper",
    "ProductSearchResult",
    "PriceCheckResult",
    "ScraperError",
    "LazadaSeleniumScraper",
    "ShopeeScraper",
    "TikTokShopScraper",
    "ScraperFactory"
]
