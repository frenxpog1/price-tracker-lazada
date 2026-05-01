"""
Temu scraper using Playwright with saved cookies (bypasses login)
"""
from typing import List, Optional, Tuple
from decimal import Decimal
import time
import re
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scrapers.base_scraper import BaseScraper, ProductResult, ScraperError

class TemuScraperWithCookies(BaseScraper):
    """
    Temu scraper using Playwright with saved cookies to bypass login
    """
    
    BASE_URL = "https://www.temu.com"
    SEARCH_URL = f"{BASE_URL}/search_result.html"
    
    def __init__(self):
        super().__init__("temu")
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
    
    async def __aenter__(self):
        """Initialize Playwright browser with saved cookies"""
        self.playwright = await async_playwright().start()
        
        # Check if we have saved cookies
        storage_file = "storage_temu.json"
        cookie_file = "cookies_temu.json"
        
        if os.path.exists(storage_file):
            self.logger.info(f"Loading saved session from {storage_file}")
            # Launch with saved storage state (includes cookies, localStorage, etc.)
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            self.context = await self.browser.new_context(
                storage_state=storage_file,
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            )
        elif os.path.exists(cookie_file):
            self.logger.info(f"Loading cookies from {cookie_file}")
            # Launch and add cookies manually
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            )
            
            # Load and add cookies
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            await self.context.add_cookies(cookies)
        else:
            self.logger.error("No saved cookies found! Please run login_helper.py first")
            raise ScraperError(
                "No saved cookies found. Please run 'python3 login_helper.py' to log in first.",
                platform="temu"
            )
        
        self.page = await self.context.new_page()
        
        # Add stealth scripts
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            window.chrome = { runtime: {} };
        """)
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def search(
        self, 
        query: str, 
        max_results: int = 20,
        page: int = 1,
        sort_by: str = "best_match"
    ) -> Tuple[List[ProductResult], int]:
        """
        Search Temu using saved cookies
        """
        try:
            # Build URL
            search_url = f"{self.SEARCH_URL}?search_key={query}"
            
            self.logger.info(f"Searching Temu with cookies: {query} (page={page})")
            
            # Navigate
            await self.page.goto(search_url, wait_until='networkidle', timeout=30000)
            
            # Wait for page to load
            await self.page.wait_for_timeout(3000)
            
            # Check if we're still logged in (not redirected to login)
            current_url = self.page.url
            if 'login' in current_url:
                self.logger.error("Redirected to login - cookies expired!")
                raise ScraperError(
                    "Session expired. Please run 'python3 login_helper.py' to log in again.",
                    platform="temu"
                )
            
            self.logger.info(f"Successfully loaded page: {current_url}")
            
            # Extract total count
            total_count = await self._extract_total_count()
            
            # Extract products
            products = await self._extract_products(max_results)
            
            self.logger.info(f"Successfully scraped {len(products)} products from Temu")
            return products, total_count
            
        except PlaywrightTimeout as e:
            self.logger.error(f"Timeout: {e}")
            raise ScraperError("Request timeout", platform="temu")
        except Exception as e:
            self.logger.error(f"Temu scraper error: {e}")
            self._handle_scraper_error(e, "search")
    
    async def _extract_total_count(self) -> int:
        """Extract total count from page"""
        try:
            body_text = await self.page.inner_text('body')
            
            patterns = [
                r'(\d+)\s+results?',
                r'(\d+)\s+items?',
                r'of\s+(\d+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, body_text, re.IGNORECASE)
                if match:
                    total = int(match.group(1))
                    self.logger.info(f"Extracted total count: {total}")
                    return total
            
            return 0
            
        except Exception as e:
            self.logger.warning(f"Error extracting total count: {e}")
            return 0
    
    async def _extract_products(self, max_results: int) -> List[ProductResult]:
        """Extract products from page"""
        products = []
        
        # Try multiple selectors
        selectors = [
            'a[href*="/goods.html"]',
            'a[href*="goods_id"]',
            '[data-testid*="product"] a',
        ]
        
        product_links = []
        for selector in selectors:
            try:
                elements = await self.page.query_selector_all(selector)
                if elements:
                    product_links = elements
                    self.logger.info(f"Found {len(elements)} products with selector: {selector}")
                    break
            except Exception as e:
                self.logger.debug(f"Selector {selector} failed: {e}")
                continue
        
        if not product_links:
            self.logger.warning("No product links found")
            return products
        
        # Process each link
        seen_urls = set()
        for link in product_links[:max_results]:
            try:
                product = await self._parse_product_link(link)
                if product and product.product_url not in seen_urls:
                    products.append(product)
                    seen_urls.add(product.product_url)
            except Exception as e:
                self.logger.debug(f"Failed to parse product: {e}")
                continue
        
        return products
    
    async def _parse_product_link(self, link_element) -> Optional[ProductResult]:
        """Parse a single product link"""
        try:
            # Get URL
            product_url = await link_element.get_attribute('href')
            if not product_url:
                return None
            
            # Make URL absolute
            if product_url.startswith('//'):
                product_url = f'https:{product_url}'
            elif product_url.startswith('/'):
                product_url = f'{self.BASE_URL}{product_url}'
            
            # Get parent container
            parent = link_element
            for _ in range(5):
                try:
                    parent = await parent.evaluate_handle('el => el.parentElement')
                    parent_html = await parent.inner_html()
                    
                    # Extract product name
                    product_name = None
                    title_match = re.search(r'title="([^"]+)"', parent_html)
                    if title_match:
                        product_name = title_match.group(1)
                        import html
                        product_name = html.unescape(product_name)
                    
                    if not product_name:
                        text = await parent.inner_text()
                        lines = [l.strip() for l in text.split('\n') if l.strip()]
                        for line in lines:
                            if len(line) > 10 and '$' not in line and '₱' not in line:
                                product_name = line
                                break
                    
                    # Extract price
                    price = None
                    price_matches = re.findall(r'[\$₱][\d,]+(?:\.\d+)?', parent_html)
                    if price_matches:
                        price = self._parse_price(price_matches[0])
                    
                    # Extract image
                    image_url = None
                    img_matches = re.findall(
                        r'https://[^"\'>\s]*(?:temu|akamaized)[^"\'>\s]*\.(?:jpg|jpeg|png|webp)',
                        parent_html
                    )
                    for match in img_matches:
                        if 'icon' not in match.lower() and 'logo' not in match.lower():
                            image_url = match.split('?')[0]
                            break
                    
                    # If we have enough data, return product
                    if product_name and price:
                        currency = 'USD' if '$' in parent_html else 'PHP'
                        
                        return ProductResult(
                            platform='temu',
                            product_url=product_url,
                            product_name=product_name[:200],
                            current_price=price,
                            currency=currency,
                            image_url=image_url,
                            availability=True,
                            scraped_at=datetime.utcnow()
                        )
                        
                except:
                    continue
            
            return None
            
        except Exception as e:
            self.logger.debug(f"Error parsing product: {e}")
            return None
    
    def _parse_price(self, price_text: str) -> Optional[Decimal]:
        """Parse price from text"""
        try:
            clean_text = price_text.replace('$', '').replace('₱', '').replace(',', '')
            price_match = re.search(r'[\d]+\.?\d*', clean_text)
            if price_match:
                price_str = price_match.group(0)
                return Decimal(price_str)
        except Exception as e:
            self.logger.warning(f"Error parsing price '{price_text}': {e}")
        return None
