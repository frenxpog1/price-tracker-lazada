/**
 * TypeScript type definitions for products and search.
 * These types match the Pydantic schemas in backend/app/schemas/product.py
 */

/**
 * A single product search result
 */
export interface ProductResult {
  platform: string; // E-commerce platform (lazada, shopee, tiktokshop)
  product_url: string; // URL to the product page
  product_name: string; // Product name/title
  current_price: number | string; // Current price (Decimal in backend, can be string or number)
  currency: string; // Currency code (default: PHP)
  image_url?: string | null; // Product image URL (optional)
  availability: boolean; // Whether product is in stock
  scraped_at: string; // ISO timestamp when data was scraped
}

/**
 * Product search results from all platforms
 */
export interface SearchResults {
  query: string; // Search query used
  results: ProductResult[]; // List of products found
  total_results: number; // Total number of results
  platforms_searched: string[]; // Platforms that were searched
  platforms_failed: string[]; // Platforms that failed
  search_time_seconds: number; // Time taken to search
}

/**
 * A single price history entry
 */
export interface PriceHistoryEntry {
  price: number | string; // Price at this point in time (Decimal in backend, can be string or number)
  currency: string; // Currency code (default: PHP)
  checked_at: string; // ISO timestamp when price was checked
  availability: boolean; // Whether product was available
}

/**
 * Price history response for a tracked product
 */
export interface PriceHistoryResponse {
  product_id: string; // Tracked product ID
  product_name: string; // Product name
  product_url: string; // Product URL
  platform: string; // E-commerce platform
  current_price: number | string | null; // Current price (optional, can be string or number)
  price_threshold: number | string; // User's price threshold (can be string or number)
  history: PriceHistoryEntry[]; // Price history entries
  total_entries: number; // Total number of history entries
}
