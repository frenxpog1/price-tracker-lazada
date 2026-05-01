#!/usr/bin/env python3
"""
Debug script to inspect Shopee's actual HTML structure
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def debug_shopee():
    print("🔍 Debugging Shopee HTML Structure...")
    
    # Setup Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(15)
    
    try:
        # Navigate to Shopee search
        url = "https://shopee.ph/search?keyword=phone"
        print(f"📍 Loading: {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(5)
        
        # Scroll to trigger lazy loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5);")
        time.sleep(2)
        
        # Get page source
        html = driver.page_source
        
        # Save to file for inspection
        with open('shopee_debug.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("✅ Saved HTML to shopee_debug.html")
        
        # Try to find any divs that might be product cards
        print("\n🔍 Looking for potential product containers...")
        
        # Try common patterns
        selectors_to_try = [
            'div[data-sqe="item"]',
            '.shopee-search-item-result__item',
            '[class*="item-card"]',
            '[class*="product"]',
            'a[href*="/product/"]',
            'div[class*="col-"]',
        ]
        
        for selector in selectors_to_try:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found {len(elements)} elements with: {selector}")
                    # Print first element's HTML
                    if len(elements) > 0:
                        print(f"   Sample HTML: {elements[0].get_attribute('outerHTML')[:200]}...")
                else:
                    print(f"❌ No elements found with: {selector}")
            except Exception as e:
                print(f"❌ Error with {selector}: {e}")
        
        # Check page text
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        print(f"\n📄 Page text length: {len(body_text)} characters")
        print(f"📄 First 500 chars: {body_text[:500]}")
        
    finally:
        driver.quit()
        print("\n✅ Debug complete. Check shopee_debug.html for full HTML")

if __name__ == "__main__":
    debug_shopee()
