/**
 * SearchBar Component
 * 
 * A search input component with debouncing for product search.
 * 
 * Features:
 * - Search input field with icon
 * - Debouncing (500ms delay after user stops typing)
 * - Loading spinner while searching
 * - Calls searchProducts from productService
 * - Emits search results to parent via callback
 * - Error handling with user-friendly messages
 * - Tailwind CSS styling matching app design
 * 
 * Requirements: 1.1, 1.2, 1.3
 */

import { useState, useEffect } from 'react';
import { searchProducts } from '../services/productService';
import { SearchResults } from '../types/product';

interface SearchBarProps {
  /**
   * Callback function called when search results are available
   */
  onSearchResults: (results: SearchResults | null) => void;
  
  /**
   * Callback function called when search error occurs
   */
  onSearchError?: (error: string) => void;
  
  /**
   * Callback function called when a new search query is initiated
   */
  onNewSearch?: () => void;
  
  /**
   * Placeholder text for the search input
   */
  placeholder?: string;
  
  /**
   * Maximum results per platform (default: 40)
   */
  maxResults?: number;
  
  /**
   * Page number (default: 1)
   */
  page?: number;
  
  /**
   * Sort option (default: "best_match")
   */
  sortBy?: string;
}

export default function SearchBar({
  onSearchResults,
  onSearchError,
  onNewSearch,
  placeholder = 'Search products across Lazada, Shopee, TikTok Shop...',
  maxResults = 40,
  page = 1,
  sortBy = 'best_match',
}: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [debouncedQuery, setDebouncedQuery] = useState('');
  const [lastSearchedQuery, setLastSearchedQuery] = useState('');

  /**
   * Debounce the search query
   * Waits 500ms after user stops typing before updating debouncedQuery
   */
  useEffect(() => {
    // Don't debounce empty queries
    if (!query.trim()) {
      setDebouncedQuery('');
      return;
    }

    // Set up debounce timer
    const timeoutId = setTimeout(() => {
      setDebouncedQuery(query.trim());
    }, 500);

    // Cleanup function to clear timeout if query changes
    return () => {
      clearTimeout(timeoutId);
    };
  }, [query]);

  /**
   * Trigger search when debouncedQuery, page, or sortBy changes
   * Use AbortController to prevent race conditions
   */
  useEffect(() => {
    if (!debouncedQuery) {
      onSearchResults(null);
      return;
    }

    // Check if this is a new search query (not just pagination/sort change)
    const isNewQuery = debouncedQuery !== lastSearchedQuery;
    if (isNewQuery && onNewSearch) {
      onNewSearch();
      setLastSearchedQuery(debouncedQuery);
    }

    // Create an AbortController to cancel previous requests
    const abortController = new AbortController();
    
    const executeSearch = async () => {
      setIsSearching(true);

      try {
        // Call searchProducts from productService
        const results = await searchProducts(debouncedQuery, maxResults, page, sortBy);
        
        // Only update results if this request wasn't cancelled
        if (!abortController.signal.aborted) {
          onSearchResults(results);
        }
      } catch (error: any) {
        // Only handle error if this request wasn't cancelled
        if (!abortController.signal.aborted) {
          console.error('Search error:', error);
          
          // Handle different error types
          let errorMessage = 'An error occurred while searching. Please try again.';
          
          if (error.response?.status === 401) {
            errorMessage = 'Your session has expired. Please log in again.';
          } else if (error.response?.status === 400) {
            errorMessage = error.response.data?.detail || 'Invalid search query.';
          } else if (error.response?.status >= 500) {
            errorMessage = 'Server error. Please try again later.';
          } else if (error.message === 'Network Error') {
            errorMessage = 'Network error. Please check your connection.';
          }
          
          // Emit error to parent component
          if (onSearchError) {
            onSearchError(errorMessage);
          }
          
          // Clear results on error
          onSearchResults(null);
        }
      } finally {
        // Only update loading state if this request wasn't cancelled
        if (!abortController.signal.aborted) {
          setIsSearching(false);
        }
      }
    };

    executeSearch();

    // Cleanup function to cancel the request if component unmounts or dependencies change
    return () => {
      abortController.abort();
    };
  }, [debouncedQuery, maxResults, page, sortBy, onSearchResults, onSearchError]);

  /**
   * Handle input change
   */
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  /**
   * Handle form submission (optional - search is triggered by debounce)
   */
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Immediately trigger search on form submit (bypass debounce)
    if (query.trim()) {
      setDebouncedQuery(query.trim());
    }
  };

  /**
   * Clear search
   */
  const handleClear = () => {
    setQuery('');
    setDebouncedQuery('');
    onSearchResults(null);
  };

  return (
    <form onSubmit={handleSubmit} className="mb-12">
      <div className="relative max-w-3xl mx-auto">
        {/* Search Icon */}
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <svg 
            className="h-5 w-5 text-white/40" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" 
            />
          </svg>
        </div>

        {/* Search Input */}
        <input
          type="text"
          value={query}
          onChange={handleInputChange}
          className="modern-input block w-full pl-12 pr-24 py-4 text-lg"
          placeholder={placeholder}
          aria-label="Search products"
        />

        {/* Right Side Icons (Loading Spinner or Clear Button) */}
        <div className="absolute inset-y-0 right-0 pr-4 flex items-center space-x-2">
          {/* Loading Spinner */}
          {isSearching && (
            <div className="flex items-center" aria-live="polite" aria-busy="true">
              <svg 
                className="animate-spin h-5 w-5 text-white" 
                fill="none" 
                viewBox="0 0 24 24"
                aria-label="Searching"
              >
                <circle 
                  className="opacity-25" 
                  cx="12" 
                  cy="12" 
                  r="10" 
                  stroke="currentColor" 
                  strokeWidth="4"
                />
                <path 
                  className="opacity-75" 
                  fill="currentColor" 
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              <span className="ml-2 text-sm text-white/60">Searching...</span>
            </div>
          )}

          {/* Clear Button */}
          {!isSearching && query && (
            <button
              type="button"
              onClick={handleClear}
              className="text-white/40 hover:text-white/70 transition-fast"
              aria-label="Clear search"
            >
              <svg 
                className="h-5 w-5" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M6 18L18 6M6 6l12 12" 
                />
              </svg>
            </button>
          )}
        </div>
      </div>
    </form>
  );
}
