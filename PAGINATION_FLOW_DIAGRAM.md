# Pagination and Sorting Flow Diagram

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      DashboardPage                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ State:                                                │  │
│  │  - currentPage: number (1)                           │  │
│  │  - sortBy: string ("best_match")                     │  │
│  │  - searchQuery: string ("")                          │  │
│  │  - searchResults: SearchResults | null               │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    SearchBar                          │  │
│  │  Props:                                               │  │
│  │   - page={currentPage}                               │  │
│  │   - sortBy={sortBy}                                  │  │
│  │   - onSearchResults={handleSearchResults}            │  │
│  │   - onNewSearch={handleNewSearch}                    │  │
│  │                                                       │  │
│  │  Internal State:                                      │  │
│  │   - query: string                                    │  │
│  │   - debouncedQuery: string                           │  │
│  │   - lastSearchedQuery: string                        │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Pagination Controls                      │  │
│  │  ┌─────────────┐  ┌──────────┐  ┌─────────────┐     │  │
│  │  │ Sort:       │  │ Previous │  │    Next     │     │  │
│  │  │ [Dropdown]  │  │  Button  │  │   Button    │     │  │
│  │  └─────────────┘  └──────────┘  └─────────────┘     │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Product Grid (40 items)                  │  │
│  │  [Product] [Product] [Product] [Product]             │  │
│  │  [Product] [Product] [Product] [Product]             │  │
│  │  ...                                                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow - User Types New Search Query

```
User types "iphone"
       │
       ▼
┌──────────────────┐
│   SearchBar      │
│  query="iphone"  │
└──────────────────┘
       │
       │ (500ms debounce)
       ▼
┌──────────────────────────┐
│   SearchBar              │
│  debouncedQuery="iphone" │
└──────────────────────────┘
       │
       │ (useEffect detects new query)
       ▼
┌──────────────────────────┐
│   SearchBar              │
│  calls onNewSearch()     │
└──────────────────────────┘
       │
       ▼
┌──────────────────────────┐
│   DashboardPage          │
│  setCurrentPage(1)       │  ← Reset to page 1
└──────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   SearchBar                              │
│  searchProducts("iphone", 40, 1, "best_match") │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   API: GET /api/products/search          │
│   ?q=iphone&page=1&sort_by=best_match    │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   Backend: search_service.py             │
│   search_all_platforms()                 │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   Backend: lazada_scraper_simple.py      │
│   search("iphone", 40, 1, "best_match")  │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   Lazada Website                         │
│   GET /catalog/?q=iphone&page=1          │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   Backend: Parse HTML                    │
│   Extract 40 products                    │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   API Response: SearchResults            │
│   { results: [...40 products...] }       │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   SearchBar                              │
│   calls onSearchResults(results)         │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   DashboardPage                          │
│   setSearchResults(results)              │
│   Display 40 products                    │
└──────────────────────────────────────────┘
```

## Data Flow - User Clicks "Next" Button

```
User clicks "Next" (page 1 → 2)
       │
       ▼
┌──────────────────────────┐
│   DashboardPage          │
│  handlePageChange(2)     │
└──────────────────────────┘
       │
       ▼
┌──────────────────────────┐
│   DashboardPage          │
│  setCurrentPage(2)       │
│  window.scrollTo(top)    │
└──────────────────────────┘
       │
       │ (SearchBar receives new page prop)
       ▼
┌──────────────────────────────────────────┐
│   SearchBar                              │
│  useEffect detects page change           │
│  searchProducts("iphone", 40, 2, "best_match") │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   API: GET /api/products/search          │
│   ?q=iphone&page=2&sort_by=best_match    │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   Lazada Website                         │
│   GET /catalog/?q=iphone&page=2          │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   DashboardPage                          │
│   Display products 41-80                 │
└──────────────────────────────────────────┘
```

## Data Flow - User Changes Sort

