/**
 * Product service for product search operations.
 * 
 * This module provides methods for:
 * - Searching products across multiple e-commerce platforms
 * - Client-side scraping (runs in user's browser, no server needed)
 * 
 * Requirements covered:
 * - 1.1: Search Lazada products
 * - 1.2: Search Shopee products
 * - 1.3: Search TikTok Shop products
 */

import api from './api';
import { SearchResults } from '../types/product';
import { scrapeLazada } from './clientScraper';

/**
 * Search for products using CLIENT-SIDE scraping.
 * This runs in the user's browser, avoiding server costs and bot detection.
 * 
 * @param query - Search query string
 * @param maxResults - Maximum results per platform (default 40)
 * @param page - Page number (default 1)
 * @param sortBy - Sort option (default 'best_match')
 * @returns Promise resolving to SearchResults
 */
export async function searchProducts(
  query: string,
  maxResults: number = 40,
  page: number = 1,
  sortBy: string = 'best_match'
): Promise<SearchResults> {
  try {
    // Use client-side scraping (runs in user's browser)
    const lazadaResults = await scrapeLazada(query, page, maxResults, sortBy);
    
    // Convert to SearchResults format
    return {
      query: lazadaResults.query,
      results: lazadaResults.results.map(product => ({
        ...product,
        scraped_at: new Date().toISOString()
      })),
      total_results: lazadaResults.total_results,
      platforms_searched: ['lazada'],
      platforms_failed: [],
      search_time_seconds: lazadaResults.search_time_seconds
    };
  } catch (error) {
    console.error('Failed to search products:', error);
    
    // Fallback to server-side API if client-side fails
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
    } catch (apiError) {
      console.error('Server-side API also failed:', apiError);
      throw error;
    }
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
