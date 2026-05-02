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
 * Restores mock prices from localStorage if they exist.
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
    const products = response.data;
    
    // Restore mock prices from localStorage
    return products.map(product => {
      const storedPrice = getMockCurrentPrice(product.id);
      if (storedPrice !== null) {
        return { ...product, current_price: storedPrice };
      }
      return product;
    });
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
 * @param currentPrice - Current price of the product (for mock data generation)
 * @returns Promise resolving to array of price history entries
 * @throws Error if the API request fails
 * 
 * @example
 * ```typescript
 * const history = await getPriceHistory("123e4567-e89b-12d3-a456-426614174000", 19990);
 * console.log(`Found ${history.length} price records`);
 * ```
 */
export async function getPriceHistory(productId: string, currentPrice?: number): Promise<PriceHistoryEntry[]> {
  try {
    const response = await api.get<PriceHistoryEntry[]>(`/tracking/products/${productId}/history`);
    
    // If no history exists, use dynamic mock data
    if (!response.data || response.data.length === 0) {
      return getDynamicMockHistory(productId, currentPrice);
    }
    
    return response.data;
  } catch (error) {
    console.error('Failed to get price history:', error);
    // Return dynamic mock data on error for demo purposes
    return getDynamicMockHistory(productId, currentPrice);
  }
}

/**
 * Generate mock price history for demo purposes.
 * Creates realistic price fluctuations over the past 30 days.
 * 
 * @param productId - ID of the tracked product
 * @param basePrice - Base price to use for generating history (optional)
 * @returns Array of mock price history entries
 */
function generateMockPriceHistory(productId: string, basePrice?: number): PriceHistoryEntry[] {
  const now = new Date();
  const history: PriceHistoryEntry[] = [];
  
  // Use provided base price or generate a random one
  const currentPrice = basePrice || (1000 + Math.random() * 4000);
  
  // Generate 30 days of price history leading up to current price
  for (let i = 30; i >= 1; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    
    // Add some realistic price variation (±10%)
    const variation = (Math.random() - 0.5) * 0.2; // -10% to +10%
    const historicalPrice = currentPrice * (1 + variation);
    
    history.push({
      id: `mock-${productId}-${i}`,
      price: Math.round(historicalPrice * 100) / 100, // Round to 2 decimals
      currency: 'PHP',
      timestamp: date.toISOString(),
      is_available: Math.random() > 0.1, // 90% availability
    });
  }
  
  // Add current price as the most recent entry
  history.push({
    id: `mock-${productId}-0`,
    price: currentPrice,
    currency: 'PHP',
    timestamp: now.toISOString(),
    is_available: true,
  });
  
  return history;
}

/**
 * Get or create dynamic mock history from localStorage.
 * This ensures price history persists and updates when prices change.
 * 
 * @param productId - ID of the tracked product
 * @param currentPrice - Current price of the product
 * @returns Array of price history entries
 */
function getDynamicMockHistory(productId: string, currentPrice?: number): PriceHistoryEntry[] {
  const storageKey = `price_history_${productId}`;
  
  try {
    // Try to get existing history from localStorage
    const stored = localStorage.getItem(storageKey);
    
    if (stored && currentPrice !== undefined) {
      const history: PriceHistoryEntry[] = JSON.parse(stored);
      
      // Check if we need to add a new entry (price changed or time passed)
      const lastEntry = history[history.length - 1];
      const lastPrice = typeof lastEntry.price === 'string' ? parseFloat(lastEntry.price) : lastEntry.price;
      const lastTime = new Date(lastEntry.timestamp).getTime();
      const now = Date.now();
      
      // Add new entry if price changed or more than 5 minutes passed
      if (Math.abs(lastPrice - currentPrice) > 0.01 || (now - lastTime) > 300000) {
        history.push({
          id: `mock-${productId}-${Date.now()}`,
          price: Math.round(currentPrice * 100) / 100,
          currency: 'PHP',
          timestamp: new Date().toISOString(),
          is_available: true,
        });
        
        // Keep only last 60 entries (about 30 days if updated hourly)
        if (history.length > 60) {
          history.splice(0, history.length - 60);
        }
        
        // Save updated history
        localStorage.setItem(storageKey, JSON.stringify(history));
      }
      
      return history;
    }
    
    // No existing history, generate initial mock data
    const history = generateMockPriceHistory(productId, currentPrice);
    localStorage.setItem(storageKey, JSON.stringify(history));
    return history;
    
  } catch (error) {
    console.error('Failed to access localStorage for price history:', error);
    // Fallback to generating fresh mock data
    return generateMockPriceHistory(productId, currentPrice);
  }
}

/**
 * Update price history when price changes (for mock data).
 * This is called when prices are randomized to keep history in sync.
 * 
 * @param productId - ID of the tracked product
 * @param newPrice - New price to add to history
 */
