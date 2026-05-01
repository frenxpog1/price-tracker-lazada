/**
 * Tracking service for product tracking operations.
 * 
 * This module provides methods for:
 * - Creating tracked products
 * - Retrieving user's tracked products
 * - Updating price thresholds
 * - Deleting tracked products
 * 
 * Requirements covered:
 * - 2.1: Track products from search results
 * - 2.2: Set price drop thresholds
 * - 2.4: View tracked products
 * - 2.5: Delete tracked products
 * - 8.1: Update price thresholds
 */

import api from './api';
import { ProductResult } from '../types/product';

/**
 * Interface for creating a tracked product
 */
export interface CreateTrackedProductRequest {
  product_name: string;
  product_url: string;
  platform: string;
  current_price: number;
  currency: string;
  price_threshold: number; // Changed from threshold_price to price_threshold to match backend
  image_url?: string;
}

/**
 * Interface for tracked product response
 */
export interface TrackedProduct {
  id: string; // Changed from number to string (UUID)
  product_name: string;
  product_url: string;
  platform: string;
  current_price: number | string; // Can be number or string (Decimal from backend)
  currency: string;
  price_threshold: number | string; // Can be number or string (Decimal from backend)
  image_url?: string;
  created_at: string;
  last_checked?: string;
  // These fields are computed on the frontend since they're not in the backend model yet
  is_available?: boolean;
  price_drop_detected?: boolean;
}

/**
 * Interface for updating threshold
 */
export interface UpdateThresholdRequest {
  price_threshold: number; // Changed from threshold_price to price_threshold to match backend
}

/**
 * Interface for price history entry
 */
export interface PriceHistoryEntry {
  id: string; // Changed from number to string (UUID)
  price: number | string; // Can be number or string (Decimal from backend)
  currency: string;
  timestamp: string;
  is_available: boolean;
}

/**
 * Track a product from search results.
 * 
 * Creates a new tracked product with the specified threshold price.
 * 
 * @param product - Product from search results
 * @param thresholdPrice - Price threshold for notifications
 * @returns Promise resolving to the created tracked product
 * @throws Error if the API request fails
 * 
 * @example
 * ```typescript
 * const trackedProduct = await trackProduct(searchResult, 99.99);
 * console.log(`Now tracking: ${trackedProduct.product_name}`);
 * ```
 */
export async function trackProduct(
  product: ProductResult,
  thresholdPrice: number
): Promise<TrackedProduct> {
  try {
    const request: CreateTrackedProductRequest = {
      product_name: product.product_name,
      product_url: product.product_url,
      platform: product.platform,
      current_price: typeof product.current_price === 'string' 
        ? parseFloat(product.current_price) 
        : product.current_price,
      currency: product.currency,
      price_threshold: thresholdPrice, // Changed from threshold_price to price_threshold
      image_url: product.image_url || undefined,
    };

    const response = await api.post<TrackedProduct>('/tracking/products', request);
    return response.data;
  } catch (error) {
    console.error('Failed to track product:', error);
    throw error;
  }
}

/**
 * Get all tracked products for the current user.
 * 
 * @returns Promise resolving to array of tracked products
 * @throws Error if the API request fails
 * 
 * @example
 * ```typescript
 * const trackedProducts = await getTrackedProducts();
 * console.log(`You are tracking ${trackedProducts.length} products`);
 * ```
 */
export async function getTrackedProducts(): Promise<TrackedProduct[]> {
  try {
    const response = await api.get<TrackedProduct[]>('/tracking/products');
    return response.data;
  } catch (error) {
    console.error('Failed to get tracked products:', error);
    throw error;
  }
}

/**
 * Update the price threshold for a tracked product.
 * 
 * @param productId - ID of the tracked product (UUID string)
 * @param thresholdPrice - New threshold price
 * @returns Promise resolving to the updated tracked product
 * @throws Error if the API request fails
 * 
 * @example
 * ```typescript
 * const updated = await updateThreshold("123e4567-e89b-12d3-a456-426614174000", 89.99);
 * console.log(`Threshold updated to ${updated.threshold_price}`);
 * ```
 */
export async function updateThreshold(
  productId: string, // Changed from number to string
  thresholdPrice: number
): Promise<TrackedProduct> {
  try {
    const request: UpdateThresholdRequest = {
      price_threshold: thresholdPrice, // Changed from threshold_price to price_threshold
    };

    const response = await api.patch<TrackedProduct>(
      `/tracking/products/${productId}/threshold`,
      request
    );
    return response.data;
  } catch (error) {
    console.error('Failed to update threshold:', error);
    throw error;
  }
}

/**
 * Delete a tracked product.
 * 
 * @param productId - ID of the tracked product to delete (UUID string)
 * @returns Promise that resolves when deletion is complete
 * @throws Error if the API request fails
 * 
 * @example
 * ```typescript
 * await deleteTrackedProduct("123e4567-e89b-12d3-a456-426614174000");
 * console.log('Product removed from tracking');
 * ```
 */
export async function deleteTrackedProduct(productId: string): Promise<void> { // Changed from number to string
  try {
    await api.delete(`/tracking/products/${productId}`);
  } catch (error) {
    console.error('Failed to delete tracked product:', error);
    throw error;
  }
}

/**
 * Get price history for a tracked product.
 * 
 * @param productId - ID of the tracked product (UUID string)
 * @returns Promise resolving to array of price history entries
 * @throws Error if the API request fails
 * 
 * @example
 * ```typescript
 * const history = await getPriceHistory("123e4567-e89b-12d3-a456-426614174000");
 * console.log(`Found ${history.length} price records`);
 * ```
 */
export async function getPriceHistory(productId: string): Promise<PriceHistoryEntry[]> { // Changed from number to string
  try {
    const response = await api.get<PriceHistoryEntry[]>(`/tracking/products/${productId}/history`);
    return response.data;
  } catch (error) {
    console.error('Failed to get price history:', error);
    throw error;
  }
}

/**
 * Usage Examples:
 * 
 * // Track a product from search results
 * const searchResult = { ... }; // ProductResult from search
 * const tracked = await trackProduct(searchResult, 99.99);
 * 
 * // Get all tracked products
 * const allTracked = await getTrackedProducts();
 * 
 * // Update threshold
 * const updated = await updateThreshold(tracked.id, 89.99);
 * 
 * // Get price history
 * const history = await getPriceHistory(tracked.id);
 * 
 * // Delete tracked product
 * await deleteTrackedProduct(tracked.id);
 * 
 * // Handle errors
 * try {
 *   const tracked = await trackProduct(product, 50.00);
 *   console.log('Successfully tracking product');
 * } catch (error) {
 *   if (error.response?.status === 409) {
 *     console.log('Product is already being tracked');
 *   } else {
 *     console.error('Failed to track product:', error);
 *   }
 * }
 */