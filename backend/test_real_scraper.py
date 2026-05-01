"""
Quick test script to verify the real Lazada scraper works.
Run this from the backend directory: python test_real_scraper.py
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.scrapers.lazada_scraper_simple import LazadaScraperSimple


async def test_scraper():
    """Test the Lazada scraper with a real search."""
    print("=" * 60)
    print("Testing Lazada Scraper")
    print("=" * 60)
    
    scraper = LazadaScraperSimple()
    
    try:
        # Test search
        query = "iphone 10 xr"
        print(f"\nSearching for: {query}")
        print("-" * 60)
        
        results = await scraper.search(query, max_results=5)
        
        print(f"\nFound {len(results)} products:\n")
        
        for i, product in enumerate(results, 1):
            print(f"{i}. {product.product_name}")
            print(f"   Price: ₱{product.current_price}")
            print(f"   URL: {product.product_url[:80]}...")
            print(f"   Image: {product.image_url[:80] if product.image_url else 'None'}...")
            print()
        
        if results:
            print("✅ Scraper is working!")
        else:
            print("⚠️  No results found - might need to update selectors")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_scraper())
