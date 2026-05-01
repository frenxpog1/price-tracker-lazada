/**
 * ProductCard Component Usage Examples
 * 
 * This file demonstrates how to use the ProductCard component
 * with different product data scenarios.
 */

import ProductCard from './ProductCard';
import { ProductResult } from '../types/product';

/**
 * Example 1: Available product from Lazada
 */
const lazadaProduct: ProductResult = {
  platform: 'Lazada',
  product_url: 'https://www.lazada.com.ph/products/laptop-123',
  product_name: 'ASUS ROG Strix G15 Gaming Laptop - Intel Core i7, 16GB RAM, RTX 3060',
  current_price: 45999.99,
  currency: 'PHP',
  image_url: 'https://via.placeholder.com/300x300?text=ASUS+Laptop',
  availability: true,
  scraped_at: '2024-01-15T10:30:00Z',
};

/**
 * Example 2: Available product from Shopee
 */
const shopeeProduct: ProductResult = {
  platform: 'Shopee',
  product_url: 'https://shopee.ph/product/456',
  product_name: 'iPhone 15 Pro Max 256GB - Natural Titanium',
  current_price: 1199.99,
  currency: 'USD',
  image_url: 'https://via.placeholder.com/300x300?text=iPhone+15',
  availability: true,
  scraped_at: '2024-01-15T10:31:00Z',
};

/**
 * Example 3: Available product from TikTok Shop
 */
const tiktokProduct: ProductResult = {
  platform: 'TikTok Shop',
  product_url: 'https://www.tiktok.com/shop/product/789',
  product_name: 'Sony WH-1000XM5 Wireless Noise Cancelling Headphones',
  current_price: 349.99,
  currency: 'USD',
  image_url: 'https://via.placeholder.com/300x300?text=Sony+Headphones',
  availability: true,
  scraped_at: '2024-01-15T10:32:00Z',
};

/**
 * Example 4: Out of stock product
 */
const outOfStockProduct: ProductResult = {
  platform: 'Lazada',
  product_url: 'https://www.lazada.com.ph/products/sold-out-999',
  product_name: 'PlayStation 5 Console - Limited Edition',
  current_price: 29999.00,
  currency: 'PHP',
  image_url: 'https://via.placeholder.com/300x300?text=PS5',
  availability: false,
  scraped_at: '2024-01-15T10:33:00Z',
};

/**
 * Example 5: Product without image
 */
const noImageProduct: ProductResult = {
  platform: 'Shopee',
  product_url: 'https://shopee.ph/product/111',
  product_name: 'Generic USB-C Cable 2m Fast Charging',
  current_price: 299.00,
  currency: 'PHP',
  image_url: null,
  availability: true,
  scraped_at: '2024-01-15T10:34:00Z',
};

/**
 * Example usage in a component
 */
export default function ProductCardExamples() {
  const handleTrack = (product: ProductResult) => {
    console.log('Tracking product:', product.product_name);
    // In real usage, this would call an API to track the product
  };

  return (
    <div className="min-h-screen bg-neutral-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-neutral-900 mb-8">
          ProductCard Component Examples
        </h1>

        {/* Example 1: Grid Layout (typical search results) */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-neutral-900 mb-4">
            Grid Layout (Search Results)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ProductCard product={lazadaProduct} onTrack={handleTrack} />
            <ProductCard product={shopeeProduct} onTrack={handleTrack} />
            <ProductCard product={tiktokProduct} onTrack={handleTrack} />
          </div>
        </section>

        {/* Example 2: Out of Stock Product */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-neutral-900 mb-4">
            Out of Stock Product
          </h2>
          <div className="max-w-sm">
            <ProductCard product={outOfStockProduct} onTrack={handleTrack} />
          </div>
        </section>

        {/* Example 3: Product Without Image */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-neutral-900 mb-4">
            Product Without Image (Fallback)
          </h2>
          <div className="max-w-sm">
            <ProductCard product={noImageProduct} onTrack={handleTrack} />
          </div>
        </section>

        {/* Example 4: Tracking State */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-neutral-900 mb-4">
            Tracking State (Button Disabled)
          </h2>
          <div className="max-w-sm">
            <ProductCard 
              product={lazadaProduct} 
              onTrack={handleTrack} 
              isTracking={true} 
            />
          </div>
        </section>

        {/* Example 5: All Platforms */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold text-neutral-900 mb-4">
            All Platform Badge Colors
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <ProductCard product={lazadaProduct} onTrack={handleTrack} />
            <ProductCard product={shopeeProduct} onTrack={handleTrack} />
            <ProductCard product={tiktokProduct} onTrack={handleTrack} />
          </div>
        </section>
      </div>
    </div>
  );
}
