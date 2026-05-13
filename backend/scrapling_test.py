import asyncio
from app.scrapers.scraper_factory import ScraperFactory
import logging

logging.basicConfig(level=logging.INFO)

async def test_lazada():
    scraper = ScraperFactory.create_scraper("lazada")
    print(f"Created scraper: {type(scraper).__name__}")
    
    # Test search
    print("Searching for laptop...")
    results = await scraper.search("laptop", max_results=3)
    for idx, result in enumerate(results):
        print(f"[{idx}] {result.product_name} - {result.current_price} {result.currency}")
        print(f"    Image: {result.image_url}")
        
    if results:
        # Test get_price
        first_url = results[0].product_url
        print(f"\nChecking price for {first_url}")
        price_result = await scraper.get_current_price(first_url)
        print(f"Price result: {price_result.current_price} (Available: {price_result.availability})")

if __name__ == "__main__":
    asyncio.run(test_lazada())
