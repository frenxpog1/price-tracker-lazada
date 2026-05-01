"""
Automated login to Temu using Google OAuth
This will log in automatically and save cookies for the scraper to use
"""
from playwright.sync_api import sync_playwright
import json
import time
import os
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

def auto_login_temu():
    """Automatically log in to Temu with Google account"""
    
    email = os.getenv('TEMU_EMAIL')
    password = os.getenv('TEMU_PASSWORD')
    
    if not email or not password:
        print("❌ Error: TEMU_EMAIL and TEMU_PASSWORD not found in .env file")
        print("   Please create a .env file with your credentials")
        return False
    
    print("\n" + "="*60)
    print("AUTOMATED TEMU LOGIN")
    print("="*60)
    print(f"Email: {email}")
    print(f"Password: {'*' * len(password)}")
    print()
    
    with sync_playwright() as p:
        # Launch browser (visible so you can see what's happening)
        print("🌐 Launching browser...")
        browser = p.chromium.launch(
            headless=False,  # Set to True for production
            args=['--disable-blink-features=AutomationControlled']
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
            window.chrome = { runtime: {} };
        """)
        
        try:
            # Go to Temu
            print("📱 Opening Temu...")
            page.goto("https://www.temu.com", wait_until='networkidle')
            time.sleep(2)
            
            # Click Sign In button
            print("🔍 Looking for Sign In button...")
            try:
                # Try multiple selectors for sign in button
                sign_in_selectors = [
                    'text=Sign in',
                    'text=Sign In',
                    'text=Login',
                    'a[href*="login"]',
                    'button:has-text("Sign")',
                ]
                
                for selector in sign_in_selectors:
                    try:
                        page.click(selector, timeout=3000)
                        print(f"✅ Clicked sign in with selector: {selector}")
                        break
                    except:
                        continue
                
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️  Could not find sign in button: {e}")
                print("   Trying to go directly to login page...")
                page.goto("https://www.temu.com/login.html", wait_until='networkidle')
                time.sleep(2)
            
            # Look for Google sign in button
            print("🔍 Looking for Google sign in button...")
            google_selectors = [
                'text=Continue with Google',
                'button:has-text("Google")',
                '[class*="google"]',
                'img[alt*="Google"]',
            ]
            
            google_clicked = False
            for selector in google_selectors:
                try:
                    page.click(selector, timeout=3000)
                    print(f"✅ Clicked Google button with selector: {selector}")
                    google_clicked = True
                    break
                except:
                    continue
            
            if not google_clicked:
                print("❌ Could not find Google sign in button")
                print("   Taking screenshot for debugging...")
                page.screenshot(path='temu_login_page.png')
                print("   Screenshot saved to: temu_login_page.png")
                
                # Manual fallback
                print("\n⚠️  MANUAL INTERVENTION NEEDED:")
                print("   1. Click the Google sign in button in the browser")
                print("   2. Complete the login process")
                print("   3. Press ENTER here when done")
                input("\nPress ENTER after logging in...")
                
            else:
                # Wait for Google popup/redirect
                print("⏳ Waiting for Google OAuth page...")
                time.sleep(3)
                
                # Handle Google OAuth - it might be a popup or redirect
                print("🔐 Handling Google OAuth...")
                
                # Wait for either popup or redirect
                google_page = None
                
                # Check for popup window
                if len(context.pages) > 1:
                    google_page = context.pages[-1]
                    print("   Found popup window")
                else:
                    # Check if current page is Google
                    if 'google.com' in page.url or 'accounts.google.com' in page.url:
                        google_page = page
                        print("   Redirected to Google")
                    else:
                        # Wait a bit more for popup
                        time.sleep(2)
                        if len(context.pages) > 1:
                            google_page = context.pages[-1]
                
                if google_page:
                    # Fill in email
                    print(f"📧 Entering email: {email}")
                    try:
                        # Wait for email input to be visible
                        google_page.wait_for_selector('input[type="email"]', timeout=10000)
                        google_page.fill('input[type="email"]', email)
                        time.sleep(1)
                        
                        # Click Next button
                        google_page.click('#identifierNext', timeout=5000)
                        time.sleep(3)
                        
                        print("✅ Email entered")
                    except Exception as e:
                        print(f"⚠️  Email step failed: {e}")
                        print("   Trying alternative selectors...")
                        try:
                            google_page.fill('input[name="identifier"]', email)
                            google_page.press('input[name="identifier"]', 'Enter')
                            time.sleep(3)
                        except:
                            pass
                    
                    # Fill in password
                    print("🔑 Entering password...")
                    try:
                        # Wait for password input
                        google_page.wait_for_selector('input[type="password"]', timeout=10000)
                        google_page.fill('input[type="password"]', password)
                        time.sleep(1)
                        
                        # Click Next button
                        google_page.click('#passwordNext', timeout=5000)
                        time.sleep(5)
                        
                        print("✅ Password entered")
                    except Exception as e:
                        print(f"⚠️  Password step failed: {e}")
                        print("   Trying alternative selectors...")
                        try:
                            google_page.fill('input[name="password"]', password)
                            google_page.press('input[name="password"]', 'Enter')
                            time.sleep(5)
                        except:
                            pass
                    
                    # Wait for redirect back to Temu
                    print("⏳ Waiting for redirect back to Temu...")
                    time.sleep(5)
                else:
                    print("⚠️  Could not find Google OAuth page")
                    print("   Manual intervention may be needed")
            
            # Check if we're logged in
            current_url = page.url
            print(f"📍 Current URL: {current_url}")
            
            if 'login' not in current_url:
                print("✅ Login successful!")
            else:
                print("⚠️  Still on login page - may need manual intervention")
                print("   Please complete any 2FA or CAPTCHA if needed")
                input("\nPress ENTER after completing login...")
            
            # Navigate to search to verify
            print("🔍 Testing search to verify login...")
            page.goto("https://www.temu.com/search_result.html?search_key=phone", wait_until='networkidle')
            time.sleep(3)
            
            if 'login' in page.url:
                print("❌ Still redirecting to login - login failed")
                return False
            
            print("✅ Login verified - can access search!")
            
            # Save cookies
            print("💾 Saving cookies...")
            cookies = context.cookies()
            
            with open('cookies_temu.json', 'w') as f:
                json.dump(cookies, f, indent=2)
            print(f"   ✅ Saved {len(cookies)} cookies to cookies_temu.json")
            
            # Save storage state
            context.storage_state(path='storage_temu.json')
            print("   ✅ Saved storage state to storage_temu.json")
            
            print("\n🎉 SUCCESS! Your Temu scraper can now use these credentials.")
            print("   The session will stay valid for several days/weeks.")
            print("   Re-run this script if you get logged out.\n")
            
            time.sleep(2)
            browser.close()
            return True
            
        except Exception as e:
            print(f"\n❌ Error during login: {e}")
            print("   Taking screenshot...")
            page.screenshot(path='temu_login_error.png')
            print("   Screenshot saved to: temu_login_error.png")
            
            browser.close()
            return False

if __name__ == "__main__":
    success = auto_login_temu()
    
    if success:
        print("\n✅ You can now run the Temu scraper!")
        print("   It will use the saved cookies automatically.")
    else:
        print("\n❌ Login failed. Please check the error messages above.")
        print("   You may need to:")
        print("   1. Check your credentials in .env file")
        print("   2. Disable 2FA temporarily")
        print("   3. Complete CAPTCHA manually")
