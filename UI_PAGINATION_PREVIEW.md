# Pagination & Sorting UI Preview

## What You'll See

### 1. Search Results Header
```
┌─────────────────────────────────────────────────────────────────┐
│  11,806 items found for "iphone 10 xr"    Found in 2.34s       │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Sort & Pagination Controls
```
┌─────────────────────────────────────────────────────────────────┐
│  Sort By: [Best Match ▼]              Page 1 of 296             │
│                                        [◀] 1 2 ... 296 [▶]      │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Sort Dropdown Options
```
┌──────────────────────┐
│ ✓ Best Match         │
│   Price: Low to High │
│   Price: High to Low │
└──────────────────────┘
```

### 4. Pagination States

**Page 1:**
```
[◀] [1] 2 3 ... 296 [▶]
     ^^^
   (active)
```

**Page 5:**
```
[◀] 1 ... 4 [5] 6 ... 296 [▶]
           ^^^
         (active)
```

**Last Page:**
```
[◀] 1 ... 294 295 [296] [▶]
                   ^^^
                (active)
```

### 5. Loading State
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│                    ⟳  Loading...                                │
│                                                                  │
│  [Product cards shown with opacity]                             │
└─────────────────────────────────────────────────────────────────┘
```

### 6. Mobile View
```
┌──────────────────────────────┐
│ Sort By: [Best Match ▼]     │
│                              │
│ Page 1 of 296                │
│ [◀ Previous]  [Next ▶]      │
└──────────────────────────────┘
```

## Complete Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  PriceTracker                                          🔔  👤      │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Track Your Favorite Products                                      │
│  Search products and get notified when prices drop                 │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ 🔍  Search products across Lazada, Shopee...            ✕   │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  11,806 items found for "iphone 10 xr"    Found in 2.34s    │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Sort By: [Best Match ▼]         Page 1 of 296              │ │
│  │                                   [◀] 1 2 3 ... 296 [▶]     │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│  │   Product   │  │   Product   │  │   Product   │               │
│  │    Card     │  │    Card     │  │    Card     │               │
│  │             │  │             │  │             │               │
│  │  ₱1,299     │  │  ₱1,499     │  │  ₱1,599     │               │
│  │  [Track]    │  │  [Track]    │  │  [Track]    │               │
│  └─────────────┘  └─────────────┘  └─────────────┘               │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│  │   Product   │  │   Product   │  │   Product   │               │
│  │    Card     │  │    Card     │  │    Card     │               │
│  └─────────────┘  └─────────────┘  └─────────────┘               │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## Interaction Flow

### Scenario 1: User Changes Sort
```
1. User clicks "Sort By" dropdown
   ┌──────────────────────┐
   │ ✓ Best Match         │
   │   Price: Low to High │ ← User clicks this
   │   Price: High to Low │
   └──────────────────────┘

2. Loading overlay appears
   [⟳ Loading...]

3. Results re-sort, page resets to 1
   Page 1 of 296
   Products now sorted by price (low to high)
```

### Scenario 2: User Navigates Pages
```
1. User on page 1, clicks "Next"
   [◀] [1] 2 3 ... 296 [▶]
                        ↑ clicks here

2. Loading overlay appears
   [⟳ Loading...]

3. Page 2 loads, scroll to top
   [◀] 1 [2] 3 ... 296 [▶]
          ↑ now active
```

### Scenario 3: User Jumps to Page
```
1. User on page 1, clicks page "5"
   [◀] [1] 2 3 ... 296 [▶]
              ↑ clicks "..."

2. Shows: [◀] 1 ... 4 [5] 6 ... 296 [▶]
                      ↑ now active
```

## Color Scheme

```
Active Page:    [1]  ← Blue background (#3B82F6)
Inactive Page:  [2]  ← White background, gray border
Hover:          [3]  ← Light gray background
Disabled:       [◀]  ← Gray, 50% opacity
Loading:        ⟳    ← Blue spinner
```

## Responsive Breakpoints

**Desktop (lg: 1024px+):**
- 3 product cards per row
- Full pagination with page numbers
- Sort dropdown on left, pagination on right

**Tablet (md: 768px+):**
- 2 product cards per row
- Full pagination with page numbers
- Sort and pagination stack vertically

**Mobile (< 768px):**
- 1 product card per row
- Only Previous/Next buttons
- Sort dropdown full width
- Pagination below sort

## Accessibility Features

```
[◀ Previous]  ← aria-label="Previous page"
[1]           ← aria-current="page" (for active)
[▶ Next]      ← aria-label="Next page"
[Sort By ▼]   ← <label for="sort-select">
```

## Animation & Transitions

- **Page change**: Smooth scroll to top (400ms)
- **Loading overlay**: Fade in (200ms)
- **Button hover**: Background color transition (150ms)
- **Spinner**: Continuous rotation animation

## Error States

**No Results:**
```
┌─────────────────────────────────────┐
│         😕                          │
│    No Products Found                │
│                                     │
│  We couldn't find any products      │
│  matching your search.              │
└─────────────────────────────────────┘
```

**Platform Failed:**
```
┌─────────────────────────────────────┐
│  ⚠️  Platform Warning               │
│                                     │
│  Some platforms were unavailable:   │
│  shopee, tiktokshop                 │
└─────────────────────────────────────┘
```

## Summary

The UI provides:
- ✅ Clear total count display
- ✅ Easy-to-use sort dropdown
- ✅ Intuitive pagination controls
- ✅ Loading states for better UX
- ✅ Responsive design for all devices
- ✅ Accessible for screen readers
- ✅ Smooth animations and transitions

Users can now easily browse through thousands of products with a clean, modern interface!
