/**
 * TypeScript type definitions for product tracking.
 * These types match the Pydantic schemas in backend/app/schemas/tracking.py
 */

/**
 * Request payload for creating a tracked product
 */
export interface TrackedProductCreate {
  platform: string; // E-commerce platform (lazada, shopee, tiktokshop)
  product_url: string; // URL to the product page
  product_name: string; // Product name/title
  current_price: number; // Current price (must be positive)
  price_threshold: number; // Price threshold for notifications (must be positive)
  currency?: string; // Currency code (default: PHP)
  image_url?: string | null; // Product image URL (optional)
}

/**
 * Tracked product response
 */
export interface TrackedProductResponse {
  id: string; // Tracked product ID
  user_id: string; // User ID who is tracking this product
  platform: string; // E-commerce platform
  product_url: string; // Product URL
  product_name: string; // Product name
  current_price: number | null; // Current price (optional)
  price_threshold: number; // Price threshold for notifications
  currency: string; // Currency code (default: PHP)
  image_url?: string | null; // Product image URL (optional)
  last_checked: string | null; // ISO timestamp of last price check (optional)
  created_at: string; // ISO timestamp when tracking started
}

/**
 * Request payload for updating price threshold
 */
export interface ThresholdUpdate {
  price_threshold: number; // New price threshold (must be positive)
}
