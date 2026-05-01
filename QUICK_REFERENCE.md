# Quick Reference - Pagination and Sorting

## 🚀 Quick Start

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## 🔍 Search Examples

| Search Query | Sort By | Page | Result |
|-------------|---------|------|--------|
| `iphone` | Best Match | 1 | Products 1-40, relevance sorted |
| `iphone` | Best Match | 2 | Products 41-80, relevance sorted |
| `iphone` | Price: Low to High | 1 | Products 1-40, cheapest first |
| `iphone` | Price: High to Low | 1 | Products 1-40, most expensive first |
| `laptop` | Price: Low to High | 3 | Products 81-120, cheapest first |

## 📡 API Endpoints

### Search Products
```
GET /api/products/search
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | required | Search query |
| `page` | integer | 1 | Page number (1-indexed) |
| `sort_by` | string | "best_match" | Sort option |
| `max_results` | integer | 40 | Items per page (1-100) |

**Sort Options:**
- `best_match` - Relevance-based sorting (default)
- `price_asc` - Price low to high
- `price_desc` - Price high to low

**Example Requests:**
```bash
# Page 1, best match
GET /api/products/search?q=iphone&page=1&sort_by=best_match&max_results=40

# Page 2, price low to high
GET /api/products/search?q=iphone&page=2&sort_by=price_asc&max_results=40

# Page 3, price high to low
GET /api/products/search?q=laptop&page=3&sort_by=price_desc&max_results=40
```

## 🎨 UI Components

### Pagination Controls
```
┌─────────────────────────────────────────────┐
│  Sort: [Best Match ▼]                       │
│  [← Previous] Page 2 [Next →]               │
└─────────────────────────────────────────────┘
```

### Sort Options
- **Best Match** - Default relevance sorting
- **Price: Low to High** - Cheapest products first
- **Price: High to Low** - Most expensive products first

### Button States
- **Previous**: Disabled on page 1, enabled on page 2+
- **Next**: Always enabled (no total page count yet)

## 🔄 User Flows

### Flow 1: Basic Search
```
User types "iphone"
  → Wait 500ms (debounce)
  → Search with page=1, sort=best_match
  → Display 40 products
```

### Flow 2: Navigate to Next Page
```
User clicks "Next"
  → page changes from 1 to 2
  → Search with page=2, same sort
  → Display products 41-80
  → Scroll to top
```

### Flow 3: Change Sort
```
User selects "Price: Low to High"
  → sort changes to price_asc
  → page resets to 1
  → Search with page=1, sort=price_asc
  → Display sorted products 1-40
```

### Flow 4: New Search Query
```
User types "laptop" (new query)
  → page resets to 1
  → sort stays same
  → Search with page=1, current sort
  → Display new results
```

## 📁 File Locations

### Backend
```
backend/
├── app/
│   ├── api/
│   │   └── products.py          # API endpoint with pagination
│   ├── services/
│   │   └── search_service.py    # Search service with pagination
│   └── scrapers/
│       └── lazada_scraper_simple.py  # Scraper with pagination
└── .env                         # USE_REAL_SCRAPERS=true
```

### Frontend
```
frontend/
└── src/
    ├── services/
    │   └── productService.ts    # API client with pagination
    ├── components/
    │   └── SearchBar.tsx        # Search bar with pagination props
    └── pages/
        └── DashboardPage.tsx    # Dashboard with pagination controls
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Only 20 results | Restart frontend and backend |
| Mock data appearing | Set `USE_REAL_SCRAPERS=true` in `.env` |
| Pagination not working | Check browser console for errors |
| Sort not working | Check Network tab for `sort_by` parameter |
| Slow search | Normal for web scraping (5-10 seconds) |

## 🔧 Configuration

### Backend Environment Variables
```bash
# backend/.env
USE_REAL_SCRAPERS=true  # Use real Lazada scraper
DEBUG=True              # Enable debug mode
DATABASE_URL=postgresql://localhost/pricetracker
```

### Frontend Environment Variables
```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 📊 Default Values

| Setting | Value | Description |
|---------|-------|-------------|
| Items per page | 40 | Matches Lazada's default |
| Initial page | 1 | First page |
| Initial sort | best_match | Relevance sorting |
| Debounce delay | 500ms | Wait time after typing |
| Max results | 100 | API limit |

## 🎯 Key Features

- ✅ **Pagination**: Browse thousands of products
- ✅ **Sorting**: Best Match, Price Low to High, Price High to Low
- ✅ **40 items per page**: Matches Lazada's default
- ✅ **Real scraper**: Uses actual Lazada website
- ✅ **Smooth UX**: Scroll to top, loading states
- ✅ **Smart reset**: Page resets on sort/query change

## 📚 Documentation

| Document | Description |
|----------|-------------|
| `IMPLEMENTATION_COMPLETE_SUMMARY.md` | User-friendly overview |
| `PAGINATION_SORTING_COMPLETE.md` | Full technical details |
| `TESTING_GUIDE.md` | Step-by-step testing |
| `PAGINATION_FLOW_DIAGRAM.md` | Visual flow diagrams |
| `UI_PAGINATION_CONTROLS.md` | UI preview and styling |
| `IMPLEMENTATION_CHECKLIST.md` | Complete checklist |
| `QUICK_REFERENCE.md` | This document |

## 💡 Tips

1. **Search Tips**
   - Use specific keywords for better results
   - Try different sort options to find best deals
   - Navigate through pages to see more products

2. **Performance Tips**
   - First search may be slow (web scraping)
   - Subsequent searches are faster (same session)
   - Use specific queries to reduce results

3. **Development Tips**
   - Check browser console for errors
   - Check Network tab for API calls
   - Check backend logs for scraper activity

## 🚦 Status Indicators

### Backend Running
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Frontend Running
```
VITE v4.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

### Successful Search
```
INFO:     Searching Lazada for: iphone (page=1, sort=best_match)
INFO:     Found 40 product cards
INFO:     Successfully parsed 40 products from Lazada
```

## 🎉 Success Criteria

Implementation is successful if:
- ✅ Real Lazada products appear (not mock data)
- ✅ 40 products per page
- ✅ Previous/Next buttons work
- ✅ Sort dropdown works
- ✅ Page resets on sort change
- ✅ Page resets on new search
- ✅ Smooth scroll to top
- ✅ No errors in console

## 📞 Support

If you encounter issues:
1. Check `TROUBLESHOOTING.md` (if exists)
2. Check `TESTING_GUIDE.md` for test scenarios
3. Check browser console for errors
4. Check backend logs for errors
5. Verify environment variables
6. Restart both frontend and backend

## 🔮 Future Enhancements

- ⬜ Total count display ("Showing 41-80 of 11,806")
- ⬜ Page number buttons (1, 2, 3, ..., 296)
- ⬜ URL parameter sync
- ⬜ Loading overlays
- ⬜ Items per page selector
- ⬜ Infinite scroll
- ⬜ Jump to page input

---

**Status**: ✅ COMPLETE AND READY TO USE

**Last Updated**: Implementation complete with all core features working.
