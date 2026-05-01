# Testing Guide - Pagination and Sorting

## Quick Start

### 1. Start the Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

**Important**: Verify `USE_REAL_SCRAPERS=true` is set in `backend/.env`

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```

### 3. Open Browser
Navigate to: http://localhost:5173 (or the URL shown in terminal)

## Test Scenarios

### Test 1: Basic Search
**Steps:**
1. Type "iphone" in the search bar
2. Wait for results to load (500ms debounce)

**Expected:**
- ✅ 40 products appear
- ✅ Search bar shows loading spinner while searching
- ✅ Results show products from Lazada (real scraper)
- ✅ Each product card shows name, price, image

**Check Network Tab:**
- Request: `GET /api/products/search?q=iphone&max_results=40&page=1&sort_by=best_match`
- Status: 200 OK
- Response: JSON with `results` array

### Test 2: Pagination - Next Page
**Steps:**
1. Search for "iphone"
2. Scroll down to pagination controls
3. Click "Next →" button

**Expected:**
- ✅ Page number changes from "Page 1" to "Page 2"
- ✅ New set of 40 products appears
- ✅ Page scrolls smoothly to top
- ✅ "Previous ←" button becomes enabled

**Check Network Tab:**
- Request: `GET /api/products/search?q=iphone&max_results=40&page=2&sort_by=best_match`
- Status: 200 OK

### Test 3: Pagination - Previous Page
**Steps:**
1. From page 2, click "Previous ←" button

**Expected:**
- ✅ Page number changes from "Page 2" to "Page 1"
- ✅ Original products from page 1 appear
- ✅ Page scrolls smoothly to top
- ✅ "Previous ←" button becomes disabled

### Test 4: Sorting - Price Low to High
**Steps:**
1. Search for "iphone"
2. Click the "Sort:" dropdown
3. Select "Price: Low to High"

**Expected:**
- ✅ Page resets to "Page 1"
- ✅ Products are sorted by price (lowest first)
- ✅ First product has lower price than last product
- ✅ Loading spinner appears briefly

**Check Network Tab:**
- Request: `GET /api/products/search?q=iphone&max_results=40&page=1&sort_by=price_asc`
- Status: 200 OK

### Test 5: Sorting - Price High to Low
**Steps:**
1. From "Price: Low to High", select "Price: High to Low"

**Expected:**
- ✅ Page stays at "Page 1"
- ✅ Products are sorted by price (highest first)
- ✅ First product has higher price than last product

**Check Network Tab:**
- Request: `GET /api/products/search?q=iphone&max_results=40&page=1&sort_by=price_desc`
- Status: 200 OK

### Test 6: Sorting - Best Match
**Steps:**
1. From "Price: High to Low", select "Best Match"

**Expected:**
- ✅ Page stays at "Page 1"
- ✅ Products return to default relevance sorting

**Check Network Tab:**
- Request: `GET /api/products/search?q=iphone&max_results=40&page=1&sort_by=best_match`
- Status: 200 OK

### Test 7: Combined - Pagination + Sorting
**Steps:**
1. Search for "iphone"
2. Click "Next" to go to page 2
3. Click "Next" again to go to page 3
4. Change sort to "Price: Low to High"

**Expected:**
- ✅ Page resets to "Page 1" (not page 3)
- ✅ Products are sorted by price
- ✅ Can navigate to page 2, 3, etc. with new sort

### Test 8: New Search Resets Pagination
**Steps:**
1. Search for "iphone"
2. Go to page 3
3. Change sort to "Price: Low to High"
4. Go to page 2
5. Search for "laptop" (new query)

**Expected:**
- ✅ Page resets to "Page 1"
- ✅ Sort stays as "Price: Low to High"
- ✅ New results for "laptop" appear

### Test 9: Empty Search
**Steps:**
1. Clear the search bar (delete all text)

**Expected:**
- ✅ Results disappear
- ✅ Pagination controls disappear
- ✅ "Your Tracked Products" section remains visible

### Test 10: Error Handling
**Steps:**
1. Stop the backend server
2. Search for "iphone"

**Expected:**
- ✅ Error message appears: "Network error. Please check your connection."
- ✅ No results shown
- ✅ Search bar is still functional

## Browser Console Checks

### No Errors
Open browser console (F12) and check for:
- ❌ No red error messages
- ❌ No React warnings
- ✅ Only info logs (if any)

### Network Requests
Check Network tab (F12 → Network):
- ✅ All requests to `/api/products/search` return 200 OK
- ✅ Request parameters match expected values
- ✅ Response contains `results` array with products

## Backend Logs

### Expected Log Messages
```
INFO:     Searching Lazada for: iphone (page=1, sort=best_match)
INFO:     Found 40 product cards
INFO:     Successfully parsed 40 products from Lazada
INFO:     User <user_id> searching for: iphone (page=1, sort=best_match)
```

### No Error Messages
- ❌ No "Mock scraper" messages (means real scraper is being used)
- ❌ No "HTTP 403" errors
- ❌ No "Failed to parse product card" errors

## Common Issues

### Issue: Only seeing mock data
**Symptom**: Products have generic names like "Mock Product 1"
**Solution**: 
1. Check `backend/.env` has `USE_REAL_SCRAPERS=true`
2. Restart backend server
3. Clear browser cache

### Issue: Pagination not working
**Symptom**: Clicking "Next" doesn't change results
**Solution**:
1. Check browser console for errors
2. Check Network tab for API calls
3. Verify `page` parameter is changing in URL

### Issue: Sorting not working
**Symptom**: Changing sort doesn't change order
**Solution**:
1. Check Network tab for `sort_by` parameter
2. Verify backend logs show correct sort parameter
3. Check if Lazada is returning sorted results

### Issue: Search is slow
**Symptom**: Takes >5 seconds to load results
**Solution**:
1. This is normal for real web scraping
2. Lazada's website may be slow
3. Check internet connection

## Success Criteria

All tests pass if:
- ✅ Real Lazada products appear (not mock data)
- ✅ Pagination works (Previous/Next buttons)
- ✅ Sorting works (Best Match, Price Low to High, Price High to Low)
- ✅ Page resets to 1 when sort changes
- ✅ Page resets to 1 when new search query entered
- ✅ No TypeScript errors
- ✅ No React warnings
- ✅ No network errors
- ✅ Smooth user experience

## Next Steps

If all tests pass:
1. ✅ Implementation is complete and working
2. Consider adding total count display
3. Consider adding page number buttons (1, 2, 3, ...)
4. Consider adding URL parameter sync
5. Consider adding loading overlays

If tests fail:
1. Check browser console for errors
2. Check backend logs for errors
3. Verify environment variables
4. Restart both frontend and backend
5. Clear browser cache and cookies
