"""
Final attempt: Playwright with persistent context (saves cookies/session)
This simulates a real browser with browsing history
"""
from playwright.sync_api import sync_playwright
import time
import os

def test_temu_with_persistent_context():
    """Test Temu with persistent browser context (like a real user)"""
    print("Initializing Playwright with persistent context...")
    
    # Create a user data directory
    user_data_dir = './playwright_user_data'
    os.makedirs(user_data_dir, exist_ok=True)
    
    with sync_playwright() as p:
        # Launch with persistent context (saves cookies, localStorage, etc.)
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
            ],
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        # Add stealth scripts
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            window.chrome = { runtime: {} };
        """)
        
        try:
            # First, visit Temu homepage to establish session
            print("Step 1: Visiting Temu homepage to establish session...")
            page.goto("https://www.temu.com", wait_until='networkidle', timeout=30000)
            time.sleep(3)
            print(f"  Homepage URL: {page.url}")
            
            # Now try search
            url = "https://www.temu.com/search_result.html?search_key=phone"
            print(f"\nStep 2: Searching for products: {url}")
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            time.sleep(5)
            
            current_url = page.url
            print(f"\nCurrent URL: {current_url}")
            
            if 'login' in current_url:
                print("❌ REDIRECTED TO LOGIN PAGE")
                print("\nTemu's bot detection is too strong. It detects:")
                print("  - Headless browsers")
                print("  - Non-headless Selenium")
                print("  - Playwright (even with stealth)")
                print("  - Persistent contexts")
                print("\nTo bypass this, you would need:")
                print("  1. Residential proxy network")
                print("  2. Real browser fingerprinting")
                print("  3. CAPTCHA solving service")
                print("  4. Rotating user agents and IPs")
            else:
                print("✅ SUCCESS - We're on the search results page!")
                
                # Try to find products
                selectors = [
                    'a[href*="/goods.html"]',
                    'a[href*="goods_id"]',
                ]
                
                for selector in selectors:
                    elements = page.query_selector_all(selector)
                    if elements:
                        print(f"\n✅ FOUND {len(elements)} PRODUCTS with {selector}!")
                        for i, elem in enumerate(elements[:3]):
                            href = elem.get_attribute('href')
                            print(f"  [{i}] {href[:80]}...")
                        break
            
            print(f"\nPage title: {page.title()}")
            
            # Save screenshot
            page.screenshot(path='temu_persistent_screenshot.png')
            print("\n📸 Screenshot: temu_persistent_screenshot.png")
            
            print("\nWaiting 10 seconds...")
            time.sleep(10)
            
        finally:
            context.close()
            print("\n✅ Browser closed")

if __name__ == "__main__":
    test_temu_with_persistent_context()
