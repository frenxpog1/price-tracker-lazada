"""
Helper script to manually log in to Temu/Shopee and save cookies
Run this once to save your login session, then the scrapers can reuse it
"""
from playwright.sync_api import sync_playwright
import json
import time

def save_cookies_for_platform(platform_name, url):
    """
    Open a browser, let user log in manually, then save cookies
    
    Args:
        platform_name: "temu", "shopee", or "tiktokshop"
        url: The login or homepage URL
    """
    print(f"\n{'='*60}")
    print(f"MANUAL LOGIN FOR {platform_name.upper()}")
    print(f"{'='*60}\n")
    
    with sync_playwright() as p:
        # Launch visible browser
        browser = p.chromium.launch(headless=False)
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        )
        
        page = context.new_page()
        
        # Add stealth scripts
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.chrome = { runtime: {} };
        """)
        
        print(f"Opening {url}...")
        print("\n📌 INSTRUCTIONS:")
        print("1. A browser window will open")
        print("2. Log in to your account manually")
        print("3. After logging in, navigate to the search page")
        print("4. Make sure you can see products")
        print("5. Come back here and press ENTER\n")
        
        page.goto(url)
        
        # Wait for user to log in
        input("Press ENTER after you've logged in and can see the site working...")
        
        # Save cookies
        cookies = context.cookies()
        
        # Save to file
        cookie_file = f"cookies_{platform_name}.json"
        with open(cookie_file, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print(f"\n✅ Cookies saved to: {cookie_file}")
        print(f"   Total cookies: {len(cookies)}")
        
        # Save storage state (includes localStorage, sessionStorage)
        storage_file = f"storage_{platform_name}.json"
        context.storage_state(path=storage_file)
        print(f"✅ Storage state saved to: {storage_file}")
        
        print("\n🎉 Done! Your scrapers can now use these credentials.")
        print("   The cookies will be valid for a few days/weeks.")
        print("   Re-run this script if you get logged out.\n")
        
        browser.close()

def main():
    """Main menu to choose which platform to log in to"""
    print("\n" + "="*60)
    print("COOKIE SAVER - Manual Login Helper")
    print("="*60)
    print("\nChoose a platform to log in to:")
    print("1. Temu")
    print("2. Shopee")
    print("3. TikTok Shop")
    print("4. All platforms (one by one)")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-4): ").strip()
    
    platforms = {
        '1': ('temu', 'https://www.temu.com'),
        '2': ('shopee', 'https://shopee.ph'),
        '3': ('tiktokshop', 'https://www.tiktokshop.com'),
    }
    
    if choice == '0':
        print("Goodbye!")
        return
    elif choice == '4':
        # Do all platforms
        for name, url in platforms.values():
            save_cookies_for_platform(name, url)
            time.sleep(2)
    elif choice in platforms:
        name, url = platforms[choice]
        save_cookies_for_platform(name, url)
    else:
        print("Invalid choice!")
        return

if __name__ == "__main__":
    main()
