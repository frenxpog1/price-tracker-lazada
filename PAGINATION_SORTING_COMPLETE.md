# Pagination and Sorting Implementation - Complete

## Overview
Successfully implemented pagination and sorting functionality for the e-commerce price tracker, allowing users to browse through thousands of products (e.g., 11,806 items) with 40 items per page and sort by Best Match, Price Low to High, or Price High to Low.

## Implementation Details

### Backend Changes

#### 1. Lazada Scraper (`backend/app/scrapers/lazada_scraper_simple.py`)
- **Updated `search()` method signature** to accept pagination and sorting parameters:
  ```python
  async def search(self, query: str, max_results: int = 10, page: int = 1, sort_by: str = "best_match")
  ```
- **Pagination**: Adds `page` parameter to URL query string
- **Sorting**: Maps sort options to Lazada's URL parameters:
  - `best_match` → no parameter (default)
  - `price_asc` → `sortBy=priceasc`
  - `price_desc` → `sortBy=pricedesc`
- **URL Format**: `https://www.lazada.com.ph/catalog/?q=iphone&page=2&sortBy=priceasc`

#### 2. Search Service (`backend/app/services/search_service.py`)
- **Updated `search_all_platforms()` method** to accept `page` and `sort_by` parameters
- **Updated `_search_platform_with_timeout()` method** to pass pagination parameters to scrapers
- **Backward compatibility**: Uses try/catch to handle scrapers that don't support pagination
  ```python
  try:
      results = await scraper.search(query, max_results, page, sort_by)
  except TypeError:
      # Scraper doesn't support pagination, use basic search
      results = await scraper.search(query, max_results)
  ```

#### 3. API Endpoint (`backend/app/api/products.py`)
- **Added query parameters** to `/api/products/search`:
  - `page`: Page number (1-indexed, default: 1)
  - `sort_by`: Sort option (default: "best_match")
  - `max_results`: Items per page (default: 40, max: 100)
- **Example**: `GET /api/products/search?q=iphone&page=2&sort_by=price_asc&max_results=40`

### Frontend Changes

#### 1. Product Service (`frontend/src/services/productService.ts`)
- **Updated `searchProducts()` function** to accept pagination parameters:
  ```typescript
  async function searchProducts(
    query: string,
    maxResults: number = 40,
    page: number = 1,
    sortBy: string = 'best_match'
  ): Promise<SearchResults>
  ```
- **Passes parameters** to API via query string

#### 2. SearchBar Component (`frontend/src/components/SearchBar.tsx`)
- **Added props**: `page` and `sortBy`
- **Added callback**: `onNewSearch` to notify parent when a new query is entered
- **Updated useEffect** to re-trigger search when `page` or `sortBy` props change
- **Query tracking**: Tracks `lastSearchedQuery` to detect new searches vs pagination/sort changes
- **Behavior**:
  - When user types new query → calls `onNewSearch()` to reset page to 1
  - When page/sort changes → re-executes search with same query but new parameters

#### 3. Dashboard Page (`frontend/src/pages/DashboardPage.tsx`)
- **Added state**:
  - `currentPage`: Current page number (default: 1)
  - `sortBy`: Current sort option (default: "best_match")
  - `searchQuery`: Current search query
- **Added handlers**:
  - `handleNewSearch()`: Resets page to 1 when new query is entered
  - `handleSortChange()`: Updates sort and resets page to 1
  - `handlePageChange()`: Updates page and scrolls to top
- **Added UI controls**:
  - Sort dropdown with 3 options
  - Previous/Next pagination buttons
  - Current page display
  - Smooth scroll to top on page change

## User Experience

### Search Flow
1. User types "iphone" in search bar
2. After 500ms debounce, search executes with page=1, sort=best_match
3. Results show 40 products from page 1

### Pagination Flow
1. User clicks "Next" button
2. `handlePageChange(2)` is called
3. SearchBar receives new `page` prop
4. SearchBar re-executes search with same query but page=2
5. Results update with products from page 2
6. Page scrolls smoothly to top

