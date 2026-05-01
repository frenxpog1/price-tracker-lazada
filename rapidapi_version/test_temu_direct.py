"""
Direct test of Temu scraping to debug what's happening
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_temu():
    """Test Temu scraping directly"""
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
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
        driver.get(url)
        
        time.sleep(5)
        
        # Check current URL
        print(f"Current URL: {driver.current_url}")
        
        # Get page title
        print(f"Page title: {driver.title}")
        
        # Get body text (first 1000 chars)
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        print(f"\nBody text (first 1000 chars):\n{body_text[:1000]}")
        
        # Try to find product links with different selectors
        selectors = [
            'a[href*="/goods.html"]',
            'a[href*="goods_id"]',
            '[class*="product"] a',
            '[class*="item"] a',
            'div[class*="goods"] a',
            'a[href]'  # All links
        ]
        
        print("\n" + "="*60)
        print("TESTING SELECTORS:")
        print("="*60)
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"{selector}: Found {len(elements)} elements")
                if elements and len(elements) > 0:
                    # Show first 3 hrefs
                    for i, elem in enumerate(elements[:3]):
                        href = elem.get_attribute('href')
                        print(f"  [{i}] {href}")
            except Exception as e:
                print(f"{selector}: Error - {e}")
        
        # Save screenshot
        driver.save_screenshot('temu_test_screenshot.png')
        print("\nScreenshot saved to: temu_test_screenshot.png")
        
        # Save HTML
        with open('temu_test_page.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("HTML saved to: temu_test_page.html")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_temu()
