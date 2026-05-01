# Pagination Controls UI Preview

## Visual Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                         Search Bar                              │
│  🔍 Search products across Lazada, Shopee, TikTok Shop...      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Search Results (40)                    Found in 2.34s          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Sort: [Best Match ▼]          [← Previous] Page 2 [Next →]    │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Product    │ │   Product    │ │   Product    │ │   Product    │
│   Card 41    │ │   Card 42    │ │   Card 43    │ │   Card 44    │
│              │ │              │ │              │ │              │
│  ₱12,999     │ │  ₱13,499     │ │  ₱13,999     │ │  ₱14,499     │
│  [Track]     │ │  [Track]     │ │  [Track]     │ │  [Track]     │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Product    │ │   Product    │ │   Product    │ │   Product    │
│   Card 45    │ │   Card 46    │ │   Card 47    │ │   Card 48    │
│              │ │              │ │              │ │              │
│  ₱14,999     │ │  ₱15,499     │ │  ₱15,999     │ │  ₱16,499     │
│  [Track]     │ │  [Track]     │ │  [Track]     │ │  [Track]     │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

... (32 more products)
```

## Sort Dropdown Options

```
┌─────────────────────────┐
│ Sort: [Best Match ▼]    │
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ ✓ Best Match            │
│   Price: Low to High    │
│   Price: High to Low    │
└─────────────────────────┘
```

## Pagination States

### Page 1 (Previous Disabled)
```
┌─────────────────────────────────────────────┐
│  [← Previous] Page 1 [Next →]               │
│   (disabled)           (enabled)            │
└─────────────────────────────────────────────┘
```

### Page 2 (Both Enabled)
```
┌─────────────────────────────────────────────┐
│  [← Previous] Page 2 [Next →]               │
│   (enabled)            (enabled)            │
└─────────────────────────────────────────────┘
```

### Page 296 (Next Disabled - if we knew total pages)
```
┌─────────────────────────────────────────────┐
│  [← Previous] Page 296 [Next →]             │
│   (enabled)            (disabled)           │
└─────────────────────────────────────────────┘
```

## User Interactions

### 1. Clicking Sort Dropdown
```
Before:
┌─────────────────────────┐
│ Sort: [Best Match ▼]    │
└─────────────────────────┘

After Click:
┌─────────────────────────┐
│ Sort: [Best Match ▼]    │
├─────────────────────────┤
│ ✓ Best Match            │ ← Currently selected
│   Price: Low to High    │
│   Price: High to Low    │
└─────────────────────────┘
```

### 2. Selecting "Price: Low to High"
```
Before:
Page 3, Best Match

After:
Page 1, Price: Low to High  ← Page reset to 1
Products sorted by price (lowest first)
```

### 3. Clicking "Next" Button
```
Before:
Page 1, showing products 1-40

After:
Page 2, showing products 41-80
Smooth scroll to top
```

### 4. Clicking "Previous" Button
```
Before:
Page 2, showing products 41-80

After:
Page 1, showing products 1-40
Smooth scroll to top
```

## Loading States

### While Searching
```
┌─────────────────────────────────────────────────────────────────┐
│  🔍 Search products...                    ⏳ Searching...       │
└─────────────────────────────────────────────────────────────────┘
```

### While Changing Page
```
┌─────────────────────────────────────────────┐
│  [← Previous] Page 2 [Next →]               │
│                                             │
│  Loading...                                 │
└─────────────────────────────────────────────┘
```

## Responsive Design

### Desktop (3 columns)
```
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Product  │ │ Product  │ │ Product  │
└──────────┘ └──────────┘ └──────────┘
```

### Tablet (2 columns)
```
┌──────────┐ ┌──────────┐
│ Product  │ │ Product  │
└──────────┘ └──────────┘
```

### Mobile (1 column)
```
┌──────────┐
│ Product  │
└──────────┘
┌──────────┐
│ Product  │
└──────────┘
```

## Color Scheme

### Pagination Controls
- **Background**: White (`bg-white`)
- **Border**: Light gray (`border-neutral-200`)
- **Text**: Dark gray (`text-neutral-700`)
- **Hover**: Light gray background (`hover:bg-neutral-50`)
- **Disabled**: 50% opacity (`disabled:opacity-50`)

### Sort Dropdown
- **Background**: White
- **Border**: Medium gray (`border-neutral-300`)
- **Text**: Dark gray (`text-neutral-700`)
- **Focus**: Primary color ring (`focus:ring-primary-500`)

### Buttons
- **Normal**: White background, gray border
- **Hover**: Light gray background
- **Disabled**: Grayed out, cursor not allowed
- **Active**: Slightly darker background

## Accessibility

### Keyboard Navigation
- **Tab**: Navigate between sort dropdown and pagination buttons
- **Enter/Space**: Activate buttons
- **Arrow keys**: Navigate dropdown options

### Screen Reader Support
- Sort dropdown has label: "Sort:"
- Buttons have descriptive text: "Previous", "Next"
- Current page announced: "Page 2"
- Disabled state announced: "Previous button disabled"

### Focus Indicators
- Visible focus ring on all interactive elements
- High contrast for better visibility
- Smooth transitions for better UX

## Animation

### Smooth Scroll
```javascript
window.scrollTo({ top: 0, behavior: 'smooth' })
```
- Smooth scroll to top when page changes
- Duration: ~500ms
- Easing: Browser default

### Loading Spinner
```
⏳ Searching...
```
- Rotating spinner icon
- Animation: `animate-spin`
- Duration: 1s per rotation

### Hover Effects
```css
transition-fast  /* 150ms ease-in-out */
```
- Button background color change
- Dropdown highlight
- Product card elevation

## Future Enhancements

### Page Number Buttons
```
┌─────────────────────────────────────────────────────────────────┐
│  [← Previous] [1] [2] [3] ... [296] [Next →]                   │
│                     ^^^                                         │
│                  Current page highlighted                       │
└─────────────────────────────────────────────────────────────────┘
```

### Total Count Display
```
┌─────────────────────────────────────────────────────────────────┐
│  Showing 41-80 of 11,806 results                               │
└─────────────────────────────────────────────────────────────────┘
```

### Items Per Page Selector
```
┌─────────────────────────────────────────────┐
│  Show: [40 ▼] items per page                │
│         ├─ 20                                │
│         ├─ 40 ✓                              │
│         ├─ 60                                │
│         └─ 100                               │
└─────────────────────────────────────────────┘
```

### Jump to Page
```
┌─────────────────────────────────────────────┐
│  Go to page: [___] [Go]                     │
└─────────────────────────────────────────────┘
```

## CSS Classes Used

### Layout
- `flex` - Flexbox layout
- `items-center` - Vertical center alignment
- `justify-between` - Space between items
- `space-x-3` - Horizontal spacing

### Styling
- `bg-white` - White background
- `border` - Border
- `border-neutral-200` - Light gray border
- `rounded-xl` - Extra large border radius
- `p-4` - Padding
- `mb-6` - Margin bottom

### Typography
- `text-sm` - Small text
- `font-medium` - Medium font weight
- `text-neutral-700` - Dark gray text

### Interactive
- `hover:bg-neutral-50` - Hover background
- `disabled:opacity-50` - Disabled opacity
- `disabled:cursor-not-allowed` - Disabled cursor
- `transition-fast` - Fast transition (150ms)

### Responsive
- `md:grid-cols-2` - 2 columns on medium screens
- `lg:grid-cols-3` - 3 columns on large screens
- `sm:px-6` - Padding on small screens
