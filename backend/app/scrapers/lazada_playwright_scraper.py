"""
Lazada scraper using Playwright for JavaScript-rendered content.
Supports pagination and sorting.
"""
from typing import List, Optional
from decimal import Decimal
import asyncio
import re
from playwright.async_api import async_playwright, Page, Browser, TimeoutError as PlaywrightTimeoutError

from app.scrapers.base_scraper import (
    BaseScraper,
    ProductSearchResult,
    PriceCheckResult
)
from app.core.exceptions import ScraperError, PlatformUnavailableError


class LazadaPlaywrightScraper(BaseScraper):
    """
    Lazada scraper using Playwright for browser automation.
    Handles JavaScript-rendered content with pagination and sorting.
    """
    
    BASE_URL = "https://www.lazada.com.ph"
    SEARCH_URL = f"{BASE_URL}/catalog/"
    
    def __init__(self):
        super().__init__("lazada")
        self.playwright = None
        self.browser = None
        self.context = None
    
    async def __aenter__(self):
        """Initialize Playwright browser."""
        self.playwright = await async_playwright().start()
        
        # Try to use system Chrome if available, otherwise use Chromium
        try:
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
        except Exception as e:
            self.logger.warning(f"Failed to launch Chromium: {e}")
            # Fallback: try with different settings
            self.browser = await self.playwright.chromium.launch(
                headless=False,  # Try non-headless
                args=['--no-sandbox']
            )
        
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup Playwright resources."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def search(
        self, 
        query: str, 
        max_results: int = 10,
        page: int = 1,
        sort_by: str = "best_match"
    ) -> List[ProductSearchResult]:
        """
        Search for products on Lazada using Playwright.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            page: Page number (1-indexed)
            sort_by: Sort option - "best_match", "price_asc", or "price_desc"
        
        Returns:
            List of ProductSearchResult objects
        """
        try:
            # Build search URL with pagination and sorting
            params = {'q': query, 'page': page}
            
            # Add sort parameter
            if sort_by == "price_asc":
                params['sortBy'] = 'priceasc'
            elif sort_by == "price_desc":
                params['sortBy'] = 'pricedesc'
            # best_match doesn't need a parameter
            
            # Build URL
            url_params = '&'.join([f"{k}={v}" for k, v in params.items()])
            search_url = f"{self.SEARCH_URL}?{url_params}"
            
            self.logger.info(f"Searching Lazada with Playwright: {query} (page={page}, sort={sort_by})")
            
            # Create new page
            page_obj = await self.context.new_page()
            
            try:
                # Navigate to search page
                await page_obj.goto(search_url, wait_until='networkidle', timeout=30000)
                
                # Wait for products to load
                try:
                    await page_obj.wait_for_selector('[data-tracking="product-card"]', timeout=10000)
                except PlaywrightTimeoutError:
                    self.logger.warning("Timeout waiting for product cards")
                
                # Wait a bit more for all products to render
                await asyncio.sleep(2)
                
                # Extract products
                products = await self._extract_products(page_obj, max_results)
                
                self.logger.info(f"Successfully scraped {len(products)} products from Lazada")
                return products
                
            finally:
                await page_obj.close()
            
        except PlaywrightTimeoutError as e:
            self.logger.error(f"Playwright timeout: {e}")
            raise ScraperError("Request timeout", platform="lazada")
        except Exception as e:
            self.logger.error(f"Playwright scraper error: {e}")
            self._handle_scraper_error(e, "search")
    
    async def _extract_products(self, page: Page, max_results: int) -> List[ProductSearchResult]:
        """
        Extract product data from the page.
        
        Args:
            page: Playwright page object
            max_results: Maximum number of products to extract
        
        Returns:
            List of ProductSearchResult objects
        """
        products = []
        
        # Find all product cards
        product_cards = await page.query_selector_all('[data-tracking="product-card"]')
        
        self.logger.info(f"Found {len(product_cards)} product cards on page")
        
        for card in product_cards[:max_results]:
            try:
                product = await self._parse_product_card(card)
                if product:
                    products.append(product)
            except Exception as e:
                self.logger.warning(f"Failed to parse product card: {e}")
                continue
        
        return products
    
    async def _parse_product_card(self, card) -> Optional[ProductSearchResult]:
        """
        Parse a single product card element.
        
        Args:
            card: Playwright element handle for product card
        
        Returns:
            ProductSearchResult or None if parsing fails
        """
        try:
            # Extract product URL
            link = await card.query_selector('a[href]')
            if not link:
                return None
            
            product_url = await link.get_attribute('href')
            if not product_url:
                return None
            
            # Make URL absolute
            if product_url.startswith('//'):
                product_url = f'https:{product_url}'
            elif product_url.startswith('/'):
                product_url = f'{self.BASE_URL}{product_url}'
            
            # Extract product name
            name_elem = await card.query_selector('[class*="title"], [class*="name"]')
            if not name_elem:
                return None
            
            product_name = await name_elem.inner_text()
            product_name = product_name.strip()
            
            # Extract price
            price_elem = await card.query_selector('[class*="price"]')
            if not price_elem:
                return None
            
            price_text = await price_elem.inner_text()
            price = self._parse_price(price_text)
            
            if price is None:
                return None
            
            # Extract image URL
            img = await card.query_selector('img')
            image_url = None
            if img:
                image_url = await img.get_attribute('src')
                if not image_url:
                    image_url = await img.get_attribute('data-src')
            
            return ProductSearchResult(
                platform='lazada',
                product_url=product_url,
                product_name=product_name,
                current_price=price,
                currency='PHP',
                image_url=image_url,
                availability=True
            )
            
        except Exception as e:
            self.logger.warning(f"Error parsing product card: {e}")
            return None
    
    async def get_current_price(self, product_url: str) -> PriceCheckResult:
        """
        Get the current price of a specific product on Lazada.
        
        Args:
            product_url: URL of the product page
        
        Returns:
            PriceCheckResult object with current price information
        """
        try:
            if not self._validate_url(product_url):
                raise ScraperError("Invalid Lazada product URL", platform="lazada")
            
            self.logger.info(f"Checking price with Playwright: {product_url}")
            
            page = await self.context.new_page()
            
            try:
                await page.goto(product_url, wait_until='networkidle', timeout=30000)
                
                # Wait for price element
                await page.wait_for_selector('[class*="pdp-price"]', timeout=10000)
                
                # Extract price
                price_elem = await page.query_selector('[class*="pdp-price"]')
                if not price_elem:
                    return PriceCheckResult(
                        product_url=product_url,
                        current_price=None,
                        currency='PHP',
                        availability=False,
                        error="Price not found"
                    )
                
                price_text = await price_elem.inner_text()
                price = self._parse_price(price_text)
                
                # Check availability
                is_available = True
                availability_elem = await page.query_selector('[class*="out-of-stock"], [class*="unavailable"]')
                if availability_elem:
                    is_available = False
                
                return PriceCheckResult(
                    product_url=product_url,
                    current_price=price,
                    currency='PHP',
                    availability=is_available
                )
                
            finally:
                await page.close()
            
        except PlaywrightTimeoutError:
            return PriceCheckResult(
                product_url=product_url,
                current_price=None,
                currency='PHP',
                availability=False,
                error="Request timeout"
            )
        except Exception as e:
            return PriceCheckResult(
                product_url=product_url,
                current_price=None,
                currency='PHP',
                availability=False,
                error=str(e)
            )
    
    def _validate_url(self, url: str) -> bool:
        """Validate that a URL belongs to Lazada."""
        return 'lazada.com' in url.lower()
