"""
Temu scraper V2 - Advanced anti-detection version
Uses the actual Temu search URL structure
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

class TemuScraperV2(BaseScraper):
    """
    Advanced Temu scraper with anti-detection measures
    """
    
    BASE_URL = "https://www.temu.com"
    
    def __init__(self):
        super().__init__("temu")
        self.driver = None
    
    async def __aenter__(self):
        """Initialize browser with advanced anti-detection"""
        chrome_options = Options()
        
        # Don't use headless - Temu detects it
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
        
        # Accept language
        chrome_options.add_argument('--lang=en-US')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Remove webdriver property
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en']
                    });
                '''
            })
            
            self.driver.set_page_load_timeout(20)
        except Exception as e:
            self.logger.error(f"Failed to initialize Chrome driver: {e}")
            raise ScraperError("Browser initialization failed", "temu", 503)
        
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
        Search Temu with anti-detection
        """
        try:
            # Use the actual Temu search URL structure
            # Format: https://www.temu.com/search_result.html?search_key=phone
            search_url = f"{self.BASE_URL}/search_result.html?search_key={query}"
            
            self.logger.info(f"Searching Temu: {query} (page={page}, sort={sort_by})")
            self.logger.info(f"URL: {search_url}")
            
            # Navigate
            self.driver.get(search_url)
            
            # Wait longer for JavaScript to load
            time.sleep(8)  # Temu needs more time
            
            # Scroll to trigger lazy loading
            for i in range(4):
                self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {(i+1)/4});")
                time.sleep(2)
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Save page source for debugging
            try:
                with open('temu_page_source.html', 'w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)
                self.logger.info("Saved page source to temu_page_source.html")
            except:
                pass
            
            # Try to find products
            products = self._extract_products_v2(max_results)
            total_count = len(products) * 15  # Estimate
            
            self.logger.info(f"Successfully scraped {len(products)} products from Temu")
            return products, total_count
            
        except Exception as e:
            self.logger.error(f"Temu scraper error: {e}")
            self._handle_scraper_error(e, "search")
    
    def _extract_products_v2(self, max_results: int) -> List[ProductResult]:
        """Extract products using multiple strategies"""
        products = []
        
        # Strategy 1: Find links to goods pages
        try:
            links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/goods.html"]')
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
        
        # Strategy 2: Try to find any divs with product data
        if len(products) == 0:
            try:
                # Look for any elements with price symbols
                price_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '$') or contains(text(), '₱')]")
                self.logger.info(f"Found {len(price_elements)} elements with prices")
                
                for elem in price_elements[:max_results]:
                    try:
                        product = self._parse_from_price_element(elem)
                        if product:
                            products.append(product)
                    except:
                        continue
                        
            except Exception as e:
                self.logger.error(f"Strategy 2 failed: {e}")
        
        return products
    
    def _parse_from_link(self, link_element) -> Optional[ProductResult]:
        """Parse product from a link element"""
        try:
            # Get URL
            product_url = link_element.get_attribute('href')
            if not product_url or '/goods.html' not in product_url:
                return None
            
            # Make URL absolute
            if not product_url.startswith('http'):
                product_url = f"{self.BASE_URL}{product_url}"
            
            # Try to find product info in parent elements
            parent = link_element
            for _ in range(5):  # Go up 5 levels
                try:
                    parent = parent.find_element(By.XPATH, '..')
                    
                    # Try to find name
                    name = None
                    try:
                        # Look for text content
                        text = parent.text
                        lines = [l.strip() for l in text.split('\n') if l.strip()]
                        for line in lines:
                            if len(line) > 10 and '$' not in line and '₱' not in line:
                                name = line
                                break
                    except:
                        pass
                    
                    # Try to find price
                    price = None
                    try:
                        text = parent.text
                        # Look for price patterns
                        price_matches = re.findall(r'[\$₱][\d,]+\.?\d*', text)
                        if price_matches:
                            price = self._parse_price(price_matches[0])
                    except:
                        pass
                    
                    # Try to find image
                    image_url = None
                    try:
                        img = parent.find_element(By.TAG_NAME, 'img')
                        image_url = img.get_attribute('src') or img.get_attribute('data-src')
                        if image_url and not image_url.startswith('http'):
                            image_url = None
                    except:
                        pass
                    
                    # If we have enough data, create product
                    if name and price:
                        # Determine currency
                        currency = 'USD' if '$' in text else 'PHP'
                        
                        return ProductResult(
                            platform='temu',
                            product_url=product_url,
                            product_name=name[:200],  # Limit length
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
            self.logger.debug(f"Error parsing link: {e}")
            return None
    
    def _parse_from_price_element(self, price_element) -> Optional[ProductResult]:
        """Parse product from an element containing price"""
        try:
            # Get parent container
            parent = price_element
            for _ in range(3):
                parent = parent.find_element(By.XPATH, '..')
            
            # Extract data
            text = parent.text
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            
            # Find name (longest line without price)
            name = None
            for line in lines:
                if len(line) > 10 and '$' not in line and '₱' not in line:
                    name = line
                    break
            
            # Find price
            price = None
            price_matches = re.findall(r'[\$₱][\d,]+\.?\d*', text)
            if price_matches:
                price = self._parse_price(price_matches[0])
            
            # Find URL
            product_url = None
            try:
                link = parent.find_element(By.CSS_SELECTOR, 'a[href*="/goods.html"]')
                product_url = link.get_attribute('href')
                if not product_url.startswith('http'):
                    product_url = f"{self.BASE_URL}{product_url}"
            except:
                pass
            
            if name and price and product_url:
                currency = 'USD' if '$' in text else 'PHP'
                
                return ProductResult(
                    platform='temu',
                    product_url=product_url,
                    product_name=name[:200],
                    current_price=price,
                    currency=currency,
                    image_url=None,
                    availability=True,
                    scraped_at=datetime.utcnow()
                )
                
        except Exception as e:
            self.logger.debug(f"Error parsing price element: {e}")
        
        return None
    
    def _parse_price(self, price_text: str) -> Optional[Decimal]:
        """Parse price from text"""
        try:
            # Remove currency symbols and extract number
            clean = price_text.replace('$', '').replace('₱', '').replace(',', '').strip()
            match = re.search(r'[\d]+\.?\d*', clean)
            if match:
                return Decimal(match.group(0))
        except Exception as e:
            self.logger.warning(f"Error parsing price '{price_text}': {e}")
        return None
