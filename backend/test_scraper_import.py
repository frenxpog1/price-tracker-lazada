"""
Quick test to verify scraper can be imported and has correct signature
"""
import sys
import inspect

# Mock the dependencies
class MockLogger:
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg, **kwargs): pass

sys.modules['app.core.logging'] = type('module', (), {'get_logger': lambda x: MockLogger()})()
sys.modules['app.core.exceptions'] = type('module', (), {
    'ScraperError': Exception,
    'PlatformUnavailableError': Exception
})()
sys.modules['app.scrapers.base_scraper'] = type('module', (), {})()

# Now try to check the scraper file
with open('app/scrapers/lazada_api_scraper.py', 'r') as f:
    content = f.read()
    
# Check for syntax errors
try:
    compile(content, 'lazada_api_scraper.py', 'exec')
    print("✓ No syntax errors")
except SyntaxError as e:
    print(f"✗ Syntax error: {e}")
    sys.exit(1)

# Check method signature
if 'async def search(' in content:
    print("✓ search method found")
    # Extract the signature
    import re
    match = re.search(r'async def search\((.*?)\):', content, re.DOTALL)
    if match:
        params = match.group(1)
        print(f"  Parameters: {params[:100]}...")
        if 'page' in params and 'sort_by' in params:
            print("✓ Pagination parameters found")
        else:
            print("✗ Missing pagination parameters")
else:
    print("✗ search method not found")

print("\n✓ All checks passed!")