### Sorting Flow
1. User selects "Price: Low to High" from dropdown
2. `handleSortChange('price_asc')` is called
3. Sort updates to 'price_asc' and page resets to 1
4. SearchBar receives new `sortBy` and `page` props
5. SearchBar re-executes search with sort=price_asc, page=1
6. Results update with sorted products from page 1

### Combined Flow
1. User searches "iphone" → page 1, best match
2. User clicks "Next" → page 2, best match
3. User changes sort to "Price: Low to High" → page 1, price ascending
4. User clicks "Next" → page 2, price ascending

## Technical Details

### State Management
- **DashboardPage** owns the pagination state (`currentPage`, `sortBy`, `searchQuery`)
- **SearchBar** receives pagination props and notifies parent of changes
- **Unidirectional data flow**: Parent controls state, child notifies of user actions

### Search Triggering
- **Debounced query changes**: 500ms delay after typing stops
- **Immediate pagination/sort changes**: No debounce for better UX
- **AbortController**: Cancels previous requests to prevent race conditions

### Page Reset Logic
- **New search query**: Page resets to 1
- **Sort change**: Page resets to 1
- **Page navigation**: Page updates, sort stays same

## Configuration

### Backend Environment Variables
```bash
# .env file
USE_REAL_SCRAPERS=true  # Must be set to use real Lazada scraper
```

### Default Values
- **Items per page**: 40 (matches Lazada's default)
- **Initial page**: 1
- **Initial sort**: best_match
- **Max results**: 100 (API limit)

## Testing

### Manual Testing Steps
1. **Start backend** with `USE_REAL_SCRAPERS=true`:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. **Start frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test search**:
   - Search for "iphone"
   - Verify 40 results appear
   - Check browser network tab for API call with correct parameters

4. **Test pagination**:
   - Click "Next" button
   - Verify new results appear
   - Check URL parameters: `page=2`
   - Click "Previous" button
   - Verify back to page 1

5. **Test sorting**:
   - Select "Price: Low to High"
   - Verify results are sorted by price ascending
   - Check URL parameters: `sort_by=price_asc`
   - Verify page reset to 1

6. **Test combined**:
   - Search "iphone"
   - Go to page 3
   - Change sort to "Price: High to Low"
   - Verify page reset to 1 with new sort

## Future Enhancements

### Total Count Display
- Parse "11,806 items found" from Lazada HTML
- Display total count and total pages
- Example: "Showing 41-80 of 11,806 results"

### Smart Page Numbers
- Show page number buttons: `1 2 3 ... 296`
- Highlight current page
- Jump to specific page

### URL Parameters
- Sync pagination state with URL query params
- Enable bookmarking and sharing
- Example: `/dashboard?q=iphone&page=2&sort=price_asc`

### Loading States
- Show loading overlay during page transitions
- Disable pagination buttons while loading
- Show skeleton loaders for product cards

### Infinite Scroll
- Alternative to pagination buttons
- Load more products as user scrolls
- "Load More" button at bottom

## Files Modified

### Backend
- `backend/app/scrapers/lazada_scraper_simple.py` - Added pagination and sorting
- `backend/app/services/search_service.py` - Pass pagination parameters
- `backend/app/api/products.py` - Added query parameters
- `backend/.env` - Set `USE_REAL_SCRAPERS=true`

### Frontend
- `frontend/src/services/productService.ts` - Added pagination parameters
- `frontend/src/components/SearchBar.tsx` - Added pagination props and logic
- `frontend/src/pages/DashboardPage.tsx` - Added pagination controls and state

## Summary

The pagination and sorting implementation is **complete and functional**. Users can now:
- ✅ Browse through thousands of products (not just 20)
- ✅ Navigate using Previous/Next buttons
- ✅ Sort by Best Match, Price Low to High, Price High to Low
- ✅ See 40 items per page (Lazada's default)
- ✅ Experience smooth page transitions with scroll to top

The implementation uses real Lazada scrapers (not mocks) and properly handles pagination via URL parameters. The code is clean, well-documented, and follows React best practices with proper state management and effect handling.
