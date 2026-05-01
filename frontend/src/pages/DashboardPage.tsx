import { useState, useCallback } from 'react'
import SearchBar from '../components/SearchBar'
import ProductCard from '../components/ProductCard'
import TrackPriceModal from '../components/TrackPriceModal'
import Navigation from '../components/Navigation'
import { ToastContainer, useToast } from '../components/Toast'
import { SearchResults, ProductResult } from '../types/product'
import { trackProduct } from '../services/trackingService'

export default function DashboardPage() {
  const [searchResults, setSearchResults] = useState<SearchResults | null>(null)
  const [searchError, setSearchError] = useState<string | null>(null)
  const [trackingProductId, setTrackingProductId] = useState<string | null>(null)
  
  // Toast notifications
  const { toasts, dismissToast, showSuccess, showError } = useToast()
  
  // Pagination and sorting
  const [currentPage, setCurrentPage] = useState(1)
  const [sortBy, setSortBy] = useState('best_match')
  const [searchQuery, setSearchQuery] = useState('')
  
  // Track price modal state
  const [trackPriceModalOpen, setTrackPriceModalOpen] = useState(false)
  const [productToTrack, setProductToTrack] = useState<ProductResult | null>(null)

  /**
   * Handle new search query - reset to page 1
   */
  const handleNewSearch = useCallback(() => {
    setCurrentPage(1)
  }, [])

  /**
   * Handle search results from SearchBar component
   * Use useCallback to prevent unnecessary re-renders
   */
  const handleSearchResults = useCallback((results: SearchResults | null) => {
    setSearchResults(results)
    setSearchError(null)
    if (results) {
      setSearchQuery(results.query)
      // Don't reset page when results come in - page is controlled by pagination buttons
    }
  }, [])

  /**
   * Handle sort change - reset to page 1
   */
  const handleSortChange = (newSortBy: string) => {
    setSortBy(newSortBy)
    setCurrentPage(1)
  }

  /**
   * Handle page change
   */
  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage)
    // Scroll to top when page changes
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  /**
   * Handle search errors from SearchBar component
   * Use useCallback to prevent unnecessary re-renders
   */
  const handleSearchError = useCallback((error: string) => {
    setSearchError(error)
    setSearchResults(null)
  }, [])

  /**
   * Handle track product action
   * Now opens a beautiful modal instead of using prompt
   */
  const handleTrackProduct = useCallback(async (product: ProductResult) => {
    setProductToTrack(product)
    setTrackPriceModalOpen(true)
  }, [])

  /**
   * Handle track price confirmation from modal
   */
  const handleTrackPriceConfirm = useCallback(async (product: ProductResult, threshold: number) => {
    setTrackingProductId(product.product_url)
    
    try {
      // Track the product
      await trackProduct(product, threshold)
      
      // Close modal and show success
      setTrackPriceModalOpen(false)
      setProductToTrack(null)
      
      // Show success toast
      showSuccess(
        'Product Tracking Started!',
        `You'll be notified when "${product.product_name}" drops to ${threshold.toFixed(2)} ${product.currency} or below.`
      )
      
    } catch (error: any) {
      console.error('Failed to track product:', error)
      
      let errorTitle = 'Failed to Track Product'
      let errorMessage = 'Please try again.'
      
      if (error.response?.status === 409) {
        errorTitle = 'Already Tracking'
        errorMessage = 'This product is already being tracked.'
      } else if (error.response?.status === 401) {
        errorTitle = 'Session Expired'
        errorMessage = 'Please log in again.'
      }
      
      showError(errorTitle, errorMessage)
      throw error // Re-throw to let modal handle the error state
    } finally {
      setTrackingProductId(null)
    }
  }, [showSuccess, showError])

  /**
   * Close track price modal
   */
  const closeTrackPriceModal = useCallback(() => {
    if (trackingProductId) return // Don't close while tracking is in progress
    setTrackPriceModalOpen(false)
    setProductToTrack(null)
  }, [trackingProductId])

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Navigation */}
      <Navigation />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-neutral-900 mb-2">Search Products</h1>
          <p className="text-neutral-600">Find products and set up price alerts across multiple platforms</p>
        </div>

        {/* Search Bar - Requirements: 1.1, 1.2, 1.3 */}
        <SearchBar
          onSearchResults={handleSearchResults}
          onSearchError={handleSearchError}
          onNewSearch={handleNewSearch}
          placeholder="Search products across Lazada, Shopee, TikTok Shop..."
          maxResults={40}
          page={currentPage}
          sortBy={sortBy}
        />

        {/* Search Error Message */}
        {searchError && (
          <div className="mb-8 p-4 bg-error-50 border border-error-200 rounded-xl">
            <div className="flex items-start">
              <svg 
                className="w-5 h-5 text-error-500 mt-0.5 mr-3 flex-shrink-0" 
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
              <div>
                <h3 className="text-sm font-semibold text-error-800 mb-1">Search Error</h3>
                <p className="text-sm text-error-700">{searchError}</p>
              </div>
            </div>
          </div>
        )}

        {/* Platform Warnings - Requirement: 9.1 */}
        {searchResults && searchResults.platforms_failed.length > 0 && (
          <div className="mb-8 p-4 bg-warning-50 border border-warning-200 rounded-xl">
            <div className="flex items-start">
              <svg 
                className="w-5 h-5 text-warning-500 mt-0.5 mr-3 flex-shrink-0" 
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
                <h3 className="text-sm font-semibold text-warning-800 mb-1">Platform Warning</h3>
                <p className="text-sm text-warning-700">
                  Some platforms were unavailable: {searchResults.platforms_failed.join(', ')}. 
                  Results shown are from available platforms only.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Empty Results Message - Requirement: 1.6 */}
        {searchResults && searchResults.results.length === 0 && (
          <div className="mb-12 text-center py-12">
            <svg 
              className="mx-auto h-16 w-16 text-neutral-400 mb-4" 
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
            <h3 className="text-xl font-semibold text-neutral-900 mb-2">No Products Found</h3>
            <p className="text-neutral-600 max-w-md mx-auto">
              We couldn't find any products matching your search. Try different keywords or check back later.
            </p>
          </div>
        )}

        {/* Search Results - Requirement: 1.5 */}
        {searchResults && searchResults.results.length > 0 && (
          <div className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-neutral-900">
                Search Results ({searchResults.total_results})
              </h2>
              <p className="text-sm text-neutral-600">
                Found in {searchResults.search_time_seconds.toFixed(2)}s
              </p>
            </div>

            {/* Simple Pagination and Sort Controls */}
            {searchQuery && (
              <div className="flex items-center justify-between mb-6 p-4 bg-white rounded-xl border border-neutral-200">
                <div className="flex items-center space-x-3">
                  <label className="text-sm font-medium text-neutral-700">Sort:</label>
                  <select
                    value={sortBy}
                    onChange={(e) => handleSortChange(e.target.value)}
                    className="px-3 py-2 border border-neutral-300 rounded-lg text-sm"
                  >
                    <option value="best_match">Best Match</option>
                    <option value="price_asc">Price: Low to High</option>
                    <option value="price_desc">Price: High to Low</option>
                  </select>
                </div>
                
                <div className="flex items-center space-x-3">
                  <button
                    onClick={() => handlePageChange(Math.max(1, currentPage - 1))}
                    disabled={currentPage === 1}
                    className="px-4 py-2 text-sm font-medium text-neutral-700 bg-white border border-neutral-300 rounded-lg hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed transition-fast"
                  >
                    ← Previous
                  </button>
                  <span className="text-sm text-neutral-600">Page {currentPage}</span>
                  <button
                    onClick={() => handlePageChange(currentPage + 1)}
                    className="px-4 py-2 text-sm font-medium text-neutral-700 bg-white border border-neutral-300 rounded-lg hover:bg-neutral-50 transition-fast"
                  >
                    Next →
                  </button>
                </div>
              </div>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {searchResults.results.map((product) => (
                <ProductCard
                  key={`${product.platform}-${product.product_url}`}
                  product={product}
                  onTrack={handleTrackProduct}
                  isTracking={trackingProductId === product.product_url}
                />
              ))}
            </div>
          </div>
        )}

        {/* Call to Action for Tracked Products */}
        {!searchResults && (
          <div className="text-center py-12">
            <div className="max-w-md mx-auto">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-neutral-900 mb-2">Start Searching</h3>
              <p className="text-neutral-600 mb-6">
                Search for products across multiple e-commerce platforms and set up price alerts to get notified when prices drop.
              </p>
              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <a
                  href="/tracked"
                  className="inline-flex items-center px-4 py-2 bg-neutral-100 text-neutral-700 rounded-lg hover:bg-neutral-200 transition-colors"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  View Tracked Products
                </a>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Track Price Modal */}
      <TrackPriceModal
        product={productToTrack}
        isOpen={trackPriceModalOpen}
        onClose={closeTrackPriceModal}
        onConfirm={handleTrackPriceConfirm}
        isTracking={trackingProductId === productToTrack?.product_url}
      />

      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} onDismiss={dismissToast} />
    </div>
  )
}