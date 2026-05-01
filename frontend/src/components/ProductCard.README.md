# ProductCard Component

## Overview

The `ProductCard` component displays individual product information from search results. It's designed to be used in a grid layout to show products from multiple e-commerce platforms (Lazada, Shopee, TikTok Shop).

**Requirements:** 1.5

## Features

- ✅ Product image display with fallback for missing images
- ✅ Product name with line clamping (2 lines max)
- ✅ Current price with currency formatting
- ✅ Platform badge with color coding (Lazada: blue, Shopee: orange, TikTok Shop: pink)
- ✅ Availability status indicator
- ✅ "Track This Product" button with loading state
- ✅ Hover effects and smooth animations
- ✅ Responsive design with Tailwind CSS
- ✅ Link to view product on original platform
- ✅ Accessibility features (ARIA labels, keyboard navigation)

## Props

```typescript
interface ProductCardProps {
  /**
   * Product data to display
   */
  product: ProductResult;
  
  /**
   * Callback function when "Track" button is clicked
   */
  onTrack: (product: ProductResult) => void;
  
  /**
   * Whether the track button is disabled (e.g., during API call)
   */
  isTracking?: boolean;
}
```

### ProductResult Type

```typescript
interface ProductResult {
  platform: string;           // E-commerce platform (lazada, shopee, tiktokshop)
  product_url: string;        // URL to the product page
  product_name: string;       // Product name/title
  current_price: number;      // Current price
  currency: string;           // Currency code (PHP, USD, etc.)
  image_url?: string | null;  // Product image URL (optional)
  availability: boolean;      // Whether product is in stock
  scraped_at: string;         // ISO timestamp when data was scraped
}
```

## Usage

### Basic Usage

```tsx
import ProductCard from './components/ProductCard';
import { ProductResult } from './types/product';

function SearchResults() {
  const product: ProductResult = {
    platform: 'Lazada',
    product_url: 'https://www.lazada.com.ph/products/laptop-123',
    product_name: 'ASUS ROG Strix G15 Gaming Laptop',
    current_price: 45999.99,
    currency: 'PHP',
    image_url: 'https://example.com/laptop.jpg',
    availability: true,
    scraped_at: '2024-01-15T10:30:00Z',
  };

  const handleTrack = (product: ProductResult) => {
    console.log('Tracking:', product.product_name);
    // Call API to track product
  };

  return (
    <ProductCard 
      product={product} 
      onTrack={handleTrack} 
    />
  );
}
```

### Grid Layout (Typical Search Results)

```tsx
function SearchResults({ products }: { products: ProductResult[] }) {
  const handleTrack = async (product: ProductResult) => {
    try {
      await trackProduct(product);
      toast.success('Product tracked successfully!');
    } catch (error) {
      toast.error('Failed to track product');
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {products.map((product, index) => (
        <ProductCard 
          key={`${product.platform}-${index}`}
          product={product} 
          onTrack={handleTrack} 
        />
      ))}
    </div>
  );
}
```

### With Tracking State

```tsx
function SearchResults({ products }: { products: ProductResult[] }) {
  const [trackingId, setTrackingId] = useState<string | null>(null);

  const handleTrack = async (product: ProductResult) => {
    const productId = `${product.platform}-${product.product_url}`;
    setTrackingId(productId);
    
    try {
      await trackProduct(product);
      toast.success('Product tracked successfully!');
    } catch (error) {
      toast.error('Failed to track product');
    } finally {
      setTrackingId(null);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {products.map((product, index) => {
        const productId = `${product.platform}-${product.product_url}`;
        return (
          <ProductCard 
            key={productId}
            product={product} 
            onTrack={handleTrack}
            isTracking={trackingId === productId}
          />
        );
      })}
    </div>
  );
}
```

## Styling

The component uses Tailwind CSS classes and follows the app's design system:

### Colors

- **Primary**: Blue (`primary-500`, `primary-600`, `primary-700`)
- **Lazada Badge**: Blue (`bg-blue-100 text-blue-800`)
- **Shopee Badge**: Orange (`bg-orange-100 text-orange-800`)
- **TikTok Shop Badge**: Pink (`bg-pink-100 text-pink-800`)
- **Success**: Green (`success-600`) for "In Stock"
- **Error**: Red (`error-500`) for "Out of Stock"

### Animations

- **Hover Effect**: Card lifts up (`hover:-translate-y-1`) and shadow increases (`hover:shadow-xl`)
- **Transition**: Smooth 200ms transition (`transition-all duration-200`)
- **Loading Spinner**: Rotating spinner when `isTracking={true}`

### Responsive Design

- **Mobile**: Single column layout
- **Tablet (md)**: 2 columns
- **Desktop (lg)**: 3 columns

## Accessibility

- ✅ Semantic HTML elements (`<button>`, `<a>`, `<img>`)
- ✅ ARIA labels for screen readers
- ✅ Keyboard navigation support
- ✅ Focus states for interactive elements
- ✅ Alt text for images
- ✅ Disabled state for unavailable products

## Edge Cases Handled

1. **Missing Image**: Shows placeholder image when `image_url` is `null` or undefined
2. **Image Load Error**: Fallback to placeholder if image fails to load
3. **Out of Stock**: Disables track button and shows "Out of Stock" badge
4. **Tracking State**: Shows loading spinner and disables button during API call
5. **Long Product Names**: Clamps to 2 lines with ellipsis (`line-clamp-2`)
6. **Currency Formatting**: Supports PHP (₱), USD ($), and other currencies

## Platform Badge Colors

The component automatically applies the correct badge color based on the platform name:

| Platform | Badge Color |
|----------|-------------|
| Lazada | Blue (`bg-blue-100 text-blue-800`) |
| Shopee | Orange (`bg-orange-100 text-orange-800`) |
| TikTok Shop | Pink (`bg-pink-100 text-pink-800`) |
| Unknown | Primary Blue (`bg-primary-100 text-primary-800`) |

## Price Formatting

The component formats prices based on the currency:

- **PHP**: `₱45,999.99`
- **USD**: `$899.99`
- **Other**: `{currency} {price}`

All prices are formatted to 2 decimal places.

## Integration with DashboardPage

The ProductCard is designed to be used in the DashboardPage search results section:

```tsx
// In DashboardPage.tsx
import SearchBar from '../components/SearchBar';
import ProductCard from '../components/ProductCard';
import { SearchResults } from '../types/product';

function DashboardPage() {
  const [searchResults, setSearchResults] = useState<SearchResults | null>(null);

  const handleSearchResults = (results: SearchResults | null) => {
    setSearchResults(results);
  };

  const handleTrack = async (product: ProductResult) => {
    // Track product logic
  };

  return (
    <div>
      <SearchBar onSearchResults={handleSearchResults} />
      
      {searchResults && searchResults.results.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {searchResults.results.map((product, index) => (
            <ProductCard 
              key={`${product.platform}-${index}`}
              product={product}
              onTrack={handleTrack}
            />
          ))}
        </div>
      )}
    </div>
  );
}
```

## Examples

See `ProductCard.example.tsx` for complete usage examples including:
- Grid layout with multiple products
- Out of stock products
- Products without images
- Tracking state
- All platform badge colors

## Related Components

- **SearchBar**: Provides search functionality that returns ProductResult[]
- **TrackedProductCard**: Similar component for displaying tracked products (to be implemented)

## Future Enhancements

- [ ] Add "Quick View" modal for product details
- [ ] Add comparison feature (select multiple products)
- [ ] Add "Add to Wishlist" button
- [ ] Show price history preview on hover
- [ ] Add product rating/reviews if available from scrapers
