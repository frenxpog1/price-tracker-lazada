"""
Diagnostic script to check which scraper is being loaded
Run this with: python3 diagnose_scraper.py
"""
import os
import sys

# Set environment variable
os.environ['USE_REAL_SCRAPERS'] = 'true'

print("=" * 60)
print("SCRAPER DIAGNOSTIC")
print("=" * 60)

print(f"\n1. Environment Variable:")
print(f"   USE_REAL_SCRAPERS = {os.getenv('USE_REAL_SCRAPERS')}")

print(f"\n2. Checking scraper files:")
scrapers = [
    'app/scrapers/lazada_api_scraper.py',
    'app/scrapers/lazada_scraper.py',
    'app/scrapers/lazada_scraper_simple.py',
    'app/scrapers/mock_scraper.py'
]

for scraper in scrapers:
    exists = os.path.exists(scraper)
    print(f"   {'✓' if exists else '✗'} {scraper}")

print(f"\n3. Attempting to import scraper factory...")
try:
    from app.scrapers.scraper_factory import ScraperFactory
    print(f"   ✓ ScraperFactory imported successfully")
    
    print(f"\n4. Checking USE_REAL_SCRAPERS in factory...")
    from app.scrapers import scraper_factory
    print(f"   USE_REAL_SCRAPERS = {scraper_factory.USE_REAL_SCRAPERS}")
    
    print(f"\n5. Creating lazada scraper...")
    scraper = ScraperFactory.create_scraper('lazada')
    print(f"   ✓ Scraper created: {type(scraper).__name__}")
    print(f"   ✓ Scraper class: {scraper.__class__.__module__}.{scraper.__class__.__name__}")
    
    print(f"\n6. Checking search method signature...")
    import inspect
    sig = inspect.signature(scraper.search)
    print(f"   Parameters: {list(sig.parameters.keys())}")
    
    if 'page' in sig.parameters and 'sort_by' in sig.parameters:
        print(f"   ✓ Pagination supported!")
    else:
        print(f"   ✗ Pagination NOT supported (old scraper)")
        
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
