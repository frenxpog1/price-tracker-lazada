# Quick Fix for "Only Showing Mock Scraping"

## Problem
The search is showing mock results instead of real Lazada results.

## Solution

### Step 1: Check if Backend is Running
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not running, start it:
cd backend
source venv/bin/activate  # or: . venv/bin/activate
python -m uvicorn app.main:app --reload
```

### Step 2: Verify Environment Variable
The backend needs `USE_REAL_SCRAPERS=true` to be set.

**Option A: Set in .env file** (RECOMMENDED)
```bash
# backend/.env should have:
USE_REAL_SCRAPERS=true
```

**Option B: Set in terminal**
```bash
export USE_REAL_SCRAPERS=true
python -m uvicorn app.main:app --reload
```

### Step 3: Test the API Directly
```bash
# Test if real scraper is being used
curl "http://localhost:8000/api/products/search?q=test&max_results=5" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Look for:
- ✓ Real product names (not "Mock Product 1", "Mock Product 2")
- ✓ Real prices
- ✓ Real image URLs

### Step 4: Check Backend Logs
When you search, the backend logs should show:
```
INFO: Loaded LazadaAPIScraper (API-based with pagination)
INFO: Creating REAL scraper for platform: lazada
INFO: Searching Lazada: query='test', page=1, sort=best_match
```

If you see:
```
INFO: Creating MOCK scraper for platform: lazada
```

Then `USE_REAL_SCRAPERS` is not being read correctly.

## Common Issues

### Issue 1: Environment Variable Not Set
**Symptom:** Logs show "Creating MOCK scraper"

**Fix:**
```bash
# Make sure .env file has:
USE_REAL_SCRAPERS=true

# Restart backend
```

### Issue 2: Old Code Cached
**Symptom:** Changes not taking effect

**Fix:**
```bash
# Stop backend (Ctrl+C)
# Clear Python cache
find backend -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
# Restart backend
python -m uvicorn app.main:app --reload
```

### Issue 3: Import Error
**Symptom:** Backend crashes on startup

**Fix:**
```bash
# Check if dependencies are installed
pip list | grep pydantic
pip list | grep beautifulsoup4
pip list | grep requests

# If missing, install:
pip install -r requirements.txt
```

## Quick Test Script

Create `backend/test_real_scraper.py`:
```python
import os
import asyncio

# Force real scrapers
os.environ['USE_REAL_SCRAPERS'] = 'true'

async def test():
    from app.scrapers.scraper_factory import ScraperFactory
    
    print("Creating scraper...")
    scraper = ScraperFactory.create_scraper('lazada')
    print(f"Scraper type: {type(scraper).__name__}")
    
    if 'Mock' in type(scraper).__name__:
        print("❌ USING MOCK SCRAPER")
        return
    
    print("✓ Using real scraper")
    print("\nTesting search...")
    
    async with scraper:
        results = await scraper.search("test", 5, 1, "best_match")
        
        if isinstance(results, dict):
            print(f"✓ Got dict with {len(results.get('products', []))} products")
            print(f"✓ Total count: {results.get('total_count', 0)}")
        elif isinstance(results, list):
            print(f"✓ Got list with {len(results)} products")
        
        print("\nFirst product:")
        products = results.get('products', results) if isinstance(results, dict) else results
        if products:
            p = products[0]
            print(f"  Name: {p.product_name}")
            print(f"  Price: {p.current_price}")
            print(f"  Platform: {p.platform}")

if __name__ == '__main__':
    asyncio.run(test())
```

Run it:
```bash
cd backend
python test_real_scraper.py
```

## Expected Output

**If working correctly:**
```
Creating scraper...
Scraper type: LazadaAPIScraper
✓ Using real scraper

Testing search...
✓ Got dict with 5 products
✓ Total count: 11806

First product:
  Name: iPhone XR 64GB...
  Price: 12999.00
  Platform: lazada
```

**If using mock:**
```
Creating scraper...
Scraper type: MockScraper
❌ USING MOCK SCRAPER
```

## Still Not Working?

1. **Check .env file location:**
   ```bash
   ls -la backend/.env
   cat backend/.env | grep USE_REAL_SCRAPERS
   ```

2. **Check if backend is reading .env:**
   ```bash
   # Add this to backend/app/main.py temporarily:
   print(f"USE_REAL_SCRAPERS = {os.getenv('USE_REAL_SCRAPERS')}")
   ```

3. **Try hardcoding it:**
   In `backend/app/scrapers/scraper_factory.py`, change:
   ```python
   USE_REAL_SCRAPERS = os.getenv("USE_REAL_SCRAPERS", "false").lower() == "true"
   ```
   To:
   ```python
   USE_REAL_SCRAPERS = True  # Force real scrapers
   ```

4. **Check Python version:**
   ```bash
   python --version  # Should be 3.11+
   ```

## Need More Help?

Share:
1. Backend startup logs
2. Output of: `cat backend/.env | grep USE_REAL_SCRAPERS`
3. Output of test script above
4. Any error messages you see
