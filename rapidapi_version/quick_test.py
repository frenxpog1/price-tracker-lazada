#!/usr/bin/env python3
"""
Quick test - just checks if one scraper works.
Fastest way to verify the implementation.
"""

import asyncio
import sys

async def quick_test():
    print("🔍 Quick Test - Testing Lazada Scraper")
    print("=" * 50)
    
    try:
        # Try importing
        print("📦 Importing scraper...")
        from scrapers.lazada_scraper import LazadaScraperAPI
        print("✅ Import successful")
        
        # Try running
        print("\n🌐 Starting browser and searching...")
        print("   (This takes 5-10 seconds...)")
        
        scraper = LazadaScraperAPI()
        async with scraper:
            results, total = await scraper.search("phone", max_results=2, page=1)
            
            if results and len(results) > 0:
                print(f"\n✅ SUCCESS! Found {len(results)} products")
                print(f"📊 Total available: {total}")
                print(f"\n📦 Sample product:")
                print(f"   {results[0].product_name[:60]}")
                print(f"   Price: {results[0].current_price} {results[0].currency}")
                print(f"\n🎉 Your scrapers are WORKING!")
                print(f"💡 Run './install_and_test.sh' to test all platforms")
                return True
            else:
                print("\n❌ No results returned")
                return False
                
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\n💡 Install dependencies first:")
        print("   pip3 install -r requirements.txt")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(quick_test())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test cancelled")
        sys.exit(1)