```
User selects "Price: Low to High"
       │
       ▼
┌──────────────────────────┐
│   DashboardPage          │
│  handleSortChange()      │
└──────────────────────────┘
       │
       ▼
┌──────────────────────────┐
│   DashboardPage          │
│  setSortBy("price_asc")  │
│  setCurrentPage(1)       │  ← Reset to page 1
└──────────────────────────┘
       │
       │ (SearchBar receives new props)
       ▼
┌──────────────────────────────────────────┐
│   SearchBar                              │
│  useEffect detects sortBy change         │
│  searchProducts("iphone", 40, 1, "price_asc") │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   API: GET /api/products/search          │
│   ?q=iphone&page=1&sort_by=price_asc     │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   Lazada Website                         │
│   GET /catalog/?q=iphone&page=1&sortBy=priceasc │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   DashboardPage                          │
│   Display sorted products (lowest first) │
└──────────────────────────────────────────┘
```

## State Management Summary

### DashboardPage (Parent)
**Owns:**
- `currentPage` - Current page number
- `sortBy` - Current sort option
- `searchQuery` - Current search query
- `searchResults` - Search results from API

**Responsibilities:**
- Manage pagination state
- Manage sort state
- Pass props to SearchBar
- Handle callbacks from SearchBar
- Render pagination controls
- Render product grid

### SearchBar (Child)
**Receives Props:**
- `page` - Page number from parent
- `sortBy` - Sort option from parent
- `onSearchResults` - Callback to send results to parent
- `onNewSearch` - Callback to notify parent of new query

**Owns:**
- `query` - User input (controlled)
- `debouncedQuery` - Debounced query for API calls
- `lastSearchedQuery` - Track query changes
- `isSearching` - Loading state

**Responsibilities:**
- Handle user input
- Debounce search queries
- Detect new queries vs pagination/sort changes
- Call API with correct parameters
- Notify parent of results and new searches

## Key Design Decisions

### 1. Parent Owns Pagination State
**Why:** DashboardPage needs to control pagination because it renders the pagination controls. SearchBar is just the search input, not the full search UI.

### 2. SearchBar Receives Page/Sort as Props
**Why:** Unidirectional data flow. Parent controls state, child receives props and notifies parent of changes.

### 3. Separate onNewSearch Callback
**Why:** Need to distinguish between:
- New search query → reset page to 1
- Pagination/sort change → keep current query, change parameters

### 4. Reset Page on Sort Change
**Why:** When user changes sort, they want to see the first page of sorted results, not page 3 of sorted results.

### 5. Scroll to Top on Page Change
**Why:** Better UX - user sees the new products immediately without having to scroll up manually.

### 6. 500ms Debounce
**Why:** Balance between responsiveness and reducing API calls. User can type "iphone" without triggering 6 API calls.

### 7. AbortController for Race Conditions
**Why:** If user types fast or clicks pagination quickly, previous requests should be cancelled to prevent stale results from appearing.

## URL Parameters (Future Enhancement)

```
Current: http://localhost:5173/dashboard
Future:  http://localhost:5173/dashboard?q=iphone&page=2&sort=price_asc

Benefits:
- Bookmarkable searches
- Shareable links
- Browser back/forward navigation
- Persistent state on refresh
```

## Total Count Display (Future Enhancement)

```
Current: "Search Results (40)"
Future:  "Search Results (41-80 of 11,806)"

Implementation:
1. Parse "11,806 items found" from Lazada HTML
2. Return total_count in API response
3. Calculate: start = (page - 1) * max_results + 1
4. Calculate: end = min(page * max_results, total_count)
5. Display: "Showing {start}-{end} of {total_count} results"
```

## Page Number Buttons (Future Enhancement)

```
Current: [Previous] Page 2 [Next]
Future:  [Previous] 1 2 [3] 4 5 ... 296 [Next]

Logic:
- Show first page (1)
- Show current page and 2 neighbors
- Show last page (total_count / max_results)
- Show ellipsis (...) for gaps
- Highlight current page
```
