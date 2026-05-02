"""
Lazada scraper using Playwright (better for Render deployment).
Optimized for speed and reliability.
"""

from typing import List, Optional, Tuple
from decimal import Decimal
import time
import re
from datetime import datetime
from playwright.async_api import async_playwright, Page, Browser
import asyncio

from .base_scraper import BaseScraper, ProductResult, ScraperError


class LazadaScraperPlaywright(BaseScraper):
    """
    Lazada scraper using Playwright.
    Works better on Render than Selenium.
    """
    
    BASE_URL = "https://www.lazada.com.ph"
    SEARCH_URL = f"{BASE_URL}/catalog/"
    
    def __init__(self):
        super().__init__("lazada")
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
    
    async def __aenter__(self):
        """Initialize Playwright browser."""
        try:
            self.playwright = await async_playwright().start()
            
            self.logger.info("Launching Playwright browser...")
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-gpu',
                    '--single-process',
                ]
            )
            
            # Create context with custom user agent
            context = await self.browser.new_context(
                user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            self.page = await context.new_page()
            self.page.set_default_timeout(30000)  # 30 second timeout for Render
            
            self.logger.info("✅ Playwright browser initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Playwright: {e}")
            raise ScraperError(f"Browser initialization failed: {str(e)}", "lazada", 503)
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup Playwright resources."""
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            self.logger.warning(f"Error during cleanup: {e}")
    
    async def search(
        self, 
        query: str, 
        max_results: int = 20,
        page: int = 1,
        sort_by: str = "best_match"
    ) -> Tuple[List[ProductResult], int]:
        """
        Search for products on Lazada.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            page: Page number (1-indexed)
            sort_by: Sort option - "best_match", "price_asc", or "price_desc"
        
        Returns:
            Tuple of (List of ProductResult objects, total count)
        """
        try:
            # Build search URL
            params = {'q': query, 'page': page}
            
            # Add sort parameter
            if sort_by == "price_asc":
                params['sortBy'] = 'priceasc'
            elif sort_by == "price_desc":
                params['sortBy'] = 'pricedesc'
            
            # Build URL
            url_params = '&'.join([f"{k}={v}" for k, v in params.items()])
            search_url = f"{self.SEARCH_URL}?{url_params}"
            
            self.logger.info(f"Searching Lazada: {query} (page={page}, sort={sort_by})")
            
            # Navigate to search page
            await self.page.goto(search_url, wait_until='domcontentloaded', timeout=30000)
            
            # Wait for products to load
            try:
                await self.page.wait_for_selector('[data-tracking="product-card"]', timeout=10000)
            except Exception:
                self.logger.warning("Timeout waiting for product cards")
            
            # Quick scroll to trigger lazy loading
            await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight * 0.5)')
            await asyncio.sleep(0.5)
            await self.page.evaluate('window.scrollTo(0, 0)')
            await asyncio.sleep(0.5)
            
            # Extract total count
            total_count = await self._extract_total_count()
            
            # Extract products
            products = await self._extract_products(max_results)
            
            self.logger.info(f"Successfully scraped {len(products)} products from Lazada")
            return products, total_count
            
        except Exception as e:
            self.logger.error(f"Playwright scraper error: {e}")
            self._handle_scraper_error(e, "search")
    
    async def _extract_total_count(self) -> int:
        """Extract the total number of results from the page."""
        try:
            page_text = await self.page.inner_text('body')
            
            # Look for pattern like "X items found"
            match = re.search(r'(\d+)\s+items?\s+found', page_text, re.IGNORECASE)
            if match:
                total = int(match.group(1))
                self.logger.info(f"Extracted total count: {total}")
                return total
            
            return 0
            
        except Exception as e:
            self.logger.warning(f"Error extracting total count: {e}")
            return 0
    
    async def _extract_products(self, max_results: int) -> List[ProductResult]:
        """Extract product data from the page."""
        products = []
        
        try:
            # Get all product cards
            cards = await self.page.query_selector_all('[data-tracking="product-card"]')
            self.logger.info(f"Found {len(cards)} product cards on page")
            
            # Process each card
            for idx, card in enumerate(cards[:max_results]):
                try:
                    product = await self._parse_product_card(card)
                    if product:
                        products.append(product)
                except Exception as e:
                    self.logger.warning(f"Failed to parse product card {idx}: {e}")
                    continue
            
        except Exception as e:
            self.logger.error(f"Error extracting products: {e}")
        
        return products
    
    async def _parse_product_card(self, card) -> Optional[ProductResult]:
        """Parse a single product card element."""
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
            
            # Extract product name from title attribute
            title_elem = await card.query_selector('a[title]')
            product_name = None
            if title_elem:
                product_name = await title_elem.get_attribute('title')
            
            # Fallback: extract from HTML
            if not product_name:
                card_html = await card.inner_html()
                title_match = re.search(r'title="([^"]+)"', card_html)
                if title_match:
                    import html
                    product_name = html.unescape(title_match.group(1))
            
            if not product_name or len(product_name) < 5:
                return None
            
            # Extract price
            price = None
            price_elem = await card.query_selector('span[class*="ooOxS"], .price, [class*="price"]')
            if price_elem:
                price_text = await price_elem.inner_text()
                if price_text and '₱' in price_text:
                    price = self._parse_price(price_text)
            
            # Fallback: extract price from HTML
            if not price:
                card_html = await card.inner_html()
                price_matches = re.findall(r'₱[\d,]+(?:\.\d+)?', card_html)
                if price_matches:
                    price = self._parse_price(price_matches[0])
            
            if price is None:
                return None
            
            # Extract image URL
            image_url = await self._extract_image_url(card)
            
            return ProductResult(
                platform='lazada',
                product_url=product_url,
                product_name=product_name,
                current_price=price,
                currency='PHP',
                image_url=image_url,
                availability=True,
                scraped_at=datetime.utcnow()
            )
            
        except Exception as e:
            self.logger.warning(f"Error parsing product card: {e}")
            return None
    
    async def _extract_image_url(self, card) -> Optional[str]:
        """Extract image URL from a product card."""
        try:
            # Try to find img elements
            imgs = await card.query_selector_all('img')
            
            for img in imgs:
                for attr in ['src', 'data-src', 'data-lazy-src']:
                    url = await img.get_attribute(attr)
                    if url and 'lazcdn.com' in url and 'data:image' not in url:
                        return url.split('?')[0] if '?' in url else url
            
            # Fallback: extract from HTML
            card_html = await card.inner_html()
            img_matches = re.findall(r'https://[^"\'>\s]*lazcdn\.com[^"\'>\s]*\.(?:jpg|jpeg|png|webp)', card_html)
            for match in img_matches:
                if 'icon' not in match.lower() and 'logo' not in match.lower():
                    return match.split('?')[0] if '?' in match else match
            
        except Exception as e:
            self.logger.debug(f"Error extracting image: {e}")
        
        return None
    
    def _parse_price(self, price_text: str) -> Optional[Decimal]:
        """Parse price from text string."""
        try:
            # Remove currency symbols and extract numbers
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('₱', '').replace(',', ''))
            if price_match:
                price_str = price_match.group(0).replace(',', '')
                return Decimal(price_str)
        except Exception as e:
            self.logger.warning(f"Error parsing price '{price_text}': {e}")
        return None
