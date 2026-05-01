import { useState, useCallback, useEffect } from 'react'
import SearchBar from '../components/SearchBar'
import ProductCard from '../components/ProductCard'
import TrackPriceModal from '../components/TrackPriceModal'
import Navigation from '../components/Navigation'
import { ToastContainer, useToast } from '../components/Toast'
import { SearchResults, ProductResult } from '../types/product'
import { 
  trackProduct
} from '../services/trackingService'

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
  
  // Tracked products state
  const [trackedProducts, setTrackedProducts] = useState<TrackedProduct[]>([])
  const [isLoadingTracked, setIsLoadingTracked] = useState(true)
  const [updatingThresholdId, setUpdatingThresholdId] = useState<string | null>(null) // Changed from number to string
  const [deletingProductId, setDeletingProductId] = useState<string | null>(null) // Changed from number to string
  
  // Price history modal state
  const [selectedProductForHistory, setSelectedProductForHistory] = useState<TrackedProduct | null>(null)
  const [priceHistory, setPriceHistory] = useState<PriceHistoryEntry[]>([])
  const [isLoadingHistory, setIsLoadingHistory] = useState(false)

  // Track price modal state
  const [trackPriceModalOpen, setTrackPriceModalOpen] = useState(false)
  const [productToTrack, setProductToTrack] = useState<ProductResult | null>(null)

  // Load tracked products on component mount
  useEffect(() => {
    loadTrackedProducts()
  }, [])

  /**
   * Load tracked products from API
   */
  const loadTrackedProducts = async () => {
    try {
      setIsLoadingTracked(true)
      const products = await getTrackedProducts()
      setTrackedProducts(products)
    } catch (error) {
      console.error('Failed to load tracked products:', error)
      // Handle error silently for now - could show a toast notification
    } finally {
      setIsLoadingTracked(false)
    }
  }

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
      const trackedProduct = await trackProduct(product, threshold)
      
      // Add to tracked products list
      setTrackedProducts(prev => [trackedProduct, ...prev])
      
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

  /**
   * Handle threshold update
   */
  const handleUpdateThreshold = useCallback(async (productId: string, newThreshold: number) => { // Changed from number to string
    setUpdatingThresholdId(productId)
    
    try {
      const updatedProduct = await updateThreshold(productId, newThreshold)
      
      // Update the product in the list
      setTrackedProducts(prev => 
        prev.map(p => p.id === productId ? updatedProduct : p)
      )
      
      // Show success toast
      showSuccess(
        'Threshold Updated!',
        `Price alert updated to ${newThreshold.toFixed(2)} ${updatedProduct.currency}.`
      )
    } catch (error) {
      console.error('Failed to update threshold:', error)
      showError('Update Failed', 'Could not update price threshold. Please try again.')
      throw error // Re-throw to let the component handle the error
    } finally {
      setUpdatingThresholdId(null)
    }
  }, [showSuccess, showError])

  /**
   * Handle product deletion
   */
  const handleDeleteProduct = useCallback(async (productId: string) => { // Changed from number to string
    setDeletingProductId(productId)
    
    try {
      await deleteTrackedProduct(productId)
      
      // Remove from tracked products list
      setTrackedProducts(prev => prev.filter(p => p.id !== productId))
      
      // Show success toast
      showSuccess('Product Removed', 'Stopped tracking this product.')
    } catch (error) {
      console.error('Failed to delete product:', error)
      showError('Delete Failed', 'Could not remove product. Please try again.')
      throw error // Re-throw to let the component handle the error
    } finally {
      setDeletingProductId(null)
    }
  }, [showSuccess, showError])

  /**
   * Handle view price history
   */
  const handleViewHistory = useCallback(async (productId: string) => { // Changed from number to string
    const product = trackedProducts.find(p => p.id === productId)
    if (!product) return
    
    setSelectedProductForHistory(product)
    setIsLoadingHistory(true)
    
    try {
      const history = await getPriceHistory(productId)
      setPriceHistory(history)
    } catch (error) {
      console.error('Failed to load price history:', error)
      setPriceHistory([])
    } finally {
      setIsLoadingHistory(false)
    }
  }, [trackedProducts])

  /**
   * Close price history modal
   */
  const closePriceHistoryModal = useCallback(() => {
    setSelectedProductForHistory(null)
    setPriceHistory([])
  }, [])

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <svg className="w-8 h-8 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span className="ml-2 text-xl font-bold text-neutral-900">PriceTracker</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button className="text-neutral-600 hover:text-neutral-900 transition-fast">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </button>
              <div className="relative">
                <button className="flex items-center space-x-2 text-neutral-700 hover:text-neutral-900 transition-fast">
                  <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                    <span className="text-sm font-semibold text-primary-600">U</span>
                  </div>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-neutral-900 mb-2">Track Your Favorite Products</h1>
          <p className="text-neutral-600">Search products and get notified when prices drop</p>
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

        {/* Tracked Products */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-neutral-900">
              Your Tracked Products ({trackedProducts.length})
            </h2>
            {trackedProducts.length > 0 && (
              <button
                onClick={loadTrackedProducts}
                disabled={isLoadingTracked}
                className="px-4 py-2 text-sm font-medium text-primary-600 bg-primary-50 rounded-lg hover:bg-primary-100 transition-fast disabled:opacity-50"
              >
                {isLoadingTracked ? 'Refreshing...' : 'Refresh'}
              </button>
            )}
          </div>

          {/* Loading State */}
          {isLoadingTracked ? (
            <div className="flex items-center justify-center py-12">
              <div className="flex items-center space-x-2 text-neutral-500">
                <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                </svg>
                <span>Loading tracked products...</span>
              </div>
            </div>
          ) : trackedProducts.length === 0 ? (
            /* Empty State */
            <div className="text-center py-12">
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
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" 
                />
              </svg>
              <h3 className="text-xl font-semibold text-neutral-900 mb-2">No Tracked Products</h3>
              <p className="text-neutral-600 max-w-md mx-auto mb-4">
                Start tracking products by searching above and clicking the "Track" button on products you're interested in.
              </p>
            </div>
          ) : (
            /* Tracked Products List */
            <div className="space-y-6">
              {trackedProducts.map((product) => (
                <TrackedProductCard
                  key={product.id}
                  product={product}
                  onUpdateThreshold={handleUpdateThreshold}
                  onDelete={handleDeleteProduct}
                  onViewHistory={handleViewHistory}
                  isUpdatingThreshold={updatingThresholdId === product.id}
                  isDeleting={deletingProductId === product.id}
                />
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Price History Modal */}
      {selectedProductForHistory && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-6 border-b border-neutral-200">
              <div>
                <h2 className="text-xl font-semibold text-neutral-900">Price History</h2>
                <p className="text-neutral-600 mt-1">{selectedProductForHistory.product_name}</p>
              </div>
              <button
                onClick={closePriceHistoryModal}
                className="text-neutral-400 hover:text-neutral-600 transition-fast"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              <PriceChart
                priceHistory={priceHistory}
                thresholdPrice={typeof selectedProductForHistory.price_threshold === 'string' ? parseFloat(selectedProductForHistory.price_threshold) : selectedProductForHistory.price_threshold}
                currency={selectedProductForHistory.currency}
                height={400}
                isLoading={isLoadingHistory}
                productName={selectedProductForHistory.product_name}
              />
            </div>
          </div>
        </div>
      )}

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