"""
Simplified Lazada scraper for RapidAPI version.
Optimized for speed and reliability without database dependencies.
"""

from typing import List, Optional, Tuple
from decimal import Decimal
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from .base_scraper import BaseScraper, ProductResult, ScraperError

class LazadaScraperAPI(BaseScraper):
    """
    Simplified Lazada scraper for API use.
    Optimized for speed and reliability.
    """
    
    BASE_URL = "https://www.lazada.com.ph"
    SEARCH_URL = f"{BASE_URL}/catalog/"
    
    def __init__(self):
        super().__init__("lazada")
        self.driver = None
    
    async def __aenter__(self):
        """Initialize Selenium browser with performance optimizations."""
        import os
        
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
        
        # Performance optimizations
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-dev-tools')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--single-process')
        
        # Disable images for faster loading
        prefs = {
            'profile.managed_default_content_settings.images': 2,
            'profile.default_content_setting_values.notifications': 2,
        }
        chrome_options.add_experimental_option('prefs', prefs)
        
        try:
            # Check if running in Docker (Chrome installed via apt)
            if os.path.exists('/usr/bin/google-chrome'):
                self.logger.info("Using Docker Chrome installation")
                chrome_options.binary_location = '/usr/bin/google-chrome'
                service = Service('/usr/bin/chromedriver') if os.path.exists('/usr/bin/chromedriver') else Service()
            else:
                # Running locally - use webdriver-manager
                self.logger.info("Using webdriver-manager for Chrome")
                service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)  # Increased timeout for API
            self.logger.info("✅ Chrome driver initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Chrome driver: {e}")
            raise ScraperError(f"Browser initialization failed: {str(e)}", "lazada", 503)
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup Selenium resources."""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
    
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
            self.driver.get(search_url)
            
            # Wait for products to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tracking="product-card"]'))
                )
            except TimeoutException:
                self.logger.warning("Timeout waiting for product cards")
            
            # Quick scroll to trigger any lazy loading
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5);")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)            
            # Extract total count
            total_count = self._extract_total_count()
            
            # Extract products
            products = self._extract_products(max_results)
            
            self.logger.info(f"Successfully scraped {len(products)} products from Lazada")
            return products, total_count
            
        except TimeoutException as e:
            self.logger.error(f"Selenium timeout: {e}")
            raise ScraperError("Request timeout", "lazada", 408)
        except Exception as e:
            self.logger.error(f"Selenium scraper error: {e}")
            self._handle_scraper_error(e, "search")
    
    def _extract_total_count(self) -> int:
        """Extract the total number of results from the page."""
        try:
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text
            
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
    
    def _extract_products(self, max_results: int) -> List[ProductResult]:
        """Extract product data from the page."""
        products = []
        
        try:
            product_cards = self.driver.find_elements(By.CSS_SELECTOR, '[data-tracking="product-card"]')
        except NoSuchElementException:
            self.logger.warning("No product cards found")
            return products
        
        self.logger.info(f"Found {len(product_cards)} product cards on page")
        
        # Process each card
        for idx, card in enumerate(product_cards[:max_results]):
            try:
                product = self._parse_product_card(card)
                if product:
                    products.append(product)
            except Exception as e:
                self.logger.warning(f"Failed to parse product card {idx}: {e}")
                continue
        
        return products
    
    def _parse_product_card(self, card) -> Optional[ProductResult]:
        """Parse a single product card element."""
        try:
            # Extract product URL
            try:
                link = card.find_element(By.CSS_SELECTOR, 'a[href]')
                product_url = link.get_attribute('href')
            except NoSuchElementException:
                return None
            
            if not product_url:
                return None
            
            # Make URL absolute
            if product_url.startswith('//'):
                product_url = f'https:{product_url}'
            elif product_url.startswith('/'):
                product_url = f'{self.BASE_URL}{product_url}'
            
            # Extract product name from title attribute
            product_name = None
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, 'a[title]')
                product_name = title_elem.get_attribute('title')
            except NoSuchElementException:
                # Fallback: extract from HTML
                card_html = card.get_attribute('innerHTML')
                if card_html:
                    title_match = re.search(r'title="([^"]+)"', card_html)
                    if title_match:
                        import html
                        product_name = html.unescape(title_match.group(1))
            
            if not product_name or len(product_name) < 5:
                return None
            
            # Extract price
            price = None
            try:
                price_elem = card.find_element(By.CSS_SELECTOR, 'span[class*="ooOxS"], .price, [class*="price"]')
                price_text = price_elem.text
                if price_text and '₱' in price_text:
                    price = self._parse_price(price_text)
            except NoSuchElementException:
                pass
            
            # Fallback: extract price from HTML
            if not price:
                card_html = card.get_attribute('innerHTML')
                if card_html:
                    price_matches = re.findall(r'₱[\d,]+(?:\.\d+)?', card_html)
                    if price_matches:
                        price = self._parse_price(price_matches[0])
            
            if price is None:
                return None
            
            # Extract image URL
            image_url = self._extract_image_url(card)
            
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
    
    def _extract_image_url(self, card) -> Optional[str]:
        """Extract image URL from a product card."""
        try:
            # Try to find img elements
            imgs = card.find_elements(By.CSS_SELECTOR, 'img')
            
            for img in imgs:
                for attr in ['src', 'data-src', 'data-lazy-src']:
                    url = img.get_attribute(attr)
                    if url and 'lazcdn.com' in url and 'data:image' not in url:
                        return url.split('?')[0] if '?' in url else url
            
            # Fallback: extract from HTML
            card_html = card.get_attribute('innerHTML')
            if card_html:
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