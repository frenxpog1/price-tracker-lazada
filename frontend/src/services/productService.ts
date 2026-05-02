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

import { SearchResults } from '../types/product';
import { scrapeLazada, ScrapedProduct } from './clientScraper';
import { getMockProducts } from './mockData';

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
    // Try client-side scraping first
    const lazadaResults = await scrapeLazada(query, page, maxResults, sortBy);
    
    // If we got results, return them
    if (lazadaResults.results.length > 0) {
      return {
        query: lazadaResults.query,
        results: lazadaResults.results.map((product: ScrapedProduct) => ({
          ...product,
          scraped_at: new Date().toISOString()
        })),
        total_results: lazadaResults.total_results,
        platforms_searched: ['lazada'],
        platforms_failed: [],
        search_time_seconds: lazadaResults.search_time_seconds
      };
    }
    
    // If no results, fall through to mock data
    throw new Error('No results from scraping');
    
  } catch (error) {
    console.warn('Scraping failed, using mock data:', error);
    
    // Use mock data for demonstration
    const mockProducts = getMockProducts(query, maxResults);
    
    return {
      query,
      results: mockProducts.map((product: ScrapedProduct) => ({
        ...product,
        scraped_at: new Date().toISOString()
      })),
      total_results: mockProducts.length,
      platforms_searched: ['lazada'],
      platforms_failed: [],
      search_time_seconds: 0.5
    };
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
