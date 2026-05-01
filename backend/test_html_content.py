"""
Check what HTML content we're getting from Lazada.
"""
import requests
from bs4 import BeautifulSoup

url = "https://www.lazada.com.ph/catalog/?q=iphone%2010%20xr"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

response = requests.get(url, headers=headers, timeout=10)

print(f"Status Code: {response.status_code}")
print(f"Content Length: {len(response.content)}")
print("\n" + "=" * 60)
print("First 2000 characters of HTML:")
print("=" * 60)
print(response.text[:2000])

# Check for specific patterns
soup = BeautifulSoup(response.content, 'html.parser')

print("\n" + "=" * 60)
print("Looking for product-related elements:")
print("=" * 60)

# Check for data-qa-locator
qa_elements = soup.find_all(attrs={'data-qa-locator': True})
print(f"\nElements with data-qa-locator: {len(qa_elements)}")
if qa_elements:
    for elem in qa_elements[:5]:
        print(f"  - {elem.get('data-qa-locator')}")

# Check for common class patterns
print(f"\nDivs with class containing 'product': {len(soup.find_all('div', class_=lambda x: x and 'product' in x.lower()))}")
print(f"Divs with class containing 'item': {len(soup.find_all('div', class_=lambda x: x and 'item' in x.lower()))}")

# Check for script tags (JavaScript)
scripts = soup.find_all('script')
print(f"\nScript tags found: {len(scripts)}")

# Check if it's a JavaScript-heavy page
if 'window.__INITIAL_STATE__' in response.text or 'window.__APP_DATA__' in response.text:
    print("\n⚠️  This page uses JavaScript to render content!")
    print("   Need to use Playwright or Selenium instead of requests+BeautifulSoup")
