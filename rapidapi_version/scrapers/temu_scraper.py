"""
Temu scraper using Selenium - Same approach as working Lazada scraper
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

class TemuScraperAPI(BaseScraper):
    """
    Temu scraper using EXACT same approach as working Lazada scraper
    """
    
    BASE_URL = "https://www.temu.com"
    SEARCH_URL = f"{BASE_URL}/search_result.html"
    
    def __init__(self):
        super().__init__("temu")
        self.driver = None
    
    async def __aenter__(self):
        """Initialize Selenium browser - NON-HEADLESS to bypass Temu detection"""
        chrome_options = Options()
        # DON'T use headless mode - Temu detects it
        # chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        
        # More realistic user agent
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
        
        # Exclude automation switches
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Preferences
        prefs = {
            'profile.managed_default_content_settings.images': 1,
            'profile.default_content_setting_values.notifications': 2,
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False
        }
        chrome_options.add_experimental_option('prefs', prefs)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(20)
        
        # Execute CDP commands to hide automation
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        })
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup"""
        if self.driver:
            self.driver.quit()
    
    async def search(
        self, 
        query: str, 
        max_results: int = 20,
        page: int = 1,
        sort_by: str = "best_match"
    ) -> Tuple[List[ProductResult], int]:
        """
        Search Temu with enhanced anti-detection
        """
        try:
            # Build URL - Temu format
            search_url = f"{self.SEARCH_URL}?search_key={query}"
            
            self.logger.info(f"Searching Temu: {query} (page={page}, sort={sort_by})")
            
            # Navigate
            self.driver.get(search_url)
            
            # Wait longer for page to load
            time.sleep(4)
            
            # Check if we got redirected to login page
            current_url = self.driver.current_url
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text.lower()
            
            if 'sign in' in page_text or 'login' in page_text or 'register' in page_text:
                self.logger.error("Temu redirected to login page - bot detection active")
                # Try to find any product links anyway
                pass
            
            # Try multiple selectors for product links
            product_selectors = [
                'a[href*="/goods.html"]',
                'a[href*="goods_id"]',
                '[class*="product"] a',
                '[class*="item"] a[href]',
                'div[class*="goods"] a'
            ]
            
            found_products = False
            for selector in product_selectors:
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    found_products = True
                    self.logger.info(f"Found products with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not found_products:
                self.logger.warning("No product links found with any selector")
            
            # Scroll to load content
            time.sleep(2)
            scroll_positions = [0.25, 0.5, 0.75, 1.0]
            for pos in scroll_positions:
                self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {pos});")
                time.sleep(0.5)
            
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Extract total count
            total_count = self._extract_total_count()
            
            # Extract products
            products = self._extract_products(max_results)
            
            self.logger.info(f"Successfully scraped {len(products)} products from Temu")
            return products, total_count
            
        except Exception as e:
            self.logger.error(f"Temu scraper error: {e}")
            self._handle_scraper_error(e, "search")
    
    def _extract_total_count(self) -> int:
        """Extract total count - EXACT same approach as Lazada"""
        try:
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text
            
            # Look for patterns like "X results", "X items"
            patterns = [
                r'(\d+)\s+results?',
                r'(\d+)\s+items?',
                r'of\s+(\d+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    total = int(match.group(1))
                    self.logger.info(f"Extracted total count: {total}")
                    return total
            
            return 0
            
        except Exception as e:
            self.logger.warning(f"Error extracting total count: {e}")
            return 0
    
    def _extract_products(self, max_results: int) -> List[ProductResult]:
        """Extract products with multiple selector strategies"""
        products = []
        
        # Try multiple selectors for product links
        product_selectors = [
            'a[href*="/goods.html"]',
            'a[href*="goods_id"]',
            '[class*="product"] a[href]',
            '[class*="item"] a[href]',
            'div[class*="goods"] a[href]'
        ]
        
        product_links = []
        for selector in product_selectors:
            try:
                links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if links:
                    product_links = links
                    self.logger.info(f"Found {len(links)} links with selector: {selector}")
                    break
            except NoSuchElementException:
                continue
        
        if not product_links:
            self.logger.warning("No product links found with any selector")
            return products
        
        self.logger.info(f"Found {len(product_links)} product links on page")
        
        # Process each link
        seen_urls = set()
        for link in product_links:
            if len(products) >= max_results:
                break
                
            try:
                product = self._parse_product_from_link(link)
                if product and product.product_url not in seen_urls:
                    products.append(product)
                    seen_urls.add(product.product_url)
            except Exception as e:
                self.logger.debug(f"Failed to parse product: {e}")
                continue
        
        return products
    
    def _parse_product_from_link(self, link_element) -> Optional[ProductResult]:
        """Parse product from link - EXACT same approach as Lazada"""
        try:
            # Get URL
            product_url = link_element.get_attribute('href')
            if not product_url or '/goods.html' not in product_url:
                return None
            
            # Make URL absolute
            if product_url.startswith('//'):
                product_url = f'https:{product_url}'
            elif product_url.startswith('/'):
                product_url = f'{self.BASE_URL}{product_url}'
            
            # Get parent container (go up a few levels to get the product card)
            parent = link_element
            for _ in range(5):
                try:
                    parent = parent.find_element(By.XPATH, '..')
                    parent_html = parent.get_attribute('innerHTML')
                    
                    # Extract product name from title attribute or text
                    product_name = None
                    try:
                        title_match = re.search(r'title="([^"]+)"', parent_html)
                        if title_match:
                            product_name = title_match.group(1)
                            import html
                            product_name = html.unescape(product_name)
                    except:
                        pass
                    
                    if not product_name:
                        # Try getting text
                        text = parent.text
                        lines = [l.strip() for l in text.split('\n') if l.strip()]
                        for line in lines:
                            if len(line) > 10 and '$' not in line and '₱' not in line:
                                product_name = line
                                break
                    
                    # Extract price from HTML (Temu uses $ or ₱)
                    price = None
                    price_matches = re.findall(r'[\$₱][\d,]+(?:\.\d+)?', parent_html)
                    if price_matches:
                        price = self._parse_price(price_matches[0])
                    
                    # Extract image
                    image_url = None
                    img_matches = re.findall(r'https://[^"\'>\s]*(?:temu|akamaized)[^"\'>\s]*\.(?:jpg|jpeg|png|webp)', parent_html)
                    for match in img_matches:
                        if 'icon' not in match.lower() and 'logo' not in match.lower():
                            image_url = match.split('?')[0]
                            break
                    
                    # If we have enough data, return product
                    if product_name and price:
                        # Determine currency
                        currency = 'USD' if '$' in parent_html else 'PHP'
                        
                        return ProductResult(
                            platform='temu',
                            product_url=product_url,
                            product_name=product_name[:200],  # Limit length
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
        """Parse price - EXACT same as Lazada"""
        try:
            # Handle both $ and ₱
            clean_text = price_text.replace('$', '').replace('₱', '').replace(',', '')
            price_match = re.search(r'[\d]+\.?\d*', clean_text)
            if price_match:
                price_str = price_match.group(0)
                return Decimal(price_str)
        except Exception as e:
            self.logger.warning(f"Error parsing price '{price_text}': {e}")
        return None