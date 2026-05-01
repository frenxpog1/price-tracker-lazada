/**
 * Product service for product search operations.
 * 
 * This module provides methods for:
 * - Searching products across multiple e-commerce platforms
 * 
 * Requirements covered:
 * - 1.1: Search Lazada products
 * - 1.2: Search Shopee products
 * - 1.3: Search TikTok Shop products
 */

import api from './api';
import { SearchResults } from '../types/product';

/**
 * Search for products across all supported e-commerce platforms.
 * 
 * Makes a GET request to /api/products/search with the search query.
 * Returns results from Lazada, Shopee, and TikTok Shop.
 * 
 * @param query - Search query string (required, min length 1)
 * @param maxResults - Maximum results per platform (1-50, default 10)
 * @returns Promise resolving to SearchResults containing products from all platforms
 * @throws Error if the API request fails
 * 
 * @example
 * ```typescript
 * const results = await searchProducts('laptop');
 * console.log(results.results); // Array of ProductResult
 * console.log(results.platforms_searched); // ['lazada', 'shopee', 'tiktokshop']
 * ```
 */
export async function searchProducts(
  query: string,
  maxResults: number = 40,
  page: number = 1,
  sortBy: string = 'best_match'
): Promise<SearchResults> {
  try {
    const response = await api.get<SearchResults>('/products/search', {
      params: {
        q: query,
        max_results: maxResults,
        page: page,
        sort_by: sortBy,
      },
    });

    return response.data;
  } catch (error) {
    console.error('Failed to search products:', error);
    throw error;
  }
}

/**
 * Usage Examples:
 * 
 * // Basic search
 * const results = await searchProducts('laptop');
 * 
 * // Search with custom max results
 * const results = await searchProducts('smartphone', 20);
 * 
 * // Handle errors
 * try {
 *   const results = await searchProducts('tablet');
 *   console.log(`Found ${results.total_results} products`);
 * } catch (error) {
 *   console.error('Search failed:', error);
 * }
 * 
 * // Access results
 * const results = await searchProducts('headphones');
 * results.results.forEach(product => {
 *   console.log(`${product.product_name} - ${product.current_price} ${product.currency}`);
 *   console.log(`Platform: ${product.platform}`);
 *   console.log(`URL: ${product.product_url}`);
 * });
 * 
 * // Check for platform failures
 * if (results.platforms_failed.length > 0) {
 *   console.warn(`Some platforms failed: ${results.platforms_failed.join(', ')}`);
 * }
 */
