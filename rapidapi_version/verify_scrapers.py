#!/usr/bin/env python3
"""
Verification script to test if all scrapers are working correctly.
This tests each scraper individually without running the full API.
"""

import sys
import asyncio
from datetime import datetime

def test_imports():
    """Test if all modules can be imported"""
    print("=" * 60)
    print("STEP 1: Testing Imports")
    print("=" * 60)
    
    try:
        print("📦 Importing FastAPI...")
        from fastapi import FastAPI
        print("   ✅ FastAPI imported")
    except ImportError as e:
        print(f"   ❌ FastAPI import failed: {e}")
        print("   💡 Run: pip3 install fastapi uvicorn")
        return False
    
    try:
        print("📦 Importing Selenium...")
        from selenium import webdriver
        print("   ✅ Selenium imported")
    except ImportError as e:
        print(f"   ❌ Selenium import failed: {e}")
        print("   💡 Run: pip3 install selenium webdriver-manager")
        return False
    
    try:
        print("📦 Importing Pydantic...")
        from pydantic import BaseModel
        print("   ✅ Pydantic imported")
    except ImportError as e:
        print(f"   ❌ Pydantic import failed: {e}")
        print("   💡 Run: pip3 install pydantic")
        return False
    
    try:
        print("📦 Importing base scraper...")
        from scrapers.base_scraper import BaseScraper, ProductResult, ScraperError
        print("   ✅ Base scraper imported")
    except ImportError as e:
        print(f"   ❌ Base scraper import failed: {e}")
        return False
    
    try:
        print("📦 Importing Lazada scraper...")
        from scrapers.lazada_scraper import LazadaScraperAPI
        print("   ✅ Lazada scraper imported")
    except ImportError as e:
        print(f"   ❌ Lazada scraper import failed: {e}")
        return False
    
    try:
        print("📦 Importing Shopee scraper...")
        from scrapers.shopee_scraper import ShopeeScraperAPI
        print("   ✅ Shopee scraper imported")
    except ImportError as e:
        print(f"   ❌ Shopee scraper import failed: {e}")
        return False
    
    try:
        print("📦 Importing Temu scraper...")
        from scrapers.temu_scraper import TemuScraperAPI
        print("   ✅ Temu scraper imported")
    except ImportError as e:
        print(f"   ❌ Temu scraper import failed: {e}")
        return False
    
    print("\n✅ All imports successful!\n")
    return True

