#!/usr/bin/env python3
"""
Test the V2 scrapers with visible browser (anti-detection)
"""

import asyncio
import sys

async def test_shopee_v2():
    print("=" * 60)
    print("Testing Shopee V2 Scraper (Visible Browser)")
    print("=" * 60)
    
    try:
        from scrapers.shopee_scraper_v2 import ShopeeScraperV2
        
        scraper = ShopeeScraperV2()
        async with scraper:
            print("✅ Browser started (visible window)")
            print("🔍 Searching for 'phone'...")
            print("⏳ This will take 15-20 seconds...")
            
            results, total = await scraper.search("phone", max_results=3)
            
            print(f"\n📊 Results:")
            print(f"   Total found: {total}")
            print(f"   Returned: {len(results)}")
            
            if results:
                print(f"\n✅ SUCCESS! Found {len(results)} products")
                for i, product in enumerate(results, 1):
                    print(f"\n   Product {i}:")
                    print(f"   Name: {product.product_name[:60]}...")
                    print(f"   Price: {product.current_price} {product.currency}")
                    print(f"   URL: {product.product_url[:60]}...")
                return True
            else:
                print("\n❌ No products found")
                return False
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_temu_v2():
    print("\n" + "=" * 60)
    print("Testing Temu V2 Scraper (Visible Browser)")
    print("=" * 60)
    
    try:
        from scrapers.temu_scraper_v2 import TemuScraperV2
        
        scraper = TemuScraperV2()
        async with scraper:
            print("✅ Browser started (visible window)")
            print("🔍 Searching for 'phone'...")
            print("⏳ This will take 20-25 seconds...")
            
            results, total = await scraper.search("phone", max_results=3)
            
            print(f"\n📊 Results:")
            print(f"   Total found: {total}")
            print(f"   Returned: {len(results)}")
            
            if results:
                print(f"\n✅ SUCCESS! Found {len(results)} products")
                for i, product in enumerate(results, 1):
                    print(f"\n   Product {i}:")
                    print(f"   Name: {product.product_name[:60]}...")
                    print(f"   Price: {product.current_price} {product.currency}")
                    print(f"   URL: {product.product_url[:60]}...")
                return True
            else:
                print("\n❌ No products found")
                print("💡 Check temu_page_source.html to see what was loaded")
                return False
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("\n🧪 Testing V2 Scrapers with Anti-Detection")
    print("=" * 60)
    print("⚠️  Browser windows will open (not headless)")
    print("⚠️  This helps bypass bot detection")
    print("=" * 60 + "\n")
    
    results = {
        'shopee': False,
        'temu': False
    }
    
    # Test Shopee
    print("1️⃣  Testing Shopee...")
    results['shopee'] = await test_shopee_v2()
    
    # Wait a bit between tests
    await asyncio.sleep(2)
    
    # Test Temu
    print("\n2️⃣  Testing Temu...")
    results['temu'] = await test_temu_v2()
    
    # Summary
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    for platform, success in results.items():
        icon = "✅" if success else "❌"
        status = "WORKING" if success else "FAILED"
        print(f"{icon} {platform.capitalize()}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\n📊 Score: {passed}/{total} scrapers working")
    
    if passed == total:
        print("\n🎉 All V2 scrapers working!")
    elif passed > 0:
        print(f"\n⚠️  {passed} out of {total} working")
    else:
        print("\n❌ Bot detection still blocking")
        print("\n💡 Recommendations:")
        print("   1. Use Lazada only (it works!)")
        print("   2. Or invest in proxy rotation + CAPTCHA solving")
        print("   3. Or wait for official APIs")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test cancelled")
        sys.exit(1)
