"""
Test script for the Lazada API scraper.
Run this to verify your setup before deploying to Vercel.
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_lazada_api_scraper():
    """Test the Lazada API scraper."""
    print("=" * 60)
    print("Testing Lazada API Scraper")
    print("=" * 60)
    
    # Check if LAZADA_API_URL is set
    api_url = os.getenv('LAZADA_API_URL')
    if not api_url:
        print("❌ ERROR: LAZADA_API_URL environment variable is not set!")
        print("Please add it to your .env file:")
        print("LAZADA_API_URL=https://your-render-service.onrender.com")
        return
    
    print(f"✅ LAZADA_API_URL is set: {api_url}")
    print()
    
    # Import the scraper
    try:
        from app.scrapers.lazada_api_scraper import LazadaAPIScraper
        print("✅ Successfully imported LazadaAPIScraper")
    except ImportError as e:
        print(f"❌ Failed to import LazadaAPIScraper: {e}")
        return
    
    # Test the scraper
    print()
    print("Testing search for 'laptop'...")
    print("-" * 60)
    
    try:
        scraper = LazadaAPIScraper()
        
        async with scraper:
            products, total = await scraper.search(
                query="laptop",
                max_results=5,
                page=1,
                sort_by="best_match"
            )
            
            print(f"✅ Search successful!")
            print(f"   Total results: {total}")
            print(f"   Products returned: {len(products)}")
            print()
            
            if products:
                print("Sample products:")
                for i, product in enumerate(products[:3], 1):
                    print(f"\n{i}. {product.product_name[:60]}...")
                    print(f"   Price: {product.currency} {product.current_price}")
                    print(f"   URL: {product.product_url[:80]}...")
                    if product.image_url:
                        print(f"   Image: {product.image_url[:80]}...")
            else:
                print("⚠️  No products returned (this might be normal if the API is cold starting)")
    
    except Exception as e:
        print(f"❌ Search failed: {e}")
        print()
        print("Possible issues:")
        print("1. Render service URL is incorrect")
        print("2. Render service is not deployed yet")
        print("3. Render service is experiencing errors")
        print()
        print("Try visiting your Render service URL in a browser:")
        print(f"   {api_url}/health")
        return
    
    print()
    print("=" * 60)
    print("✅ All tests passed! Your setup is ready for deployment.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_lazada_api_scraper())