export function updateMockPriceHistory(productId: string, newPrice: number): void {
  const storageKey = `price_history_${productId}`;
  
  try {
    const stored = localStorage.getItem(storageKey);
    
    if (stored) {
      const history: PriceHistoryEntry[] = JSON.parse(stored);
      
      // Add new entry
      history.push({
        id: `mock-${productId}-${Date.now()}`,
        price: Math.round(newPrice * 100) / 100,
        currency: 'PHP',
        timestamp: new Date().toISOString(),
        is_available: true,
      });
      
      // Keep only last 60 entries
      if (history.length > 60) {
        history.splice(0, history.length - 60);
      }
      
      // Save updated history
      localStorage.setItem(storageKey, JSON.stringify(history));
      console.log(`Updated price history for ${productId}: ${newPrice}`);
    }
  } catch (error) {
    console.error('Failed to update mock price history:', error);
  }
}

/**
 * Store the current mock price in localStorage.
 * This allows prices to persist across page reloads.
 * 
 * @param productId - ID of the tracked product
 * @param price - Current price to store
 */
function storeMockCurrentPrice(productId: string, price: number): void {
  const storageKey = `current_price_${productId}`;
  
  try {
    localStorage.setItem(storageKey, price.toString());
  } catch (error) {
    console.error('Failed to store mock current price:', error);
  }
}

/**
 * Get the stored mock current price from localStorage.
 * Returns null if no stored price exists.
 * 
 * @param productId - ID of the tracked product
 * @returns Stored price or null
 */
function getMockCurrentPrice(productId: string): number | null {
  const storageKey = `current_price_${productId}`;
  
  try {
    const stored = localStorage.getItem(storageKey);
    if (stored) {
      const price = parseFloat(stored);
      return isNaN(price) ? null : price;
    }
  } catch (error) {
    console.error('Failed to get mock current price:', error);
  }
  
  return null;
}

/**
 * Randomize the price of a tracked product (for testing).
 * Simulates a price change and checks if it triggers the threshold.
 * 
 * @param productId - ID of the tracked product
 * @param currentPrice - Current price of the product
 * @param threshold - Price threshold
 * @param smallChange - If true, uses smaller variation (±5% for hourly changes)
 * @returns Promise resolving to the new price and whether threshold was triggered
 * 
 * @example
 * ```typescript
 * const result = await randomizePrice("123...", 5000, 3000);
 * if (result.thresholdTriggered) {
 *   console.log('Price dropped below threshold!');
 * }
 * ```
 */
export async function randomizePrice(
  productId: string,
  currentPrice: number,
  threshold: number,
  smallChange: boolean = false
): Promise<{ newPrice: number; thresholdTriggered: boolean; priceDropped: boolean }> {
  // Generate a new random price
  // Small change (hourly): ±5%, Large change (manual): ±30%
  const maxVariation = smallChange ? 0.1 : 0.6; // 5% or 30%
  const variation = (Math.random() - 0.5) * maxVariation;
  const newPrice = Math.round(currentPrice * (1 + variation) * 100) / 100;
  
  // Check if threshold was triggered
  const thresholdTriggered = newPrice <= threshold && currentPrice > threshold;
  const priceDropped = newPrice < currentPrice;
  
  console.log('randomizePrice:', {
    productId,
    currentPrice,
    newPrice,
    threshold,
    thresholdTriggered,
    priceDropped,
    smallChange
  });
  
  // Store the new price in localStorage
  storeMockCurrentPrice(productId, newPrice);
  
  // Update mock price history
  updateMockPriceHistory(productId, newPrice);
  
  // In a real app, this would update the backend
  // For now, we'll just return the simulated result
  console.log(`Price ${smallChange ? 'auto-' : ''}randomized: ${currentPrice} → ${newPrice} (Threshold: ${threshold})`);
  
  return {
    newPrice,
    thresholdTriggered,
    priceDropped,
  };
}

/**
 * Start automatic price randomization for all tracked products.
 * Changes prices every hour with small variations (±5%).
 * 
 * @param getProducts - Function to get current products
 * @param onPriceChange - Callback when a price changes
 * @returns Cleanup function to stop the interval
 */
export function startAutoPriceRandomization(
  getProducts: () => TrackedProduct[],
  onPriceChange: (productId: string, newPrice: number, thresholdTriggered: boolean) => void
): () => void {
  // Randomize prices every hour (3600000 ms)
  // For testing, you can change this to 60000 (1 minute) or 10000 (10 seconds)
  const INTERVAL = 3600000; // 1 hour
  
  const intervalId = setInterval(async () => {
    const products = getProducts(); // Get fresh products
    console.log('Auto-randomizing prices for', products.length, 'products...');
    
    for (const product of products) {
      const currentPrice = typeof product.current_price === 'string' 
        ? parseFloat(product.current_price) 
        : product.current_price;
      
      const threshold = typeof product.price_threshold === 'string'
        ? parseFloat(product.price_threshold)
        : product.price_threshold;
      
      try {
        const result = await randomizePrice(
          product.id,
          currentPrice,
          threshold,
          true // Small change for hourly updates
        );
        
        onPriceChange(product.id, result.newPrice, result.thresholdTriggered);
      } catch (error) {
        console.error(`Failed to randomize price for product ${product.id}:`, error);
      }
    }
  }, INTERVAL);
  
  // Return cleanup function
  return () => {
    clearInterval(intervalId);
    console.log('Stopped auto price randomization');
  };
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