"""
Fully automated Temu login - no manual intervention needed
Automatically detects when login is complete and saves cookies
"""
from playwright.sync_api import sync_playwright
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

def fully_auto_login_temu():
    """
    Fully automated login that:
    1. Opens Temu
    2. Clicks sign in
    3. Clicks Google button
    4. Fills in credentials
    5. Waits for login to complete
    6. Automatically saves cookies
    """
    
    email = os.getenv('TEMU_EMAIL')
    password = os.getenv('TEMU_PASSWORD')
    
    if not email or not password:
        print("❌ Error: TEMU_EMAIL and TEMU_PASSWORD not found in .env file")
        return False
    
    print("\n" + "="*60)
    print("FULLY AUTOMATED TEMU LOGIN")
    print("="*60)
    print(f"Email: {email}")
    print(f"Password: {'*' * len(password)}")
    print("\n🤖 Running fully automated login...")
    print("   (Browser will open and close automatically)\n")
    
    with sync_playwright() as p:
        # Launch browser
        print("🌐 Launching browser...")
        browser = p.chromium.launch(
            headless=False,  # Visible so you can see progress
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
        
        # Add stealth
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
            # Step 1: Go to Temu
            print("📱 Opening Temu homepage...")
            page.goto("https://www.temu.com", wait_until='networkidle', timeout=30000)
            time.sleep(2)
            
            # Step 2: Click Sign In
            print("🔍 Looking for Sign In button...")
            sign_in_clicked = False
            sign_in_selectors = [
                'text=Sign in',
                'text=Sign In', 
                'a:has-text("Sign")',
                'button:has-text("Sign")',
            ]
            
            for selector in sign_in_selectors:
                try:
                    page.click(selector, timeout=3000)
                    print(f"✅ Clicked Sign In")
                    sign_in_clicked = True
                    break
                except:
                    continue
            
            if not sign_in_clicked:
                print("⚠️  Couldn't find Sign In button, going directly to login page...")
                page.goto("https://www.temu.com/login.html", wait_until='networkidle')
            
            time.sleep(2)
            
            # Step 3: Click Google button
            print("🔍 Looking for Google sign in button...")
            google_clicked = False
            google_selectors = [
                'text=Continue with Google',
                'button:has-text("Google")',
                '[aria-label*="Google"]',
            ]
            
            for selector in google_selectors:
                try:
                    page.click(selector, timeout=3000)
                    print(f"✅ Clicked Google button")
                    google_clicked = True
                    break
                except:
                    continue
            
            if not google_clicked:
                print("❌ Could not find Google button")
                page.screenshot(path='temu_no_google_button.png')
                print("   Screenshot saved to: temu_no_google_button.png")
                browser.close()
                return False
            
            # Step 4: Handle Google OAuth
            print("⏳ Waiting for Google OAuth page...")
            time.sleep(3)
            
            # Find Google page (popup or redirect)
            google_page = None
            for i in range(10):  # Try for 10 seconds
                if len(context.pages) > 1:
                    google_page = context.pages[-1]
                    break
                elif 'google.com' in page.url or 'accounts.google.com' in page.url:
                    google_page = page
                    break
                time.sleep(1)
            
            if not google_page:
                print("❌ Google OAuth page not found")
                browser.close()
                return False
            
            print("✅ Found Google OAuth page")
            
            # Step 5: Fill email
            print(f"📧 Entering email...")
            try:
                google_page.wait_for_selector('input[type="email"]', timeout=10000)
                google_page.fill('input[type="email"]', email)
                time.sleep(0.5)
                
                # Click Next
                try:
                    google_page.click('#identifierNext', timeout=3000)
                except:
                    google_page.press('input[type="email"]', 'Enter')
                
                print("✅ Email entered")
                time.sleep(3)
                
            except Exception as e:
                print(f"❌ Failed to enter email: {e}")
                browser.close()
                return False
            
            # Step 6: Fill password
            print(f"🔑 Entering password...")
            try:
                google_page.wait_for_selector('input[type="password"]', timeout=10000)
                google_page.fill('input[type="password"]', password)
                time.sleep(0.5)
                
                # Click Next
                try:
                    google_page.click('#passwordNext', timeout=3000)
                except:
                    google_page.press('input[type="password"]', 'Enter')
                
                print("✅ Password entered")
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Failed to enter password: {e}")
                browser.close()
                return False
            
            # Step 7: Wait for redirect back to Temu
            print("⏳ Waiting for redirect back to Temu...")
            
            # Wait up to 30 seconds for redirect
            for i in range(30):
                current_url = page.url
                if 'temu.com' in current_url and 'login' not in current_url:
                    print(f"✅ Redirected back to Temu: {current_url}")
                    break
                time.sleep(1)
            else:
                print("⚠️  Timeout waiting for redirect")
            
            time.sleep(3)
            
            # Step 8: Verify login by testing search
            print("🔍 Verifying login with search test...")
            page.goto("https://www.temu.com/search_result.html?search_key=phone", wait_until='networkidle', timeout=30000)
            time.sleep(3)
            
            if 'login' in page.url:
                print("❌ Still redirecting to login - login failed")
                page.screenshot(path='temu_login_failed.png')
                print("   Screenshot saved to: temu_login_failed.png")
                browser.close()
                return False
            
            print("✅ Login verified - search works!")
            
            # Step 9: Save cookies
            print("\n💾 Saving session...")
            cookies = context.cookies()
            
            with open('cookies_temu.json', 'w') as f:
                json.dump(cookies, f, indent=2)
            print(f"   ✅ Saved {len(cookies)} cookies to cookies_temu.json")
            
            # Save storage state
            context.storage_state(path='storage_temu.json')
            print("   ✅ Saved storage state to storage_temu.json")
            
            # Take success screenshot
            page.screenshot(path='temu_login_success.png')
            print("   📸 Screenshot saved to: temu_login_success.png")
            
            print("\n" + "="*60)
            print("🎉 SUCCESS! Fully automated login complete!")
            print("="*60)
            print("Your Temu scraper can now run automatically.")
            print("The session will stay valid for days/weeks.")
            print("="*60 + "\n")
            
            time.sleep(2)
            browser.close()
            return True
            
        except Exception as e:
            print(f"\n❌ Error during login: {e}")
            page.screenshot(path='temu_error.png')
            print("   Screenshot saved to: temu_error.png")
            browser.close()
            return False

if __name__ == "__main__":
    print("\n⚠️  IMPORTANT NOTES:")
    print("1. This will open a visible browser window")
    print("2. The entire process takes 20-30 seconds")
    print("3. If Google asks for 2FA, you'll need to handle it manually")
    print("4. Watch the browser to see progress")
    print("\n🚀 Starting in 3 seconds...\n")
    
    time.sleep(3)
    
    success = fully_auto_login_temu()
    
    if success:
        print("\n✅ Ready to use! Run this to test:")
        print("   python3 test_temu_with_saved_cookies.py")
    else:
        print("\n❌ Login failed. Possible reasons:")
        print("   1. Google detected automation (try manual login)")
        print("   2. 2FA is enabled (disable temporarily)")
        print("   3. Wrong credentials (check .env file)")
        print("\n   Try manual login instead:")
        print("   python3 simple_login_temu.py")
