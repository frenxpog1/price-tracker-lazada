"""
Temu login using email/password (bypasses Google's bot detection)
"""
from playwright.sync_api import sync_playwright
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

def email_login_temu():
    """
    Log in to Temu using email/password instead of Google
    This bypasses Google's "browser not secure" error
    """
    
    email = os.getenv('TEMU_EMAIL')
    password = os.getenv('TEMU_PASSWORD')
    
    if not email or not password:
        print("❌ Error: TEMU_EMAIL and TEMU_PASSWORD not found in .env file")
        return False
    
    print("\n" + "="*60)
    print("TEMU EMAIL/PASSWORD LOGIN")
    print("="*60)
    print(f"Email: {email}")
    print(f"Password: {'*' * len(password)}")
    print("\n🔐 Using email/password login (no Google OAuth)")
    print("   This avoids Google's bot detection\n")
    
    with sync_playwright() as p:
        print("🌐 Launching browser...")
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
            ]
        )
        
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
        
        try:
            # Go to login page
            print("📱 Opening Temu login page...")
            page.goto("https://www.temu.com/login.html", wait_until='networkidle')
            time.sleep(2)
            
            # Look for email input
            print("🔍 Looking for email/password login option...")
            
            # Try to find and click "Sign in with email" or similar
            email_login_selectors = [
                'text=Sign in with email',
                'text=Use email',
                'text=Email',
                'button:has-text("email")',
                'a:has-text("email")',
            ]
            
            email_option_found = False
            for selector in email_login_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print(f"✅ Clicked email login option")
                    email_option_found = True
                    time.sleep(1)
                    break
                except:
                    continue
            
            # Try to find email input field
            print("📧 Looking for email input...")
            email_input_selectors = [
                'input[type="email"]',
                'input[name="email"]',
                'input[placeholder*="email" i]',
                'input[placeholder*="Email" i]',
            ]
            
            email_input_found = False
            for selector in email_input_selectors:
                try:
                    page.wait_for_selector(selector, timeout=3000)
                    page.fill(selector, email)
                    print(f"✅ Entered email")
                    email_input_found = True
                    time.sleep(1)
                    break
                except:
                    continue
            
            if not email_input_found:
                print("\n⚠️  Could not find email input field")
                print("   Temu might not support direct email/password login")
                print("   OR the page structure is different\n")
                print("📸 Taking screenshot for debugging...")
                page.screenshot(path='temu_login_page_structure.png')
                print("   Screenshot saved to: temu_login_page_structure.png\n")
                
                print("💡 ALTERNATIVE SOLUTION:")
                print("   1. In the browser window, manually log in with email/password")
                print("   2. (Don't use Google - use email/password or phone)")
                print("   3. After logging in, search for 'phone'")
                print("   4. Come back here and press ENTER\n")
                
                input("Press ENTER after logging in manually...")
                
            else:
                # Try to find password input
                print("🔑 Looking for password input...")
                password_input_selectors = [
                    'input[type="password"]',
                    'input[name="password"]',
                    'input[placeholder*="password" i]',
                ]
                
                for selector in password_input_selectors:
                    try:
                        page.wait_for_selector(selector, timeout=3000)
                        page.fill(selector, password)
                        print(f"✅ Entered password")
                        time.sleep(1)
                        break
                    except:
                        continue
                
                # Click submit/login button
                print("🔘 Looking for submit button...")
                submit_selectors = [
                    'button[type="submit"]',
                    'button:has-text("Sign in")',
                    'button:has-text("Log in")',
                    'button:has-text("Continue")',
                ]
                
                for selector in submit_selectors:
                    try:
                        page.click(selector, timeout=2000)
                        print(f"✅ Clicked submit button")
                        time.sleep(3)
                        break
                    except:
                        continue
                
                print("⏳ Waiting for login to complete...")
                time.sleep(5)
            
            # Test if logged in
            print("\n🔍 Testing if login was successful...")
            page.goto("https://www.temu.com/search_result.html?search_key=phone", wait_until='networkidle')
            time.sleep(3)
            
            if 'login' in page.url:
                print("❌ Still on login page - login failed")
                page.screenshot(path='temu_login_failed.png')
                browser.close()
                return False
            
            print("✅ Login successful!")
            
            # Save cookies
            print("\n💾 Saving session...")
            cookies = context.cookies()
            
            with open('cookies_temu.json', 'w') as f:
                json.dump(cookies, f, indent=2)
            print(f"   ✅ Saved {len(cookies)} cookies to cookies_temu.json")
            
            context.storage_state(path='storage_temu.json')
            print("   ✅ Saved storage state to storage_temu.json")
            
            page.screenshot(path='temu_login_success.png')
            print("   📸 Screenshot saved")
            
            print("\n" + "="*60)
            print("🎉 SUCCESS! Cookies saved!")
            print("="*60)
            print("Your Temu scraper can now run automatically.")
            print("="*60 + "\n")
            
            time.sleep(2)
            browser.close()
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            page.screenshot(path='temu_error.png')
            browser.close()
            return False

if __name__ == "__main__":
    print("\n💡 TIP: If Temu doesn't have email/password login,")
    print("   you can log in manually with any method when prompted.\n")
    
    time.sleep(2)
    
    success = email_login_temu()
    
    if success:
        print("\n✅ Test the cookies:")
        print("   /usr/bin/python3 test_temu_with_saved_cookies.py")
    else:
        print("\n❌ Login failed")
