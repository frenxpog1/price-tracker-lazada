import asyncio
from app.scrapers.lazada_scrapling_scraper import LazadaScraplingScraper

async def test():
    scraper = LazadaScraplingScraper()
    res = await scraper.search("iphone", max_results=10)
    for r in res:
        print(r.product_name)
        print(" ->", r.image_url)
    if scraper._session:
        await scraper._session.close()

if __name__ == "__main__":
    asyncio.run(test())
