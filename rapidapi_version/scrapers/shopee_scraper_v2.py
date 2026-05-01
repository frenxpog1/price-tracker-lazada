"""
Shopee scraper V2 - Advanced anti-detection version
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

class ShopeeScraperV2(BaseScraper):
    """
    Advanced Shopee scraper with anti-detection measures
    """
    
    BASE_URL = "https://shopee.ph"
    
    def __init__(self):
        super().__init__("shopee")
        self.driver = None
    
    async def __aenter__(self):
        """Initialize browser with advanced anti-detection"""
        chrome_options = Options()
        
        # Don't use headless - it's easily detected
        # chrome_options.add_argument('--headless')
        
        # Anti-detection measures
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Realistic user agent
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Window size
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Remove webdriver property
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                '''
            })
            
            self.driver.set_page_load_timeout(20)
        except Exception as e:
            self.logger.error(f"Failed to initialize Chrome driver: {e}")
            raise ScraperError("Browser initialization failed", "shopee", 503)
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup"""
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
        Search Shopee with anti-detection
        """
        try:
            # Build URL - Shopee uses different URL structure
            # Format: https://shopee.ph/search?keyword=phone&page=0&sortBy=relevancy
            sort_param = self._get_sort_parameter(sort_by)
            search_url = f"{self.BASE_URL}/search?keyword={query}&page={page-1}&sortBy={sort_param}"
            
            self.logger.info(f"Searching Shopee: {query} (page={page}, sort={sort_by})")
            self.logger.info(f"URL: {search_url}")
            
            # Navigate
            self.driver.get(search_url)
            
            # Wait longer for JavaScript to load
            time.sleep(5)
            
            # Scroll to trigger lazy loading
            for i in range(3):
                self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {(i+1)/3});")
                time.sleep(1)
            
            # Try to find products with multiple selectors
            products = self._extract_products_v2(max_results)
            total_count = len(products) * 10  # Estimate
            
            self.logger.info(f"Successfully scraped {len(products)} products from Shopee")
            return products, total_count
            
        except Exception as e:
            self.logger.error(f"Shopee scraper error: {e}")
            self._handle_scraper_error(e, "search")
    
    def _get_sort_parameter(self, sort_by: str) -> str:
        """Convert sort_by to Shopee parameter"""
        mapping = {
            "best_match": "relevancy",
            "price_asc": "price",
            "price_desc": "pricedesc"
        }
        return mapping.get(sort_by, "relevancy")
    
    def _extract_products_v2(self, max_results: int) -> List[ProductResult]:
        """Extract products using multiple strategies"""
        products = []
        
        # Strategy 1: Try to find any links to product pages
        try:
            links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/product/"]')
            self.logger.info(f"Found {len(links)} product links")
            
            for link in links[:max_results]:
                try:
                    product = self._parse_from_link(link)
                    if product:
                        products.append(product)
                except Exception as e:
                    self.logger.debug(f"Failed to parse link: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Strategy 1 failed: {e}")
        
        return products
    
    def _parse_from_link(self, link_element) -> Optional[ProductResult]:
        """Parse product from a link element"""
        try:
            # Get URL
            product_url = link_element.get_attribute('href')
            if not product_url or '/product/' not in product_url:
                return None
            
            # Try to find product info in parent elements
            parent = link_element
            for _ in range(5):  # Go up 5 levels
                try:
                    parent = parent.find_element(By.XPATH, '..')
                    
                    # Try to find name
                    name = None
                    try:
                        name_elem = parent.find_element(By.CSS_SELECTOR, '[class*="title"], [class*="name"]')
                        name = name_elem.text
                    except:
                        pass
                    
                    # Try to find price
                    price = None
                    try:
                        price_elem = parent.find_element(By.CSS_SELECTOR, '[class*="price"]')
                        price_text = price_elem.text
                        if '₱' in price_text:
                            price = self._parse_price(price_text)
                    except:
                        pass
                    
                    # Try to find image
                    image_url = None
                    try:
                        img = parent.find_element(By.TAG_NAME, 'img')
                        image_url = img.get_attribute('src') or img.get_attribute('data-src')
                    except:
                        pass
                    
                    # If we have enough data, create product
                    if name and price:
                        return ProductResult(
                            platform='shopee',
                            product_url=product_url,
                            product_name=name,
                            current_price=price,
                            currency='PHP',
                            image_url=image_url,
                            availability=True,
                            scraped_at=datetime.utcnow()
                        )
                        
                except:
                    continue
            
            return None
            
        except Exception as e:
            self.logger.debug(f"Error parsing link: {e}")
            return None
    
    def _parse_price(self, price_text: str) -> Optional[Decimal]:
        """Parse price from text"""
        try:
            # Remove currency and extract number
            clean = price_text.replace('₱', '').replace(',', '').strip()
            match = re.search(r'[\d]+\.?\d*', clean)
            if match:
                return Decimal(match.group(0))
        except Exception as e:
            self.logger.warning(f"Error parsing price '{price_text}': {e}")
        return None
