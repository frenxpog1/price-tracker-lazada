#!/usr/bin/env python3
"""
Direct test of the Lazada scraper to see what it returns.
"""
import asyncio
import sys
sys.path.insert(0, '/Users/fritzhelrosenacario/Desktop/Hey/backend')

from app.scrapers.lazada_scraper_simple import LazadaScraperSimple

async def test_scraper():
    scraper = LazadaScraperSimple()
    
    print("Testing Lazada scraper...")
    print("Searching for 'iphone' on page 1...")
    
    try:
        results = await scraper.search("iphone", max_results=5, page=1, sort_by="best_match")
        
        print(f"\n✅ Search completed!")
        print(f"Found {len(results)} products\n")
        
        if results:
            for i, product in enumerate(results, 1):
                print(f"{i}. {product.product_name}")
                print(f"   Price: {product.current_price} {product.currency}")
                print(f"   URL: {product.product_url[:80]}...")
                print()
        else:
            print("❌ No products found!")
            print("\nThis means:")
            print("1. Lazada's HTML structure has changed")
            print("2. Products are loaded via JavaScript (need browser automation)")
            print("3. Lazada is blocking our requests")
            
            # Check if HTML was saved
            import os
            if os.path.exists('/tmp/lazada_response.html'):
                print("\n📄 HTML response saved to: /tmp/lazada_response.html")
                print("Check this file to see what Lazada actually returned")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_scraper())
