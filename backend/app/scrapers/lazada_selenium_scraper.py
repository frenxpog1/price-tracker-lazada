"""
Lazada scraper using Selenium for JavaScript-rendered content.
Supports pagination and sorting.
"""
from typing import List, Optional
from decimal import Decimal
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from app.scrapers.base_scraper import (
    BaseScraper,
    ProductSearchResult,
    PriceCheckResult
)
from app.core.exceptions import ScraperError, PlatformUnavailableError


class LazadaSeleniumScraper(BaseScraper):
    """
    Lazada scraper using Selenium for browser automation.
    Handles JavaScript-rendered content with pagination and sorting.
    """
    
    BASE_URL = "https://www.lazada.com.ph"
    SEARCH_URL = f"{BASE_URL}/catalog/"
    
    def __init__(self):
        super().__init__("lazada")
        self.driver = None
    
    async def __aenter__(self):
        """Initialize Selenium browser with performance optimizations."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Performance optimizations - disable unnecessary features
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-dev-tools')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        
        # Disable images to speed up page load (we'll get image URLs from HTML)
        prefs = {
            'profile.managed_default_content_settings.images': 2,
            'profile.default_content_setting_values.notifications': 2,
        }
        chrome_options.add_experimental_option('prefs', prefs)
        
        # Use webdriver-manager to automatically download and manage ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(15)  # Reduced from 30
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup Selenium resources."""
        if self.driver:
            self.driver.quit()
    
    async def search(
        self, 
        query: str, 
        max_results: int = 10,
        page: int = 1,
        sort_by: str = "best_match"
    ) -> tuple[List[ProductSearchResult], int]:
        """
        Search for products on Lazada using Selenium.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            page: Page number (1-indexed)
            sort_by: Sort option - "best_match", "price_asc", or "price_desc"
        
        Returns:
            Tuple of (List of ProductSearchResult objects, total count)
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
            
            self.logger.info(f"Searching Lazada with Selenium: {query} (page={page}, sort={sort_by})")
            
            # Navigate to search page
            self.driver.get(search_url)
            
            # Wait for products to load - reduced wait time
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tracking="product-card"]'))
                )
            except TimeoutException:
                self.logger.warning("Timeout waiting for product cards")
            
            # Wait a bit longer for images to load (staggered approach)
            time.sleep(2)
            
            # More aggressive image loading strategy
            try:
                # Scroll to different positions to trigger lazy loading
                scroll_positions = [0.25, 0.5, 0.75, 1.0]
                for pos in scroll_positions:
                    self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {pos});")
                    time.sleep(0.3)  # Short wait at each position
                
                # Scroll back to top
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(0.5)
                
                # Force trigger image loading with JavaScript
                self.driver.execute_script("""
                    // Find all img elements and trigger loading
                    document.querySelectorAll('img').forEach(img => {
                        if (img.getAttribute('data-src')) {
                            img.src = img.getAttribute('data-src');
                        }
                        // Trigger load event
                        img.scrollIntoView({behavior: 'instant', block: 'nearest'});
                    });
                """)
                time.sleep(1)
                
            except Exception as e:
                self.logger.warning(f"Error during image loading: {e}")
            
            # Extract total count
            total_count = self._extract_total_count()
            
            # Extract products
            products = self._extract_products(max_results)
            
            self.logger.info(f"Successfully scraped {len(products)} products from Lazada (total: {total_count})")
            return products, total_count
            
        except TimeoutException as e:
            self.logger.error(f"Selenium timeout: {e}")
            raise ScraperError("Request timeout", platform="lazada")
        except Exception as e:
            self.logger.error(f"Selenium scraper error: {e}")
            self._handle_scraper_error(e, "search")
    
    def _extract_total_count(self) -> int:
        """
        Extract the total number of results from the page.
        
        Returns:
            Total count of results, or 0 if not found
        """
        try:
            # Look for text like "3244 items found for 'concave lens'"
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text
            
            # Try to find pattern like "X items found"
            import re
            match = re.search(r'(\d+)\s+items?\s+found', page_text, re.IGNORECASE)
            if match:
                total = int(match.group(1))
                matched_text = match.group(0)
                self.logger.info(f"Extracted total count: {total} from text: '{matched_text}'")
                return total
            
            # Alternative: look for specific element (adjust selector as needed)
            try:
                count_elem = self.driver.find_element(By.CSS_SELECTOR, '[class*="search-info"]')
                text = count_elem.text
                match = re.search(r'(\d+)', text)
                if match:
                    total = int(match.group(1))
                    self.logger.info(f"Extracted total count from element: {total}")
                    return total
            except NoSuchElementException:
                pass
            
            self.logger.warning("Could not find total count pattern in page text")
            return 0
            
        except Exception as e:
            self.logger.warning(f"Error extracting total count: {e}")
            return 0
    
    def _extract_products(self, max_results: int) -> List[ProductSearchResult]:
        """
        Extract product data from the page with precise image matching.
        
        Args:
            max_results: Maximum number of products to extract
        
        Returns:
            List of ProductSearchResult objects
        """
        products = []
        
        # Find all product cards first
        try:
            product_cards = self.driver.find_elements(By.CSS_SELECTOR, '[data-tracking="product-card"]')
        except NoSuchElementException:
            self.logger.warning("No product cards found")
            return products
        
        self.logger.info(f"Found {len(product_cards)} product cards on page")
        
        # Process each card individually with more precise image extraction
        for idx, card in enumerate(product_cards[:max_results]):
            try:
                product = self._parse_product_card_with_precise_image(card, idx)
                if product:
                    products.append(product)
            except Exception as e:
                self.logger.warning(f"Failed to parse product card {idx}: {e}")
                continue
        
        return products
    
    def _extract_image_from_card(self, card) -> Optional[str]:
        """
        Extract image URL directly from a product card with multiple strategies.
        
        Args:
            card: Selenium WebElement for product card
        
        Returns:
            Image URL or None if not found
        """
        try:
            # Strategy 1: Find all img elements in this card
            imgs = card.find_elements(By.CSS_SELECTOR, 'img')
            
            for img in imgs:
                # Check multiple attributes in order of preference
                for attr in ['src', 'data-src', 'data-lazy-src', 'data-original', 'data-img']:
                    url = img.get_attribute(attr)
                    if url and 'lazcdn.com' in url and 'data:image' not in url:
                        # Clean up URL
                        url = url.split('?')[0] if '?' in url else url
                        return url
            
            # Strategy 2: Look for background images in div elements
            divs_with_bg = card.find_elements(By.CSS_SELECTOR, 'div[style*="background-image"]')
            for div in divs_with_bg:
                style = div.get_attribute('style')
                if style and 'lazcdn.com' in style:
                    import re
                    match = re.search(r'url\(["\']?(https://[^"\')\s]*lazcdn\.com[^"\')\s]*)["\']?\)', style)
                    if match:
                        return match.group(1)
            
            # Strategy 3: Extract from card's HTML using regex
            card_html = card.get_attribute('innerHTML')
            if card_html:
                import re
                # Look for any lazcdn.com image URLs
                img_matches = re.findall(r'https://[^"\'>\s]*lazcdn\.com[^"\'>\s]*\.(?:jpg|jpeg|png|webp)', card_html)
                for match in img_matches:
                    # Skip icons and logos, prefer product images
                    if 'icon' not in match.lower() and 'logo' not in match.lower() and '/p/' in match:
                        return match.split('?')[0] if '?' in match else match
                
                # If no /p/ images found, take any non-icon image
                for match in img_matches:
                    if 'icon' not in match.lower() and 'logo' not in match.lower():
                        return match.split('?')[0] if '?' in match else match
            
        except Exception as e:
            self.logger.debug(f"Error extracting image from card: {e}")
        
        return None
    
    def _parse_product_card_with_precise_image(self, card, idx: int) -> Optional[ProductSearchResult]:
        """
        Parse a product card with more precise image matching.
        
        Args:
            card: Selenium WebElement for product card
            idx: Index of the card for fallback matching
        
        Returns:
            ProductSearchResult or None if parsing fails
        """
        try:
            # Extract product URL first
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
            
            # Extract product ID from URL for image matching
            product_id = None
            import re
            id_match = re.search(r'i(\d+)', product_url)
            if id_match:
                product_id = id_match.group(1)
            
            # Extract product name from HTML instead of text
            product_name = None
            try:
                # Try to find the title attribute first
                title_elem = card.find_element(By.CSS_SELECTOR, 'a[title]')
                product_name = title_elem.get_attribute('title')
            except NoSuchElementException:
                # Fallback: extract from HTML
                card_html = card.get_attribute('innerHTML')
                if card_html:
                    # Look for title attribute in HTML
                    title_match = re.search(r'title="([^"]+)"', card_html)
                    if title_match:
                        product_name = title_match.group(1)
                        # Decode HTML entities
                        import html
                        product_name = html.unescape(product_name)
            
            if not product_name or len(product_name) < 5:
                return None
            
            # Extract price from HTML
            price = None
            try:
                # Look for price elements
                price_elem = card.find_element(By.CSS_SELECTOR, 'span[class*="ooOxS"], .price, [class*="price"]')
                price_text = price_elem.text
                if price_text and '₱' in price_text:
                    price = self._parse_price(price_text)
            except NoSuchElementException:
                pass
            
            # Fallback: extract from HTML if price element text is empty
            if not price:
                card_html = card.get_attribute('innerHTML')
                if card_html:
                    # Look for peso prices in HTML
                    price_matches = re.findall(r'₱[\d,]+(?:\.\d+)?', card_html)
                    if price_matches:
                        price = self._parse_price(price_matches[0])
                    else:
                        # Alternative pattern: look for price in span elements
                        span_matches = re.findall(r'<span[^>]*>₱[\d,]+(?:\.\d+)?</span>', card_html)
                        if span_matches:
                            # Extract just the price part
                            price_match = re.search(r'₱[\d,]+(?:\.\d+)?', span_matches[0])
                            if price_match:
                                price = self._parse_price(price_match.group(0))
            
            if price is None:
                return None
            
            # Try multiple strategies to get the correct image
            image_url = self._get_precise_image_for_card(card, product_id, idx)
            
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
    
    def _get_precise_image_for_card(self, card, product_id: Optional[str], idx: int) -> Optional[str]:
        """
        Get the most accurate image for a specific product card.
        
        Args:
            card: Selenium WebElement for product card
            product_id: Product ID extracted from URL
            idx: Card index for fallback
        
        Returns:
            Image URL or None
        """
        # Strategy 1: Look for images within this specific card
        try:
            imgs = card.find_elements(By.CSS_SELECTOR, 'img')
            for img in imgs:
                # Check if image is actually loaded (not a placeholder)
                for attr in ['src', 'data-src', 'data-lazy-src']:
                    url = img.get_attribute(attr)
                    if url and 'lazcdn.com' in url and 'data:image' not in url:
                        # Prefer images that contain the product ID
                        if product_id and product_id in url:
                            return url.split('?')[0]
                        # Or any valid lazcdn image
                        elif '/p/' in url or '/g/' in url:
                            return url.split('?')[0]
        except:
            pass
        
        # Strategy 2: Look in the card's HTML for image URLs
        try:
            card_html = card.get_attribute('innerHTML')
            if card_html:
                import re
                # Find all lazcdn image URLs
                img_matches = re.findall(r'https://[^"\'>\s]*lazcdn\.com[^"\'>\s]*\.(?:jpg|jpeg|png|webp)', card_html)
                
                # Prefer images with product ID
                if product_id:
                    for match in img_matches:
                        if product_id in match and 'icon' not in match.lower():
                            return match.split('?')[0]
                
                # Fallback to any product image
                for match in img_matches:
                    if ('/p/' in match or '/g/' in match) and 'icon' not in match.lower() and 'logo' not in match.lower():
                        return match.split('?')[0]
        except:
            pass
        
        # Strategy 3: Get all images from page and try to match by position
        try:
            page_source = self.driver.page_source
            import re
            all_images = re.findall(r'https://[^"\'>\s]*lazcdn\.com[^"\'>\s]*\.(?:jpg|jpeg|png|webp)', page_source)
            product_images = [url for url in all_images if '/p/' in url and 'icon' not in url.lower()]
            
            if idx < len(product_images):
                return product_images[idx].split('?')[0]
        except:
            pass
        
        return None
    
    def _parse_product_card(self, card, image_url: Optional[str] = None) -> Optional[ProductSearchResult]:
        """
        Parse a single product card element.
        
        Args:
            card: Selenium WebElement for product card
            image_url: Pre-extracted image URL (optional)
        
        Returns:
            ProductSearchResult or None if parsing fails
        """
        try:
            # Get all text from the card
            card_text = card.text
            
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
            
            # Extract product name from card text
            lines = [line.strip() for line in card_text.split('\n') if line.strip()]
            
            product_name = None
            for line in lines:
                # Skip lines that look like prices
                if '₱' not in line and not line.replace(',', '').replace('.', '').isdigit():
                    if len(line) > 10:
                        product_name = line
                        break
            
            if not product_name:
                return None
            
            # Extract price from card text
            price = None
            for line in lines:
                if '₱' in line:
                    price = self._parse_price(line)
                    if price:
                        break
            
            if price is None:
                return None
            
            # Use pre-extracted image URL or try to extract from card again
            if not image_url:
                try:
                    img = card.find_element(By.CSS_SELECTOR, 'img')
                    for attr in ['src', 'data-src', 'data-lazy-src', 'data-original']:
                        url = img.get_attribute(attr)
                        if url and 'lazcdn.com' in url and 'data:image' not in url:
                            image_url = url
                            break
                except:
                    pass
            
            # Clean up image URL if found
            if image_url:
                # Remove query parameters and clean up
                image_url = image_url.split('?')[0] if '?' in image_url else image_url
                # Handle srcset format
                if ' ' in image_url:
                    image_url = image_url.split(' ')[0]
            
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
            
            self.logger.info(f"Checking price with Selenium: {product_url}")
            
            self.driver.get(product_url)
            
            # Wait for price element
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="pdp-price"]'))
                )
            except TimeoutException:
                return PriceCheckResult(
                    product_url=product_url,
                    current_price=None,
                    currency='PHP',
                    availability=False,
                    error="Price not found"
                )
            
            # Extract price
            try:
                price_elem = self.driver.find_element(By.CSS_SELECTOR, '[class*="pdp-price"]')
                price_text = price_elem.text
                price = self._parse_price(price_text)
            except NoSuchElementException:
                return PriceCheckResult(
                    product_url=product_url,
                    current_price=None,
                    currency='PHP',
                    availability=False,
                    error="Price not found"
                )
            
            # Check availability
            is_available = True
            try:
                self.driver.find_element(By.CSS_SELECTOR, '[class*="out-of-stock"], [class*="unavailable"]')
                is_available = False
            except NoSuchElementException:
                pass
            
            return PriceCheckResult(
                product_url=product_url,
                current_price=price,
                currency='PHP',
                availability=is_available
            )
            
        except TimeoutException:
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
    
    def _parse_price(self, price_text: str) -> Optional[Decimal]:
        """
        Parse price from text string.
        
        Args:
            price_text: Text containing price information
        
        Returns:
            Decimal price or None if parsing fails
        """
        try:
            import re
            # Remove currency symbols and extract numbers
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('₱', '').replace(',', ''))
            if price_match:
                price_str = price_match.group(0).replace(',', '')
                return Decimal(price_str)
        except Exception as e:
            self.logger.warning(f"Error parsing price '{price_text}': {e}")
        return None