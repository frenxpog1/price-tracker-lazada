import asyncio
import json
from app.scrapers.lazada_scrapling_scraper import LazadaScraplingScraper

async def test():
    scraper = LazadaScraplingScraper()
    session = await scraper.get_session()
    page = await session.fetch("https://www.lazada.com.ph/catalog/?q=iphone&page=1")
    
    scripts = page.css('script[type="application/ld+json"]')
    for s in scripts:
        text = s.text
        if text and 'ItemList' in text:
            data = json.loads(text)
            print(json.dumps(data, indent=2))
            
if __name__ == "__main__":
    asyncio.run(test())
