#!/usr/bin/env python3
"""
Test the Playwright-based Lazada scraper.
"""
import asyncio
import sys
sys.path.insert(0, '/Users/fritzhelrosenacario/Desktop/Hey/backend')

from app.scrapers.lazada_playwright_scraper import LazadaPlaywrightScraper

async def test_scraper():
    print("Testing Lazada Playwright scraper...")
    print("This will take 10-15 seconds (browser automation is slow)\n")
    
    async with LazadaPlaywrightScraper() as scraper:
        print("🌐 Browser started")
        print("🔍 Searching for 'iphone' on page 1...")
        
        try:
            results = await scraper.search("iphone", max_results=5, page=1, sort_by="best_match")
            
            print(f"\n✅ Search completed!")
            print(f"Found {len(results)} products\n")
            
            if results:
                for i, product in enumerate(results, 1):
                    print(f"{i}. {product.product_name}")
                    print(f"   Price: ₱{product.current_price}")
                    print(f"   URL: {product.product_url[:80]}...")
                    print()
                
                print("✅ SUCCESS! Real Lazada scraping is working!")
            else:
                print("❌ No products found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_scraper())