async def test_lazada_scraper():
    """Test Lazada scraper"""
    print("=" * 60)
    print("STEP 2: Testing Lazada Scraper")
    print("=" * 60)
    
    try:
        from scrapers.lazada_scraper import LazadaScraperAPI
        
        print("🔍 Initializing Lazada scraper...")
        scraper = LazadaScraperAPI()
        
        print("🌐 Starting browser...")
        async with scraper:
            print("✅ Browser started successfully")
            
            print("🔎 Searching for 'phone' (3 results)...")
            start_time = datetime.now()
            
            results, total = await scraper.search(
                query="phone",
                max_results=3,
                page=1,
                sort_by="best_match"
            )
            
            elapsed = (datetime.now() - start_time).total_seconds()
            
            print(f"⏱️  Search completed in {elapsed:.2f} seconds")
            print(f"📊 Total results found: {total}")
            print(f"📦 Products returned: {len(results)}")
            
            if results:
                print("\n📋 Sample Results:")
                for i, product in enumerate(results[:3], 1):
                    print(f"\n   Product {i}:")
                    print(f"   Name: {product.product_name[:60]}...")
                    print(f"   Price: {product.current_price} {product.currency}")
                    print(f"   URL: {product.product_url[:60]}...")
                    print(f"   Image: {'✅ Yes' if product.image_url else '❌ No'}")
                
                print("\n✅ Lazada scraper is WORKING!")
                return True
            else:
                print("❌ No results returned from Lazada")
                return False
                
    except Exception as e:
        print(f"❌ Lazada scraper failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_shopee_scraper():
    """Test Shopee scraper"""
    print("\n" + "=" * 60)
    print("STEP 3: Testing Shopee Scraper")
    print("=" * 60)
    
    try:
        from scrapers.shopee_scraper import ShopeeScraperAPI
        
        print("🔍 Initializing Shopee scraper...")
        scraper = ShopeeScraperAPI()
        
        print("🌐 Starting browser...")
        async with scraper:
            print("✅ Browser started successfully")
            
            print("🔎 Searching for 'phone' (3 results)...")
            start_time = datetime.now()
            
            results, total = await scraper.search(
                query="phone",
                max_results=3,
                page=1,
                sort_by="best_match"
            )
            
            elapsed = (datetime.now() - start_time).total_seconds()
            
            print(f"⏱️  Search completed in {elapsed:.2f} seconds")
            print(f"📊 Total results found: {total}")
            print(f"📦 Products returned: {len(results)}")
            
            if results:
                print("\n📋 Sample Results:")
                for i, product in enumerate(results[:3], 1):
                    print(f"\n   Product {i}:")
                    print(f"   Name: {product.product_name[:60]}...")
                    print(f"   Price: {product.current_price} {product.currency}")
                    print(f"   URL: {product.product_url[:60]}...")
                    print(f"   Image: {'✅ Yes' if product.image_url else '❌ No'}")
                
                print("\n✅ Shopee scraper is WORKING!")
                return True
            else:
                print("❌ No results returned from Shopee")
                return False
                
    except Exception as e:
        print(f"❌ Shopee scraper failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_temu_scraper():
    """Test Temu scraper"""
    print("\n" + "=" * 60)
    print("STEP 4: Testing Temu Scraper")
    print("=" * 60)
    
    try:
        from scrapers.temu_scraper import TemuScraperAPI
        
        print("🔍 Initializing Temu scraper...")
        scraper = TemuScraperAPI()
        
        print("🌐 Starting browser...")
        async with scraper:
            print("✅ Browser started successfully")
            
            print("🔎 Searching for 'phone' (3 results)...")
            start_time = datetime.now()
            
            results, total = await scraper.search(
                query="phone",
                max_results=3,
                page=1,
                sort_by="best_match"
            )
            
            elapsed = (datetime.now() - start_time).total_seconds()
            
            print(f"⏱️  Search completed in {elapsed:.2f} seconds")
            print(f"📊 Total results found: {total}")
            print(f"📦 Products returned: {len(results)}")
            
            if results:
                print("\n📋 Sample Results:")
                for i, product in enumerate(results[:3], 1):
                    print(f"\n   Product {i}:")
                    print(f"   Name: {product.product_name[:60]}...")
                    print(f"   Price: {product.current_price} {product.currency}")
                    print(f"   URL: {product.product_url[:60]}...")
                    print(f"   Image: {'✅ Yes' if product.image_url else '❌ No'}")
                
                print("\n✅ Temu scraper is WORKING!")
                return True
            else:
                print("❌ No results returned from Temu")
                return False
                
    except Exception as e:
        print(f"❌ Temu scraper failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("\n🧪 RapidAPI Scraper Verification Suite")
    print("=" * 60)
    print("This will test each scraper individually to verify they work.")
    print("Note: Each test will take 10-20 seconds as it scrapes real data.")
    print("=" * 60 + "\n")
    
    # Test imports first
    if not test_imports():
        print("\n❌ Import test failed. Please install missing dependencies.")
        print("\n💡 Quick fix:")
        print("   cd rapidapi_version")
        print("   pip3 install -r requirements.txt")
        return False
    
    # Test each scraper
    results = {
        'lazada': False,
        'shopee': False,
        'temu': False
    }
    
    # Test Lazada
    try:
        results['lazada'] = await test_lazada_scraper()
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        return False
    
    # Test Shopee
    try:
        results['shopee'] = await test_shopee_scraper()
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        return False
    
    # Test Temu
    try:
        results['temu'] = await test_temu_scraper()
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        return False
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for platform, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {platform.capitalize()}: {'WORKING' if status else 'FAILED'}")
    
    print(f"\n📊 Score: {passed}/{total} scrapers working")
    
    if passed == total:
        print("\n🎉 SUCCESS! All scrapers are working correctly!")
        print("✅ Your RapidAPI implementation is ready to deploy!")
    elif passed > 0:
        print(f"\n⚠️  PARTIAL SUCCESS: {passed} out of {total} scrapers working")
        print("💡 Fix the failed scrapers before deploying")
    else:
        print("\n❌ FAILURE: No scrapers are working")
        print("💡 Check your internet connection and dependencies")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
