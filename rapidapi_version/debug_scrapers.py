"""
Debug script to save HTML from Shopee and Temu for selector analysis
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def save_page_html(url, filename):
    """Save HTML from a page"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(15)
    
    try:
        print(f"Loading {url}...")
        driver.get(url)
        time.sleep(3)
        
        # Scroll to load content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5);")
        time.sleep(1)
        
        html = driver.page_source
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Saved HTML to {filename} ({len(html)} bytes)")
        
        # Also print page text to see what's visible
        body_text = driver.find_element('tag name', 'body').text
        print(f"\nPage text preview (first 500 chars):")
        print(body_text[:500])
        
    finally:
        driver.quit()

if __name__ == "__main__":
    # Test Shopee
    print("=" * 60)
    print("TESTING SHOPEE")
    print("=" * 60)
    save_page_html(
        "https://shopee.ph/search?keyword=phone&page=0",
        "shopee_debug.html"
    )
    
    print("\n" + "=" * 60)
    print("TESTING TEMU")
    print("=" * 60)
    save_page_html(
        "https://www.temu.com/search_result.html?search_key=phone",
        "temu_debug.html"
    )
