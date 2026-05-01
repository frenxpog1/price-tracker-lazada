"""
Shopee scraper implementation using Playwright for dynamic content.
"""
from typing import List, Optional
from decimal import Decimal
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeout

from app.scrapers.base_scraper import (
    BaseScraper,
    ProductSearchResult,
    PriceCheckResult
)
from app.core.exceptions import ScraperError, PlatformUnavailableError


class ShopeeScraper(BaseScraper):
    """
    Scraper for Shopee e-commerce platform.
    Uses Playwright for handling dynamic JavaScript content.
    """
    
    # Shopee Philippines base URL
    BASE_URL = "https://shopee.ph"
    SEARCH_URL = f"{BASE_URL}/search"
    
    # CSS selectors with fallbacks
    SEARCH_SELECTORS = {
        "product_card": [
            '[data-sqe="item"]',
            '.shopee-search-item-result__item',
            '.col-xs-2-4'
        ],
        "product_link": [
            'a[data-sqe="link"]',
            '.shopee-search-item-result__item a',
            'a'
        ],
        "product_name": [
            '[data-sqe="name"]',
            '.ie3A+n',
            '.shopee-item-card__text-name'
        ],
        "product_price": [
            '[data-sqe="price"]',
            '.ZEgDH9',
            '.shopee-item-card__current-price'
        ],
        "product_image": [
            'img[data-sqe="image"]',
            '.shopee-search-item-result__image img',
            'img'
        ]
    }
    
    PRODUCT_PAGE_SELECTORS = {
        "price": [
            '[data-sqe="product-price"]',
            '.pqTWkA',
            '._3n5NQx'
        ],
        "availability": [
            '[data-sqe="product-stock"]',
            '.flex.items-center',
            '.product-stock'
        ]
    }
    
    def __init__(self):
        super().__init__("shopee")
        self.browser: Optional[Browser] = None
        self.playwright = None
    
    async def _init_browser(self):
        """Initialize Playwright browser if not already initialized."""
        if self.browser is None:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            self.logger.info("Playwright browser initialized")
    
    async def _close_browser(self):
        """Close Playwright browser."""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
            self.logger.info("Playwright browser closed")
    
    async def _create_page(self) -> Page:
        """Create a new browser page with common settings."""
        await self._init_browser()
        page = await self.browser.new_page()
        
        # Set user agent to avoid bot detection
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        return page
    
    async def _find_element_text(self, page: Page, selectors: List[str]) -> Optional[str]:
        """
        Try multiple selectors to find element text.
        
        Args:
            page: Playwright page object
            selectors: List of CSS selectors to try
        
        Returns:
            Element text if found, None otherwise
        """
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    text = await element.inner_text()
                    if text and text.strip():
                        return text.strip()
            except Exception:
                continue
        return None
    
    async def _find_element_attribute(
        self,
        page: Page,
        selectors: List[str],
        attribute: str
    ) -> Optional[str]:
        """
        Try multiple selectors to find element attribute.
        
        Args:
            page: Playwright page object
            selectors: List of CSS selectors to try
            attribute: Attribute name to get
        
        Returns:
            Attribute value if found, None otherwise
        """
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    value = await element.get_attribute(attribute)
                    if value:
                        return value
            except Exception:
                continue
        return None
    
    async def search(self, query: str, max_results: int = 10) -> List[ProductSearchResult]:
        """
        Search for products on Shopee.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
        
        Returns:
            List of ProductSearchResult objects
        
        Raises:
            ScraperError: If scraping fails
        """
        page = None
        try:
            page = await self._create_page()
            
            # Navigate to search page
            search_url = f"{self.SEARCH_URL}?keyword={query}"
            self.logger.info(f"Searching Shopee for: {query}")
            
            try:
                await page.goto(search_url, wait_until="networkidle", timeout=30000)
            except PlaywrightTimeout:
                raise PlatformUnavailableError("shopee")
            
            # Wait for product cards to load
            await page.wait_for_selector(
                self.SEARCH_SELECTORS["product_card"][0],
                timeout=10000
            )
            
            # Extract product information
            products = []
            product_cards = await page.query_selector_all(
                self.SEARCH_SELECTORS["product_card"][0]
            )
            
            for card in product_cards[:max_results]:
                try:
                    # Extract product URL
                    link_element = await card.query_selector(
                        self.SEARCH_SELECTORS["product_link"][0]
                    )
                    if not link_element:
                        continue
                    
                    product_url = await link_element.get_attribute("href")
                    if not product_url:
                        continue
                    
                    # Make URL absolute
                    if product_url.startswith("/"):
                        product_url = f"{self.BASE_URL}{product_url}"
                    
                    # Extract product name
                    name = await self._find_element_text(
                        card,
                        self.SEARCH_SELECTORS["product_name"]
                    )
                    if not name:
                        continue
                    
                    # Extract price
                    price_text = await self._find_element_text(
                        card,
                        self.SEARCH_SELECTORS["product_price"]
                    )
                    if not price_text:
                        continue
                    
                    price = self._parse_price(price_text)
                    if price is None:
                        continue
                    
                    # Extract image URL
                    image_url = await self._find_element_attribute(
                        card,
                        self.SEARCH_SELECTORS["product_image"],
                        "src"
                    )
                    
                    products.append(ProductSearchResult(
                        platform="shopee",
                        product_url=product_url,
                        product_name=name,
                        current_price=price,
                        currency="PHP",
                        image_url=image_url,
                        availability=True
                    ))
                    
                except Exception as e:
                    self.logger.warning(f"Failed to parse product card: {str(e)}")
                    continue
            
            self.logger.info(f"Found {len(products)} products on Shopee")
            return products
            
        except PlatformUnavailableError:
            raise
        except Exception as e:
            self._handle_scraper_error(e, "search")
        finally:
            if page:
                await page.close()
    
    async def get_current_price(self, product_url: str) -> PriceCheckResult:
        """
        Get the current price of a specific product on Shopee.
        
        Args:
            product_url: URL of the product page
        
        Returns:
            PriceCheckResult object with current price information
        
        Raises:
            ScraperError: If scraping fails
        """
        page = None
        try:
            if not self._validate_url(product_url):
                raise ScraperError(
                    "Invalid Shopee product URL",
                    platform="shopee"
                )
            
            page = await self._create_page()
            
            self.logger.info(f"Checking price for: {product_url}")
            
            try:
                await page.goto(product_url, wait_until="networkidle", timeout=30000)
            except PlaywrightTimeout:
                return PriceCheckResult(
                    product_url=product_url,
                    current_price=None,
                    currency="PHP",
                    availability=False,
                    error="Platform unavailable"
                )
            
            # Extract price
            price_text = await self._find_element_text(
                page,
                self.PRODUCT_PAGE_SELECTORS["price"]
            )
            
            if not price_text:
                return PriceCheckResult(
                    product_url=product_url,
                    current_price=None,
                    currency="PHP",
                    availability=False,
                    error="Price not found"
                )
            
            price = self._parse_price(price_text)
            
            # Check availability
            availability_text = await self._find_element_text(
                page,
                self.PRODUCT_PAGE_SELECTORS["availability"]
            )
            
            is_available = True
            if availability_text:
                availability_lower = availability_text.lower()
                if any(term in availability_lower for term in ["out of stock", "unavailable", "sold out"]):
                    is_available = False
            
            return PriceCheckResult(
                product_url=product_url,
                current_price=price,
                currency="PHP",
                availability=is_available
            )
            
        except Exception as e:
            self._handle_scraper_error(e, "price_check")
        finally:
            if page:
                await page.close()
    
    def _validate_url(self, url: str) -> bool:
        """
        Validate that a URL belongs to Shopee.
        
        Args:
            url: URL to validate
        
        Returns:
            True if URL is a valid Shopee URL
        """
        return "shopee.ph" in url.lower()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close browser on context exit."""
        await self._close_browser()
