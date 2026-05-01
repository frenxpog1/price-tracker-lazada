# Frontend Pagination & Sorting Implementation

## Overview
Added pagination and sorting controls to the frontend dashboard to handle large search results from Lazada and other platforms.

## What Was Implemented

### 1. Updated Types (`frontend/src/types/product.ts`)
Added:
```typescript
interface PaginationInfo {
  current_page: number
  total_pages: number
  items_per_page: number
  total_count: number
}

interface SearchResults {
  // ... existing fields
  pagination?: PaginationInfo | null
  sort_by?: string | null
}
```

### 2. Updated Product Service (`frontend/src/services/productService.ts`)
Updated `searchProducts` function signature:
```typescript
searchProducts(
  query: string,
  maxResults: number = 40,
  page: number = 1,
  sortBy: string = 'best_match'
): Promise<SearchResults>
```

### 3. Updated Dashboard Page (`frontend/src/pages/DashboardPage.tsx`)

#### New State Variables:
- `currentPage`: Current page number
- `sortBy`: Current sort option
- `isLoadingPage`: Loading state for page changes
- `lastSearchQuery`: Last search query for pagination

#### New Functions:
- `handlePageChange(newPage)`: Navigate to a different page
- `handleSortChange(newSortBy)`: Change sort option

#### New UI Components:

**1. Total Count Display:**
```
"11,806 items found for 'iphone 10 xr'"
```

**2. Sort Dropdown:**
- Best Match
- Price: Low to High
- Price: High to Low

**3. Pagination Controls:**
- Previous/Next buttons
- Page numbers with ellipsis
- Current page highlighted
- "Page X of Y" indicator

## UI Features

### Sort Dropdown
- Located above search results
- Disabled while loading
- Resets to page 1 when changed
- Smooth transition with loading overlay

### Pagination
- Shows current page and total pages
- Previous/Next navigation buttons
- Smart page number display:
  - Shows current page
  - Shows adjacent pages
  - Shows first and last page
  - Uses ellipsis (...) for gaps
- Disabled buttons when at boundaries
- Scrolls to top on page change

### Loading States
- Loading overlay during page/sort changes
- Disabled controls while loading
- Spinner with "Loading..." text

### Responsive Design
- Mobile: Shows only prev/next buttons
- Desktop: Shows full pagination with page numbers
- Flexbox layout adapts to screen size

## User Flow

1. **User searches** for "iphone 10 xr"
2. **Results show**: "11,806 items found for 'iphone 10 xr'"
3. **User can**:
   - Change sort order (Best Match → Price Low to High)
   - Navigate pages (Page 1 → Page 2)
   - See total pages (Page 1 of 296)

4. **On page change**:
   - Loading overlay appears
   - New results load
   - Page scrolls to top
   - URL could be updated (future enhancement)

5. **On sort change**:
   - Resets to page 1
   - Loading overlay appears
   - Results re-sort
   - Maintains search query

## Code Example

### Using the Updated API:
```typescript
// Search with pagination and sorting
const results = await searchProducts(
  'iphone 10 xr',  // query
  40,              // max results per page
  2,               // page number
  'price_asc'      // sort by price low to high
)

// Access pagination info
if (results.pagination) {
  console.log(`Page ${results.pagination.current_page} of ${results.pagination.total_pages}`)
  console.log(`Total items: ${results.pagination.total_count}`)
}
```

### Pagination Component Structure:
```tsx
<div className="pagination-controls">
  {/* Sort Dropdown */}
  <select value={sortBy} onChange={handleSortChange}>
    <option value="best_match">Best Match</option>
    <option value="price_asc">Price: Low to High</option>
    <option value="price_desc">Price: High to Low</option>
  </select>

  {/* Pagination */}
  <div className="page-controls">
    <button onClick={() => handlePageChange(page - 1)}>Previous</button>
    <span>Page {page} of {totalPages}</span>
    <button onClick={() => handlePageChange(page + 1)}>Next</button>
  </div>
</div>
```

## Testing

### Manual Testing Steps:

1. **Start the application**:
   ```bash
   # Backend (with real scrapers)
   cd backend
   export USE_REAL_SCRAPERS=true
   python -m uvicorn app.main:app --reload

   # Frontend
   cd frontend
   npm run dev
   ```

2. **Test Search**:
   - Search for "iphone 10 xr"
   - Verify total count shows (e.g., "11,806 items found")

3. **Test Sorting**:
   - Change sort to "Price: Low to High"
   - Verify results re-sort
   - Verify page resets to 1

4. **Test Pagination**:
   - Click "Next" button
   - Verify page 2 loads
   - Verify URL shows page 2 results
   - Click page number (e.g., "5")
   - Verify page 5 loads

5. **Test Edge Cases**:
   - Try to go before page 1 (button should be disabled)
   - Try to go past last page (button should be disabled)
   - Change sort while on page 5 (should reset to page 1)

## Styling

### Tailwind Classes Used:
- `rounded-xl`: Rounded corners for modern look
- `border-neutral-300`: Subtle borders
- `bg-primary-500`: Primary color for active page
- `hover:bg-neutral-50`: Hover effects
- `disabled:opacity-50`: Disabled state styling
- `transition-fast`: Smooth transitions

### Color Scheme:
- Primary: Blue (#3B82F6)
- Neutral: Gray scale
- White backgrounds with subtle borders

## Future Enhancements

1. **URL Parameters**: Update URL with page and sort params
2. **Infinite Scroll**: Option for infinite scroll instead of pagination
3. **Items Per Page**: Allow user to choose items per page (20, 40, 60)
4. **Jump to Page**: Input field to jump to specific page
5. **Keyboard Navigation**: Arrow keys for prev/next
6. **Loading Skeleton**: Show skeleton cards while loading
7. **Persist State**: Remember page/sort in localStorage
8. **Analytics**: Track which sort options are most popular

## Accessibility

- ✅ ARIA labels on buttons
- ✅ Disabled state for buttons
- ✅ Keyboard navigation support
- ✅ Focus indicators
- ✅ Screen reader friendly
- ✅ Semantic HTML

## Performance

- Debounced search (500ms)
- Abort previous requests
- Smooth scrolling
- Optimized re-renders with useCallback
- Loading states prevent double-clicks

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

## Files Modified

1. `frontend/src/types/product.ts` - Added PaginationInfo type
2. `frontend/src/services/productService.ts` - Updated searchProducts function
3. `frontend/src/pages/DashboardPage.tsx` - Added pagination and sorting UI

## Summary

The frontend now fully supports:
- ✅ Pagination (navigate through thousands of results)
- ✅ Sorting (Best Match, Price Low to High, Price High to Low)
- ✅ Total count display (e.g., "11,806 items found")
- ✅ Loading states
- ✅ Responsive design
- ✅ Smooth UX with transitions

Users can now browse through all 11,806 items instead of just seeing 20!
