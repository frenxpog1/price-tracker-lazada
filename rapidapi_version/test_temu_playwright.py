"""
Test Temu with Playwright (better bot detection bypass than Selenium)
"""
from playwright.sync_api import sync_playwright
import time

def test_temu_playwright():
    """Test Temu with Playwright"""
    print("Initializing Playwright...")
    
    with sync_playwright() as p:
        # Launch browser - try non-headless first
        browser = p.chromium.launch(
            headless=False,  # Visible browser
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ]
        )
        
        # Create context with realistic settings
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
        )
        
        page = context.new_page()
        
        # Add stealth scripts manually
        page.add_init_script("""
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Override plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            // Chrome runtime
            window.chrome = {
                runtime: {}
            };
            
            // Permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)
        
        try:
            url = "https://www.temu.com/search_result.html?search_key=phone"
            print(f"Loading: {url}")
            print("Browser window will open - watch what happens...")
            
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Wait a bit for page to fully load
            time.sleep(5)
            
            # Check current URL
            current_url = page.url
            print(f"\nCurrent URL: {current_url}")
            
            # Check if redirected to login
            if 'login' in current_url:
                print("❌ REDIRECTED TO LOGIN PAGE - Still detected")
            else:
                print("✅ NO REDIRECT - We're on the search results page!")
            
            # Get page title
            print(f"Page title: {page.title()}")
            
            # Get body text preview
            body_text = page.inner_text('body')
            print(f"\nBody text (first 500 chars):\n{body_text[:500]}")
            
            # Try to find product links
            print("\n" + "="*60)
            print("LOOKING FOR PRODUCTS:")
            print("="*60)
            
            # Try multiple selectors
            selectors = [
                'a[href*="/goods.html"]',
                'a[href*="goods_id"]',
                '[class*="product"] a',
                '[data-testid*="product"]',
            ]
            
            for selector in selectors:
                try:
                    elements = page.query_selector_all(selector)
                    print(f"{selector}: Found {len(elements)} elements")
                    
                    if elements and len(elements) > 0:
                        print(f"  ✅ FOUND {len(elements)} PRODUCTS!")
                        # Show first 3
                        for i, elem in enumerate(elements[:3]):
                            href = elem.get_attribute('href')
                            text = elem.inner_text()[:50] if elem.inner_text() else "No text"
                            print(f"  [{i}] {text} - {href[:60] if href else 'No href'}...")
                        break
                except Exception as e:
                    print(f"{selector}: Error - {e}")
            
            # Take screenshot for debugging
            page.screenshot(path='temu_playwright_screenshot.png')
            print("\n📸 Screenshot saved to: temu_playwright_screenshot.png")
            
            # Save HTML
            html = page.content()
            with open('temu_playwright_page.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("💾 HTML saved to: temu_playwright_page.html")
            
            print("\nWaiting 10 seconds so you can see the browser...")
            time.sleep(10)
            
        finally:
            browser.close()
            print("\n✅ Browser closed")

if __name__ == "__main__":
    test_temu_playwright()
