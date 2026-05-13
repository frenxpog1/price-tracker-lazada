"""
Lazada scraper using Scrapling for bypassing anti-bot and extracting data.
"""
import asyncio
from typing import List, Optional
from decimal import Decimal

from app.scrapers.base_scraper import (
    BaseScraper,
    ProductSearchResult,
    PriceCheckResult
)
from app.core.exceptions import ScraperError
from scrapling.fetchers import AsyncStealthySession


class LazadaScraplingScraper(BaseScraper):
    """
    Lazada scraper using Scrapling's AsyncStealthySession to bypass anti-bot systems
    with maximum speed and stability by reusing the browser session.
    """
    
    BASE_URL = "https://www.lazada.com.ph"
    SEARCH_URL = f"{BASE_URL}/catalog/"
    _session: Optional[AsyncStealthySession] = None
    
    def __init__(self):
        super().__init__("lazada")
        
    @classmethod
    async def get_session(cls) -> AsyncStealthySession:
        if cls._session is None:
            cls._session = AsyncStealthySession(headless=True)
            await cls._session.start()
        return cls._session

    async def search(
        self, 
        query: str, 
        max_results: int = 10,
        page: int = 1,
        sort_by: str = "best_match"
    ) -> List[ProductSearchResult]:
        """Asynchronous search logic using Scrapling AsyncStealthySession."""
        params = {'q': query, 'page': page}
        if sort_by == "price_asc":
            params['sortBy'] = 'priceasc'
        elif sort_by == "price_desc":
            params['sortBy'] = 'pricedesc'
            
        url_params = '&'.join([f"{k}={v}" for k, v in params.items()])
        search_url = f"{self.SEARCH_URL}?{url_params}"
        
        self.logger.info(f"Searching Lazada with Scrapling (Async): {search_url}")
        
        try:
            session = await self.get_session()
            
            async def scroll_page(page):
                # Scroll down to trigger all lazy-loaded images
                import asyncio
                for i in range(5):
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight * " + str(i/5) + ")")
                    await asyncio.sleep(0.3)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1)

            page_obj = await session.fetch(search_url, page_action=scroll_page)
            
            # Parse JSON-LD to get real image URLs (bypasses lazy loading placeholders)
            import json
            import re
            images_map = {}
            
            def extract_product_id(url: str) -> str:
                # Extracts the unique ID from strings like: //www.lazada.com.ph/products/apple-iphone-15-i4119890424.html?spm=...
                # or //www.lazada.com.ph/products/pdp-i4119890424.html
                match = re.search(r'-i(\d+)\.html', url)
                return match.group(1) if match else url
                
            scripts = page_obj.css('script[type="application/ld+json"]')
            for s in scripts:
                text = s.text
                if text and 'ItemList' in text:
                    try:
                        data = json.loads(text)
                        for item in data.get('itemListElement', []):
                            i_data = item.get('item', {})
                            i_url = i_data.get('url', '')
                            i_image = i_data.get('image', '')
                            if i_url and i_image:
                                p_id = extract_product_id(i_url)
                                images_map[p_id] = i_image
                    except Exception as e:
                        self.logger.warning(f"Error parsing ld+json: {e}")
            
            # Scrapling page object allows css/xpath selection
            product_cards = page_obj.css('[data-tracking="product-card"]')
            self.logger.info(f"Found {len(product_cards)} product cards")
            
            products = []
            for card in product_cards[:max_results]:
                try:
                    # Extract URL
                    links = card.css('a[href]')
                    if not links:
                        continue
                    link = links[0]
                    raw_product_url = link.attrib.get('href')
                    if not raw_product_url:
                        continue
                        
                    product_url = raw_product_url
                    if product_url.startswith('//'):
                        product_url = f'https:{product_url}'
                    elif product_url.startswith('/'):
                        product_url = f'{self.BASE_URL}{product_url}'
                    
                    # Extract Name
                    name_elems = card.css('a[title]')
                    if not name_elems:
                        # fallback
                        name_elems = card.css('a[href]')
                    product_name = name_elems[0].attrib.get('title') or name_elems[0].text.strip()
                    if not product_name:
                        continue
                    
                    # Extract Price
                    price = None
                    spans = card.css('span')
                    for span in spans:
                        text = span.text.strip()
                        if '₱' in text or 'PHP' in text or '$' in text:
                            price = self._parse_price(text)
                            if price:
                                break
                    if price is None:
                        continue
                    
                    # Extract Image
                    # Use JSON-LD map first by matching product ID
                    p_id = extract_product_id(raw_product_url)
                    image_url = images_map.get(p_id)
                    
                    # Fallback to DOM if not found
                    if not image_url:
                        imgs = card.css('img')
                        for img in imgs:
                            src = img.attrib.get('src', '')
                            data_src = img.attrib.get('data-src', '')
                            is_product = img.attrib.get('type') == 'product'
                            
                            # Prefer type="product", then data-src, then valid src
                            best_url = ''
                            if is_product and src and not src.startswith('data:'):
                                best_url = src
                            elif data_src:
                                best_url = data_src
                            elif src and 'lzd-img-global' not in src and not src.startswith('data:'):
                                best_url = src
                                
                            if best_url:
                                if best_url.startswith('//'):
                                    image_url = f'https:{best_url}'
                                else:
                                    image_url = best_url
                                
                                # If we found a type="product", we can break immediately
                                if is_product:
                                    break
                    
                    products.append(ProductSearchResult(
                        platform='lazada',
                        product_url=product_url,
                        product_name=product_name,
                        current_price=price,
                        currency='PHP',
                        image_url=image_url,
                        availability=True
                    ))
                except Exception as e:
                    self.logger.warning(f"Error parsing product card: {e}")
                    
            return products
            
        except Exception as e:
            self._handle_scraper_error(e, "search")

    async def get_current_price(self, product_url: str) -> PriceCheckResult:
        """Asynchronous price check logic using Scrapling AsyncStealthySession."""
        if not self._validate_url(product_url):
            raise ScraperError("Invalid Lazada product URL", platform="lazada")
            
        self.logger.info(f"Checking price with Scrapling (Async): {product_url}")
        
        try:
            session = await self.get_session()
            page_obj = await session.fetch(product_url)
            
            price = None
            spans = page_obj.css('span')
            for span in spans:
                text = span.text.strip()
                if ('₱' in text or 'PHP' in text or '$' in text) and any(c.isdigit() for c in text):
                    price = self._parse_price(text)
                    if price is not None:
                        break
            
            if price is None:
                return PriceCheckResult(
                    product_url=product_url,
                    current_price=None,
                    currency='PHP',
                    availability=False,
                    error="Price not found"
                )
                
            availability_elems = page_obj.css('[class*="out-of-stock"], [class*="unavailable"]')
            is_available = len(availability_elems) == 0
            
            return PriceCheckResult(
                product_url=product_url,
                current_price=price,
                currency='PHP',
                availability=is_available
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
        return 'lazada.com' in url.lower()

