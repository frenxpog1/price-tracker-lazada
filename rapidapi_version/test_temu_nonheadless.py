"""
Test Temu with NON-HEADLESS browser (visible window)
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_temu_nonheadless():
    """Test Temu with visible browser"""
    chrome_options = Options()
    # NO HEADLESS MODE
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Exclude automation switches
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(20)
    
    # Execute CDP commands
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    })
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        url = "https://www.temu.com/search_result.html?search_key=phone"
        print(f"Loading: {url}")
        print("A Chrome window will open - watch what happens...")
        driver.get(url)
        
        time.sleep(5)
        
        # Check current URL
        print(f"\nCurrent URL: {driver.current_url}")
        
        # Check if redirected to login
        if 'login' in driver.current_url:
            print("❌ REDIRECTED TO LOGIN PAGE - Bot detected even in non-headless mode")
        else:
            print("✅ NO REDIRECT - We're on the search results page!")
        
        # Get page title
        print(f"Page title: {driver.title}")
        
        # Try to find product links
        selectors = [
            'a[href*="/goods.html"]',
            'a[href*="goods_id"]',
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"{selector}: Found {len(elements)} elements")
                if elements and len(elements) > 0:
                    print(f"  ✅ FOUND PRODUCTS!")
                    # Show first 3
                    for i, elem in enumerate(elements[:3]):
                        href = elem.get_attribute('href')
                        print(f"  [{i}] {href[:80]}...")
                    break
            except Exception as e:
                print(f"{selector}: Error - {e}")
        
        print("\nWaiting 10 seconds so you can see the browser...")
        time.sleep(10)
        
    finally:
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    test_temu_nonheadless()
