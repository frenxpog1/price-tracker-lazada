/**
 * SearchBar Component Usage Examples
 * 
 * This file demonstrates how to use the SearchBar component in different scenarios.
 */

import { useState } from 'react';
import SearchBar from './SearchBar';
import { SearchResults } from '../types/product';

/**
 * Example 1: Basic Usage
 * 
 * Simple integration with state management for search results
 */
export function BasicSearchExample() {
  const [searchResults, setSearchResults] = useState<SearchResults | null>(null);
  const [searchError, setSearchError] = useState<string>('');

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Product Search</h1>
      
      <SearchBar
        onSearchResults={setSearchResults}
        onSearchError={setSearchError}
      />

      {/* Display error */}
      {searchError && (
        <div className="mb-4 p-4 bg-error-50 border border-error-200 rounded-lg">
          <p className="text-error-700">{searchError}</p>
        </div>
      )}

      {/* Display results */}
      {searchResults && (
        <div>
          <h2 className="text-xl font-semibold mb-4">
            Found {searchResults.total_results} products
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {searchResults.results.map((product, index) => (
              <div key={index} className="border rounded-lg p-4">
                <h3 className="font-semibold">{product.product_name}</h3>
                <p className="text-primary-500 font-bold">
                  {product.currency} {product.current_price}
                </p>
                <p className="text-sm text-neutral-600">{product.platform}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Example 2: With Custom Placeholder and Max Results
 * 
 * Customize the search bar appearance and behavior
 */
export function CustomizedSearchExample() {
  const [searchResults, setSearchResults] = useState<SearchResults | null>(null);

  return (
    <div className="p-8">
      <SearchBar
        onSearchResults={setSearchResults}
        placeholder="Find the best deals on electronics..."
        maxResults={20}
      />
      
      {searchResults && (
        <p className="text-neutral-600">
          Search completed in {searchResults.search_time_seconds.toFixed(2)}s
        </p>
      )}
    </div>
  );
}

/**
 * Example 3: With Platform Warnings
 * 
 * Display warnings when some platforms fail
 */
export function SearchWithWarningsExample() {
  const [searchResults, setSearchResults] = useState<SearchResults | null>(null);
  const [searchError, setSearchError] = useState<string>('');

  return (
    <div className="p-8">
      <SearchBar
        onSearchResults={setSearchResults}
        onSearchError={setSearchError}
      />

      {/* Display platform warnings */}
      {searchResults && searchResults.platforms_failed.length > 0 && (
        <div className="mb-4 p-4 bg-warning-50 border border-warning-200 rounded-lg">
          <p className="text-warning-700">
            Warning: Some platforms were unavailable: {searchResults.platforms_failed.join(', ')}
          </p>
        </div>
      )}

      {/* Display error */}
      {searchError && (
        <div className="mb-4 p-4 bg-error-50 border border-error-200 rounded-lg">
          <p className="text-error-700">{searchError}</p>
        </div>
      )}

      {/* Display results */}
      {searchResults && searchResults.results.length === 0 && (
        <div className="text-center py-12">
          <p className="text-neutral-600">No products found. Try a different search term.</p>
        </div>
      )}
    </div>
  );
}

/**
 * Example 4: Integration with DashboardPage
 * 
 * How to integrate SearchBar into the existing DashboardPage
 */
export function DashboardIntegrationExample() {
  const [searchResults, setSearchResults] = useState<SearchResults | null>(null);
  const [searchError, setSearchError] = useState<string>('');

  const handleSearchResults = (results: SearchResults | null) => {
    setSearchResults(results);
    // Clear error when new results arrive
    if (results) {
      setSearchError('');
    }
  };

  const handleSearchError = (error: string) => {
    setSearchError(error);
    // Clear results when error occurs
    setSearchResults(null);
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-neutral-900 mb-2">
            Track Your Favorite Products
          </h1>
          <p className="text-neutral-600">
            Search products and get notified when prices drop
          </p>
        </div>

        {/* Search Bar */}
        <SearchBar
          onSearchResults={handleSearchResults}
          onSearchError={handleSearchError}
        />

        {/* Error Display */}
        {searchError && (
          <div className="mb-6 p-4 bg-error-50 border border-error-200 rounded-lg">
            <div className="flex items-start">
              <svg 
                className="h-5 w-5 text-error-500 mt-0.5 mr-3 flex-shrink-0" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
                />
              </svg>
              <p className="text-sm text-error-700">{searchError}</p>
            </div>
          </div>
        )}

        {/* Platform Warnings */}
        {searchResults && searchResults.platforms_failed.length > 0 && (
          <div className="mb-6 p-4 bg-warning-50 border border-warning-200 rounded-lg">
            <div className="flex items-start">
              <svg 
                className="h-5 w-5 text-warning-500 mt-0.5 mr-3 flex-shrink-0" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" 
                />
              </svg>
              <div>
                <p className="text-sm font-medium text-warning-800 mb-1">
                  Some platforms were unavailable
                </p>
                <p className="text-sm text-warning-700">
                  {searchResults.platforms_failed.join(', ')} could not be searched. 
                  Results shown are from available platforms only.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Search Results */}
        {searchResults && searchResults.results.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold text-neutral-900 mb-6">
              Search Results ({searchResults.total_results})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {searchResults.results.map((product, index) => (
                <div
                  key={index}
                  className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-200 hover:-translate-y-1 overflow-hidden"
                >
                  {product.image_url && (
                    <div className="aspect-square bg-neutral-100">
                      <img 
                        src={product.image_url} 
                        alt={product.product_name} 
                        className="w-full h-full object-cover" 
                      />
                    </div>
                  )}
                  <div className="p-5">
                    <div className="flex items-center justify-between mb-2">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                        {product.platform}
                      </span>
                    </div>
                    <h3 className="text-lg font-semibold text-neutral-900 mb-2 line-clamp-2">
                      {product.product_name}
                    </h3>
                    <p className="text-2xl font-bold text-primary-500 mb-4">
                      {product.currency} {product.current_price}
                    </p>
                    <button className="w-full bg-primary-500 text-white py-2.5 px-4 rounded-lg font-semibold hover:bg-primary-600 transition-fast">
                      Track This Product
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {searchResults && searchResults.results.length === 0 && (
          <div className="text-center py-12">
            <svg 
              className="mx-auto h-12 w-12 text-neutral-400 mb-4" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
              />
            </svg>
            <h3 className="text-lg font-medium text-neutral-900 mb-2">
              No products found
            </h3>
            <p className="text-neutral-600">
              Try searching with different keywords or check your spelling.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
