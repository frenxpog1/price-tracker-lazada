# SearchBar Component

A React component for searching products across multiple e-commerce platforms with debouncing and loading states.

## Features

- ✅ **Debounced Search**: Waits 500ms after user stops typing before triggering search
- ✅ **Loading States**: Shows spinner and "Searching..." text during API calls
- ✅ **Error Handling**: Gracefully handles network errors, API errors, and authentication issues
- ✅ **Clear Functionality**: Allows users to clear search with a button
- ✅ **Immediate Search**: Supports form submission to bypass debounce
- ✅ **Accessible**: Includes ARIA labels and semantic HTML
- ✅ **Responsive**: Works on all screen sizes with Tailwind CSS
- ✅ **Multi-Platform**: Searches Lazada, Shopee, and TikTok Shop simultaneously

## Requirements Covered

- **Requirement 1.1**: Search Lazada products
- **Requirement 1.2**: Search Shopee products
- **Requirement 1.3**: Search TikTok Shop products

## Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `onSearchResults` | `(results: SearchResults \| null) => void` | Yes | - | Callback function called when search results are available or cleared |
| `onSearchError` | `(error: string) => void` | No | - | Callback function called when search error occurs |
| `placeholder` | `string` | No | `"Search products across Lazada, Shopee, TikTok Shop..."` | Placeholder text for the search input |
| `maxResults` | `number` | No | `10` | Maximum results per platform |

## Usage

### Basic Usage

```tsx
import { useState } from 'react';
import SearchBar from './components/SearchBar';
import { SearchResults } from './types/product';

function App() {
  const [searchResults, setSearchResults] = useState<SearchResults | null>(null);

  return (
    <div>
      <SearchBar onSearchResults={setSearchResults} />
      
      {searchResults && (
        <div>
          <h2>Found {searchResults.total_results} products</h2>
          {searchResults.results.map((product, index) => (
            <div key={index}>
              <h3>{product.product_name}</h3>
              <p>{product.currency} {product.current_price}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### With Error Handling

```tsx
import { useState } from 'react';
import SearchBar from './components/SearchBar';
import { SearchResults } from './types/product';

function App() {
  const [searchResults, setSearchResults] = useState<SearchResults | null>(null);
  const [searchError, setSearchError] = useState<string>('');

  return (
    <div>
      <SearchBar
        onSearchResults={setSearchResults}
        onSearchError={setSearchError}
      />
      
      {searchError && (
        <div className="error-message">
          {searchError}
        </div>
      )}
      
      {searchResults && (
        <div>
          {/* Display results */}
        </div>
      )}
    </div>
  );
}
```

### With Custom Configuration

```tsx
<SearchBar
  onSearchResults={setSearchResults}
  onSearchError={setSearchError}
  placeholder="Find the best deals..."
  maxResults={20}
/>
```

### Integration with DashboardPage

See `SearchBar.example.tsx` for a complete example of integrating the SearchBar into the DashboardPage.

## Behavior

### Debouncing

The SearchBar implements a 500ms debounce delay. This means:

1. User types "laptop"
2. SearchBar waits 500ms after the last keystroke
3. If no more keystrokes occur, the search is triggered
4. If user continues typing, the timer resets

This prevents excessive API calls while the user is still typing.

### Form Submission

Users can press Enter to immediately trigger a search, bypassing the debounce delay.

### Loading States

While a search is in progress:
- A spinning loader icon appears on the right side of the input
- "Searching..." text is displayed
- The input remains enabled (users can continue typing)

### Clear Functionality

When the input has text and is not searching:
- A clear button (X icon) appears on the right side
- Clicking it clears the input and resets search results
- Calls `onSearchResults(null)` to notify parent component

### Error Handling

The component handles various error scenarios:

| Error Type | User Message |
|------------|--------------|
| Network Error | "Network error. Please check your connection." |
| 401 Unauthorized | "Your session has expired. Please log in again." |
| 400 Bad Request | "Invalid search query." (or API error message) |
| 500 Server Error | "Server error. Please try again later." |
| Other Errors | "An error occurred while searching. Please try again." |

## API Integration

The SearchBar calls `searchProducts()` from `services/productService.ts`:

```typescript
const results = await searchProducts(query, maxResults);
```

This function:
- Makes a GET request to `/api/products/search`
- Includes the JWT token for authentication
- Returns results from all three platforms (Lazada, Shopee, TikTok Shop)
- Handles platform failures gracefully

## SearchResults Type

```typescript
interface SearchResults {
  query: string;                  // Search query used
  results: ProductResult[];       // Array of products found
  total_results: number;          // Total number of results
  platforms_searched: string[];   // Platforms that were searched
  platforms_failed: string[];     // Platforms that failed
  search_time_seconds: number;    // Time taken to search
}
```

## Styling

The component uses Tailwind CSS classes matching the app's design system:

- **Colors**: Primary blue (`primary-500`), neutral grays
- **Spacing**: Consistent padding and margins
- **Transitions**: Smooth animations (`transition-fast`)
- **Shadows**: Subtle shadow on input
- **Focus States**: Blue ring on focus

## Accessibility

The component follows accessibility best practices:

- ✅ Semantic HTML (`<form>`, `<input>`, `<button>`)
- ✅ ARIA labels (`aria-label`, `aria-live`, `aria-busy`)
- ✅ Keyboard navigation (Enter to submit, Tab to navigate)
- ✅ Screen reader support (loading states announced)
- ✅ Focus indicators (visible focus ring)

## Testing

See `SearchBar.test.tsx` for example test cases covering:

- Rendering with placeholder
- Debouncing behavior (500ms delay)
- Loading states during search
- Search results callback
- Error handling
- Clear functionality
- Form submission

To run tests (after setting up testing framework):

```bash
npm test SearchBar
```

## Performance Considerations

- **Debouncing**: Reduces API calls by waiting for user to finish typing
- **Cleanup**: Properly cleans up timers to prevent memory leaks
- **Memoization**: Uses `useCallback` to prevent unnecessary re-renders
- **Conditional Rendering**: Only shows loading/clear buttons when needed

## Browser Support

Works in all modern browsers that support:
- ES6+ JavaScript
- CSS Grid and Flexbox
- SVG icons

## Dependencies

- React 18+
- TypeScript
- Tailwind CSS
- Axios (via `services/productService.ts`)

## Future Enhancements

Potential improvements for future versions:

- [ ] Search history/suggestions
- [ ] Autocomplete
- [ ] Voice search
- [ ] Advanced filters (price range, platform selection)
- [ ] Search analytics
- [ ] Keyboard shortcuts (Ctrl+K to focus)
- [ ] Recent searches dropdown

## Related Components

- `ProductCard`: Displays individual search results
- `DashboardPage`: Main page that uses SearchBar
- `productService`: API service for search functionality

## Support

For issues or questions about the SearchBar component, please refer to:
- Component source: `frontend/src/components/SearchBar.tsx`
- Usage examples: `frontend/src/components/SearchBar.example.tsx`
- Test examples: `frontend/src/components/SearchBar.test.tsx`
