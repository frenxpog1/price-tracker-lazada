"""
Test Temu with undetected-chromedriver (stealth mode)
"""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

def test_temu_undetected():
    """Test Temu with undetected chromedriver"""
    print("Initializing undetected Chrome...")
    
    options = uc.ChromeOptions()
    # options.add_argument('--headless=new')  # Don't use headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = uc.Chrome(options=options)
    
    try:
        url = "https://www.temu.com/search_result.html?search_key=phone"
        print(f"Loading: {url}")
        driver.get(url)
        
        time.sleep(6)
        
        # Check current URL
        print(f"\nCurrent URL: {driver.current_url}")
        
        # Check if redirected to login
        if 'login' in driver.current_url:
            print("❌ REDIRECTED TO LOGIN PAGE - Still detected")
        else:
            print("✅ NO REDIRECT - We're on the search results page!")
        
        # Get page title
        print(f"Page title: {driver.title}")
        
        # Get body text preview
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        print(f"\nBody text (first 500 chars):\n{body_text[:500]}")
        
        # Try to find product links
        selectors = [
            'a[href*="/goods.html"]',
            'a[href*="goods_id"]',
        ]
        
        print("\n" + "="*60)
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"{selector}: Found {len(elements)} elements")
                if elements and len(elements) > 0:
                    print(f"  ✅ FOUND {len(elements)} PRODUCTS!")
                    # Show first 3
                    for i, elem in enumerate(elements[:3]):
                        href = elem.get_attribute('href')
                        text = elem.text[:50] if elem.text else "No text"
                        print(f"  [{i}] {text} - {href[:60]}...")
            except Exception as e:
                print(f"{selector}: Error - {e}")
        
    finally:
        driver.quit()
        print("\nBrowser closed")

if __name__ == "__main__":
    test_temu_undetected()
