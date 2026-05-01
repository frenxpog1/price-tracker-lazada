"""
Simple semi-automated login for Temu
You just need to log in once manually, then cookies are saved forever
"""
from playwright.sync_api import sync_playwright
import json
import time

def simple_login_temu():
    """
    Open browser, let you log in manually (with Google or any method),
    then save cookies for automated use
    """
    print("\n" + "="*60)
    print("TEMU LOGIN - Save Cookies for Automation")
    print("="*60)
    print("\n📌 INSTRUCTIONS:")
    print("1. A browser will open to Temu")
    print("2. Log in using ANY method you prefer:")
    print("   - Google")
    print("   - Facebook")  
    print("   - Email/Password")
    print("   - Phone number")
    print("3. After logging in, search for 'phone' to verify")
    print("4. Come back here and press ENTER")
    print("\n⏳ Starting in 3 seconds...\n")
    time.sleep(3)
    
    with sync_playwright() as p:
        # Launch visible browser
        browser = p.chromium.launch(headless=False)
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        )
        
        page = context.new_page()
        
        # Add stealth
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.chrome = { runtime: {} };
        """)
        
        # Go to Temu
        print("🌐 Opening Temu...")
        page.goto("https://www.temu.com", wait_until='networkidle')
        
        # Wait for user to log in
        print("\n✋ Please log in to Temu in the browser window...")
        print("   After logging in, search for 'phone' to test")
        print("   Then come back here and press ENTER\n")
        
        input("Press ENTER after you've logged in and tested search...")
        
        # Verify login
        current_url = page.url
        print(f"\n📍 Current URL: {current_url}")
        
        if 'login' in current_url.lower():
            print("⚠️  Warning: You're still on the login page")
            print("   Make sure you completed the login process")
            
            retry = input("\nDo you want to try again? (y/n): ")
            if retry.lower() == 'y':
                input("Press ENTER after logging in...")
        
        # Test search
        print("\n🔍 Testing search...")
        page.goto("https://www.temu.com/search_result.html?search_key=phone", wait_until='networkidle')
        time.sleep(3)
        
        if 'login' in page.url:
            print("❌ Still redirecting to login - login verification failed")
            print("   Please make sure you're fully logged in")
            browser.close()
            return False
        
        print("✅ Login verified - search works!")
        
        # Save cookies
        print("\n💾 Saving session...")
        cookies = context.cookies()
        
        with open('cookies_temu.json', 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"   ✅ Saved {len(cookies)} cookies to cookies_temu.json")
        
        # Save storage state (includes localStorage, sessionStorage)
        context.storage_state(path='storage_temu.json')
        print("   ✅ Saved storage state to storage_temu.json")
        
        print("\n🎉 SUCCESS!")
        print("="*60)
        print("Your Temu scraper can now run automatically!")
        print("The session will stay valid for days/weeks.")
        print("Re-run this script only if you get logged out.")
        print("="*60 + "\n")
        
        time.sleep(2)
        browser.close()
        return True

if __name__ == "__main__":
    success = simple_login_temu()
    
    if not success:
        print("\n❌ Login failed. Please try again.")
