# Troubleshooting: "Only Showing Mock Results"

## Quick Diagnosis

### Step 1: Check Backend Logs
When you search on the frontend, look at your backend terminal. You should see:

**✓ GOOD (Real Scraper):**
```
INFO: Loaded LazadaAPIScraper (API-based with pagination)
INFO: Creating REAL scraper for platform: lazada
INFO: Searching Lazada: query='iphone', page=1, sort=best_match
INFO: Found 40 product cards on page 1
INFO: Total items found: 11806
```

**✗ BAD (Mock Scraper):**
```
INFO: Creating MOCK scraper for platform: lazada
```

### Step 2: Check What You See
Look at the product names in the search results:

**✓ GOOD (Real Products):**
- "iPhone XR 64GB Smartphone..."
- "Apple iPhone XR 128GB..."
- Real prices like ₱12,999

**✗ BAD (Mock Products):**
- "Mock Product 1 from lazada"
- "Mock Product 2 from lazada"
- Fake prices like ₱999.99

## Solution

### If You See Mock Products:

**1. Restart Backend with Environment Variable:**
```bash
# Stop backend (Ctrl+C in backend terminal)

# Make sure you're in backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Set environment variable AND start
USE_REAL_SCRAPERS=true python -m uvicorn app.main:app --reload
```

**2. Or Update .env File:**
```bash
# Edit backend/.env
# Make sure it has:
USE_REAL_SCRAPERS=true

# Then restart backend:
python -m uvicorn app.main:app --reload
```

**3. Clear Python Cache:**
```bash
# Sometimes Python caches old code
cd backend
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete

# Restart backend
python -m uvicorn app.main:app --reload
```

## Verify It's Working

### Method 1: Check Backend Logs
Search for something on the frontend, then look at backend logs.

You should see:
```
INFO: User <user_id> searching for: iphone (page=1, sort=best_match)
INFO: Searching all platforms for: iphone (page=1, sort=best_match)
INFO: Searching Lazada: query='iphone', page=1, sort=best_match
```

### Method 2: Check Product Names
Real products will have:
- Real product names (not "Mock Product X")
- Real prices (not ₱999.99, ₱1999.99)
- Real images (not placeholder images)
- Platform badges (Lazada, Shopee, etc.)

### Method 3: Check Total Count
If pagination is working, you should see:
```
"11,806 items found for 'iphone 10 xr'"
```

Not:
```
"Search Results (20)"
```

## Common Issues

### Issue 1: Backend Not Restarted
**Problem:** You updated the code but didn't restart the backend.

**Solution:**
```bash
# In backend terminal, press Ctrl+C
# Then restart:
python -m uvicorn app.main:app --reload
```

### Issue 2: Wrong Directory
**Problem:** Running commands from wrong directory.

**Solution:**
```bash
# Make sure you're in backend directory:
pwd  # Should show: .../backend

# If not:
cd backend
```

### Issue 3: Virtual Environment Not Activated
**Problem:** Dependencies not found.

**Solution:**
```bash
# Activate venv:
source venv/bin/activate

# You should see (venv) in your prompt:
(venv) user@computer:~/backend$
```

### Issue 4: Environment Variable Not Set
**Problem:** `USE_REAL_SCRAPERS` not being read.

**Solution:**
```bash
# Check if it's set:
echo $USE_REAL_SCRAPERS

# If empty, set it:
export USE_REAL_SCRAPERS=true

# Or add to .env file
```

### Issue 5: Import Error
**Problem:** New scraper can't be imported.

**Check backend logs for:**
```
WARNING: Could not load LazadaAPIScraper: <error>
```

**Solution:**
```bash
# Check if file exists:
ls -la app/scrapers/lazada_api_scraper.py

# Check for syntax errors:
python3 -m py_compile app/scrapers/lazada_api_scraper.py
```

## Still Not Working?

### Debug Mode

Add this to `backend/app/main.py` at the top:
```python
import os
print(f"🔍 DEBUG: USE_REAL_SCRAPERS = {os.getenv('USE_REAL_SCRAPERS')}")

from app.scrapers.scraper_factory import ScraperFactory
print(f"🔍 DEBUG: USE_REAL_SCRAPERS in factory = {ScraperFactory._load_real_scrapers}")
```

Restart backend and check the output.

### Force Real Scrapers

Edit `backend/app/scrapers/scraper_factory.py`:

Find this line:
```python
USE_REAL_SCRAPERS = os.getenv("USE_REAL_SCRAPERS", "false").lower() == "true"
```

Change to:
```python
USE_REAL_SCRAPERS = True  # FORCE REAL SCRAPERS
```

Save and restart backend.

## Expected Behavior

When working correctly:

1. **Search "iphone 10 xr"**
2. **See:** "11,806 items found for 'iphone 10 xr'"
3. **See:** Real product names and prices
4. **See:** Sort dropdown (Best Match, Price Low to High, Price High to Low)
5. **See:** Pagination (Page 1 of 296)
6. **Click:** "Next" button → loads page 2
7. **Change:** Sort to "Price: Low to High" → results re-sort

## Need More Help?

Share:
1. **Backend startup logs** (first 20 lines)
2. **Backend search logs** (when you search)
3. **Screenshot** of what you see
4. **Output of:** `cat backend/.env | grep USE_REAL_SCRAPERS`
