import asyncio
from app.scrapers.lazada_scrapling_scraper import LazadaScraplingScraper

async def test_1000():
    scraper = LazadaScraplingScraper()
    total_found = 0
    missing_images = 0
    
    try:
        # Test 10 pages (40 items each = 400 items). 25 pages might get us rate limited.
        for page_num in range(1, 11):
            url = f"https://www.lazada.com.ph/catalog/?q=iphone&page={page_num}"
            print(f"Fetching page {page_num}...")
            
            # Reusing the search method by manually modifying the BASE_URL temporarily, 
            # or just using the search method directly.
            # wait, scraper.search hardcodes page=1 if we just pass 'iphone'.
            # We can modify it or just copy the fetch logic here.
            
            session = await scraper.get_session()
            
            async def scroll_page(page):
                import asyncio
                for i in range(5):
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight * " + str(i/5) + ")")
                    await asyncio.sleep(0.3)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1)

            page_obj = await session.fetch(url, page_action=scroll_page)
            
            import json, re
            images_map = {}
            def extract_product_id(u: str) -> str:
                match = re.search(r'-i(\d+)\.html', u)
                return match.group(1) if match else u

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
                    except: pass
            
            cards = page_obj.css('[data-tracking="product-card"]')
            print(f"Page {page_num}: Found {len(cards)} cards")
            
            for card in cards:
                total_found += 1
                links = card.css('a[href]')
                if not links: continue
                raw_url = links[0].attrib.get('href', '')
                p_id = extract_product_id(raw_url)
                
                image_url = images_map.get(p_id)
                if not image_url:
                    imgs = card.css('img')
                    for img in imgs:
                        src = img.attrib.get('src', '')
                        data_src = img.attrib.get('data-src', '')
                        is_product = img.attrib.get('type') == 'product'
                        
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
                            if is_product:
                                break
                
                if not image_url:
                    name_elems = card.css('a[title]')
                    name = name_elems[0].attrib.get('title') if name_elems else "Unknown"
                    print(f"  [MISSING IMAGE] {name} | URL: {raw_url}")
                    missing_images += 1
                    
        print("-" * 30)
        print(f"Total Products Checked: {total_found}")
        print(f"Successfully Extracted Images: {total_found - missing_images} ({(total_found - missing_images)/total_found * 100:.1f}%)")
        print(f"Missing Images: {missing_images}")
        
    finally:
        if scraper._session:
            await scraper._session.close()

if __name__ == "__main__":
    asyncio.run(test_1000())
