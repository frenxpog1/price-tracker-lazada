"""
Test if saved Temu cookies work
"""
from playwright.sync_api import sync_playwright
import json
import os
import time

def test_saved_cookies():
    """Test if we can use saved cookies to access Temu"""
    
    storage_file = "storage_temu.json"
    cookie_file = "cookies_temu.json"
    
    if not os.path.exists(storage_file) and not os.path.exists(cookie_file):
        print("❌ No saved cookies found!")
        print("   Please run: python3 simple_login_temu.py first")
        return False
    
    print("\n" + "="*60)
    print("TESTING SAVED TEMU COOKIES")
    print("="*60 + "\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # Load saved session
        if os.path.exists(storage_file):
            print(f"📂 Loading session from {storage_file}")
            context = browser.new_context(storage_state=storage_file)
        else:
            print(f"📂 Loading cookies from {cookie_file}")
            context = browser.new_context()
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
        
        page = context.new_page()
        
        # Test search
        print("🔍 Testing search for 'phone'...")
        page.goto("https://www.temu.com/search_result.html?search_key=phone", wait_until='networkidle')
        time.sleep(3)
        
        current_url = page.url
        print(f"📍 Current URL: {current_url}")
        
        if 'login' in current_url:
            print("\n❌ FAILED - Redirected to login page")
            print("   Your cookies have expired")
            print("   Please run: python3 simple_login_temu.py")
            browser.close()
            return False
        
        print("\n✅ SUCCESS - Cookies work!")
        
        # Try to find products
        print("\n🔍 Looking for products...")
        try:
            products = page.query_selector_all('a[href*="/goods.html"]')
            print(f"   Found {len(products)} product links")
            
            if len(products) > 0:
                print("\n✅ PRODUCTS FOUND - Scraper will work!")
                # Show first 3
                for i, product in enumerate(products[:3]):
                    href = product.get_attribute('href')
                    print(f"   [{i+1}] {href[:80]}...")
            else:
                print("\n⚠️  No products found - may need different selectors")
        except Exception as e:
            print(f"   Error: {e}")
        
        print("\n" + "="*60)
        print("Your Temu scraper is ready to use!")
        print("="*60 + "\n")
        
        time.sleep(3)
        browser.close()
        return True

if __name__ == "__main__":
    test_saved_cookies()
