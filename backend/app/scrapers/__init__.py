"""
Scraper modules for e-commerce platforms.
"""
from app.scrapers.base_scraper import (
    BaseScraper,
    ProductSearchResult,
    PriceCheckResult
)
from app.core.exceptions import ScraperError
from app.scrapers.lazada_selenium_scraper import LazadaSeleniumScraper
from app.scrapers.shopee_scraper import ShopeeScraper
from app.scrapers.tiktokshop_scraper import TikTokShopScraper
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
