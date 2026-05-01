"""
Simple login for Shopee - save cookies for automation
"""
from playwright.sync_api import sync_playwright
import json
import time

def simple_login_shopee():
    """Log in to Shopee once, save cookies forever"""
    
    print("\n" + "="*60)
    print("SHOPEE LOGIN - Save Cookies for Automation")
    print("="*60)
    print("\n📌 INSTRUCTIONS:")
    print("1. A browser will open to Shopee")
    print("2. Log in using ANY method (Google, Facebook, Phone)")
    print("3. After logging in, search for 'phone' to verify")
    print("4. Come back here and press ENTER\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        )
        
        page = context.new_page()
        
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.chrome = { runtime: {} };
        """)
        
        print("🌐 Opening Shopee...")
        page.goto("https://shopee.ph", wait_until='networkidle')
        
        print("\n✋ Please log in to Shopee in the browser...")
        print("   Then search for 'phone' to test")
        print("   Come back and press ENTER\n")
        
        input("Press ENTER after logging in...")
        
        # Test search
        print("\n🔍 Testing search...")
        page.goto("https://shopee.ph/search?keyword=phone", wait_until='networkidle')
        time.sleep(3)
        
        if 'login' in page.url.lower() or 'unavailable' in page.text.lower():
            print("⚠️  Warning: May not be fully logged in")
        else:
            print("✅ Login verified!")
        
        # Save cookies
        print("\n💾 Saving session...")
        cookies = context.cookies()
        
        with open('cookies_shopee.json', 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"   ✅ Saved {len(cookies)} cookies")
        
        context.storage_state(path='storage_shopee.json')
        print("   ✅ Saved storage state")
        
        print("\n🎉 SUCCESS! Shopee scraper ready!\n")
        
        time.sleep(2)
        browser.close()
        return True

if __name__ == "__main__":
    simple_login_shopee()
