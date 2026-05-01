# Pagination and Sorting Implementation

## Overview
Implemented pagination and sorting features for the Lazada scraper to handle large search results (e.g., 11,806 items instead of just 20).

## What Was Implemented

### 1. New Lazada API Scraper (`backend/app/scrapers/lazada_api_scraper.py`)
- **Pagination Support**: Fetch results page by page (40 items per page, Lazada's default)
- **Sorting Options**:
  - `best_match`: Default sorting (Best Match)
  - `price_asc`: Price Low to High
  - `price_desc`: Price High to Low
- **Total Count Extraction**: Extracts the total number of items found (e.g., "11806 items found")
- **Returns**: Dict with products, pagination info, and total count

### 2. Updated API Endpoint (`backend/app/api/products.py`)
New query parameters:
- `page`: Page number (default: 1)
- `sort_by`: Sort option (default: "best_match")
- `max_results`: Items per page (default: 40, max: 100)

Example API call:
```
GET /api/products/search?q=iphone+10+xr&page=2&sort_by=price_asc&max_results=40
```

### 3. Updated Schemas (`backend/app/schemas/product.py`)
Added:
- `PaginationInfo`: Contains current_page, total_pages, items_per_page, total_count
- Updated `SearchResults` to include pagination and sort_by fields

### 4. Updated Search Service (`backend/app/services/search_service.py`)
- Supports pagination and sorting parameters
- Backward compatible with old scrapers
- Automatically detects if scraper supports pagination

### 5. Updated Scraper Factory (`backend/app/scrapers/scraper_factory.py`)
- Prioritizes the new `LazadaAPIScraper` when loading real scrapers
- Falls back to older scrapers if API scraper fails

## How It Works

### URL Parameters
Lazada uses these URL parameters:
- `q`: Search query
- `page`: Page number (1-indexed)
- `sortBy`: Sort option
  - Empty or omitted = Best Match
  - `priceasc` = Price Low to High
  - `pricedesc` = Price High to Low

### Total Count Extraction
The scraper looks for HTML like:
```html
<span>11806 items found for "iphone 10 xr"</span>
```

And extracts the number using regex: `(\d+)\s+items?\s+found`

### Pagination Calculation
```python
items_per_page = 40  # Lazada default
total_pages = (total_count + items_per_page - 1) // items_per_page
```

## API Response Example

```json
{
  "query": "iphone 10 xr",
  "results": [...],
  "total_results": 40,
  "platforms_searched": ["lazada"],
  "platforms_failed": [],
  "search_time_seconds": 2.34,
  "pagination": {
    "current_page": 1,
    "total_pages": 296,
    "items_per_page": 40,
    "total_count": 11806
  },
  "sort_by": "best_match"
}
```

## Frontend Integration (Next Steps)

### 1. Update Search Component
Add pagination controls:
```tsx
<div className="pagination">
  <button onClick={() => setPage(page - 1)} disabled={page === 1}>
    Previous
  </button>
  <span>Page {page} of {totalPages}</span>
  <button onClick={() => setPage(page + 1)} disabled={page === totalPages}>
    Next
  </button>
</div>
```

### 2. Add Sort Dropdown
```tsx
<select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
  <option value="best_match">Best Match</option>
  <option value="price_asc">Price: Low to High</option>
  <option value="price_desc">Price: High to Low</option>
</select>
```

### 3. Update API Call
```typescript
const searchProducts = async (query: string, page: number, sortBy: string) => {
  const response = await api.get('/products/search', {
    params: { q: query, page, sort_by: sortBy, max_results: 40 }
  });
  return response.data;
};
```

### 4. Display Total Count
```tsx
<div className="search-info">
  {pagination?.total_count} items found for "{query}"
</div>
```

## Testing

### Enable Real Scrapers
Set environment variable:
```bash
export USE_REAL_SCRAPERS=true
```

### Test API Endpoints
```bash
# Page 1, Best Match
curl "http://localhost:8000/api/products/search?q=iphone+10+xr&page=1&sort_by=best_match"

# Page 2, Price Low to High
curl "http://localhost:8000/api/products/search?q=iphone+10+xr&page=2&sort_by=price_asc"

# Page 1, Price High to Low
curl "http://localhost:8000/api/products/search?q=iphone+10+xr&page=1&sort_by=price_desc"
```

## Limitations & Notes

1. **Lazada's Anti-Bot Protection**: May block requests if too many are made quickly
2. **Dynamic Content**: Some content is loaded via JavaScript, may need Playwright for full support
3. **Rate Limiting**: Consider adding delays between requests
4. **Total Count Accuracy**: The total count shown by Lazada may not always be exact

## Future Improvements

1. **Caching**: Cache search results to reduce scraping load
2. **Rate Limiting**: Implement request throttling
3. **Playwright Integration**: Use browser automation for better reliability
4. **Shopee & TikTok Shop**: Implement pagination for other platforms
5. **Filters**: Add category, price range, and rating filters

## What You Can Do Now

1. **Test the Backend**: Start the backend with `USE_REAL_SCRAPERS=true` and test the API
2. **Update Frontend**: Add pagination controls and sort dropdown to the search page
3. **Provide Feedback**: Let me know if you need adjustments to the implementation
4. **Share URLs**: If you have specific Lazada URLs for different pages/sorts, share them for better accuracy
