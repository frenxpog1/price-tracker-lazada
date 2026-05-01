# How to Test the RapidAPI Implementation

## Quick Test (Recommended)

Run this single command to install dependencies and test all scrapers:

```bash
cd rapidapi_version
./install_and_test.sh
```

This will:
1. Install all required Python packages
2. Test each scraper individually (Lazada, Shopee, Temu)
3. Show you real results from each platform
4. Tell you if everything is working

**Expected time**: 2-3 minutes total

---

## Manual Testing (Step by Step)

If you prefer to do it manually:

### Step 1: Install Dependencies

```bash
cd rapidapi_version
pip3 install -r requirements.txt
```

**What this installs:**
- FastAPI (web framework)
- Selenium (browser automation)
- Pydantic (data validation)
- Other utilities

### Step 2: Verify Scrapers Work

```bash
python3 verify_scrapers.py
```

**What this does:**
- Tests if all Python modules can be imported
- Tests Lazada scraper with a real search
- Tests Shopee scraper with a real search
- Tests Temu scraper with a real search
- Shows you sample results from each platform

**Expected output:**
```
✅ All imports successful!
✅ Lazada scraper is WORKING!
✅ Shopee scraper is WORKING!
✅ Temu scraper is WORKING!
🎉 SUCCESS! All scrapers are working correctly!
```

### Step 3: Start the API Server

```bash
python3 run_api.py
```

**What this does:**
- Starts the FastAPI server on http://localhost:8000
- Enables the interactive documentation at http://localhost:8000/docs
- Makes the API ready to receive requests

### Step 4: Test the Full API

Open a new terminal and run:

```bash
cd rapidapi_version
python3 test_api.py
```

**What this does:**
- Tests all API endpoints
- Tests health check
- Tests platform listing
- Tests search functionality
- Tests each platform individually

---

## Quick Browser Test

Once the API is running (Step 3), open your browser:

1. **API Documentation**: http://localhost:8000/docs
   - Interactive interface to test all endpoints
   - Try the `/search` endpoint with query "phone"

2. **Health Check**: http://localhost:8000/health
   - Should return: `{"status": "healthy", "timestamp": ...}`

3. **Platform List**: http://localhost:8000/platforms
   - Shows all supported platforms and their status

4. **Search Test**: http://localhost:8000/search?q=phone&per_page=3
   - Should return real products from all platforms

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
pip3 install -r requirements.txt
```

### "Chrome driver not found" or browser errors

**Solution:**
The first run will automatically download ChromeDriver. Just wait a bit longer.

### Scraper returns no results

**Possible causes:**
1. Internet connection issue
2. Platform website changed their HTML structure
3. Platform is blocking automated requests

**Check:**
```bash
# Test your internet
curl -I https://www.lazada.com.ph

# Try running the verification again
python3 verify_scrapers.py
```

### API is slow

**This is normal!** Each scraper:
- Launches a headless Chrome browser
- Loads the e-commerce website
- Waits for JavaScript to render
- Extracts product data

**Expected times:**
- Lazada: 5-10 seconds
- Shopee: 10-15 seconds
- Temu: 10-15 seconds
- All three together: 25-40 seconds

---

## What Success Looks Like

### ✅ Verification Script Success:
```
🧪 RapidAPI Scraper Verification Suite
========================================

STEP 1: Testing Imports
✅ All imports successful!

STEP 2: Testing Lazada Scraper
✅ Browser started successfully
⏱️  Search completed in 8.45 seconds
📊 Total results found: 3271
📦 Products returned: 3
✅ Lazada scraper is WORKING!

STEP 3: Testing Shopee Scraper
✅ Browser started successfully
⏱️  Search completed in 12.34 seconds
📊 Total results found: 2450
📦 Products returned: 3
✅ Shopee scraper is WORKING!

STEP 4: Testing Temu Scraper
✅ Browser started successfully
⏱️  Search completed in 11.23 seconds
📊 Total results found: 1890
📦 Products returned: 3
✅ Temu scraper is WORKING!

FINAL RESULTS
========================================
✅ Lazada: WORKING
✅ Shopee: WORKING
✅ Temu: WORKING

📊 Score: 3/3 scrapers working
🎉 SUCCESS! All scrapers are working correctly!
```

### ✅ API Test Success:
```
🧪 E-commerce Scraper API Test Suite
========================================

📋 Running: Health Check
✅ Health check passed

📋 Running: Platforms Endpoint
✅ Platforms endpoint works: ['lazada', 'shopee', 'temu']

📋 Running: Search Endpoint
✅ Search successful!
   Query: phone
   Total results: 7611
   Results returned: 15
   Platforms searched: ['lazada', 'shopee', 'temu']

📊 Test Results: 6/6 tests passed
🎉 All tests passed! API is working correctly!
```

---

## Ready for RapidAPI?

If you see the success messages above, your API is **100% ready** to deploy to RapidAPI!

**Next steps:**
1. Deploy to a hosting platform (Heroku, AWS, DigitalOcean, etc.)
2. Get your public API URL
3. Create a RapidAPI listing
4. Configure pricing and rate limits
5. Launch! 🚀
