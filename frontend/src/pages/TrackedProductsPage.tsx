/**
 * TrackedProductsPage Component
 * 
 * A dedicated page for managing tracked products.
 * 
 * Features:
 * - List all tracked products
 * - Edit price thresholds
 * - Delete tracked products
 * - View price history
 * - Filter and sort options
 * - Bulk actions
 * - Statistics overview
 */

import { useState, useCallback, useEffect } from 'react'
import TrackedProductCard from '../components/TrackedProductCard'
import PriceChart from '../components/PriceChart'
import { ToastContainer, useToast } from '../components/Toast'
import { 
  TrackedProduct, 
  getTrackedProducts, 
  updateThreshold, 
  deleteTrackedProduct,
  getPriceHistory,
  PriceHistoryEntry,
  startAutoPriceRandomization
} from '../services/trackingService'

export default function TrackedProductsPage() {
  // Tracked products state
  const [trackedProducts, setTrackedProducts] = useState<TrackedProduct[]>([])
  const [isLoadingTracked, setIsLoadingTracked] = useState(true)
  const [updatingThresholdId, setUpdatingThresholdId] = useState<string | null>(null)
  const [deletingProductId, setDeletingProductId] = useState<string | null>(null)
  
  // Auto-randomization state
  const [nextUpdateTime, setNextUpdateTime] = useState<Date | null>(null)
  const [timeUntilUpdate, setTimeUntilUpdate] = useState<string>('')
  
  // Filter and sort state
  const [filterPlatform, setFilterPlatform] = useState<string>('all')
  const [sortBy, setSortBy] = useState<string>('created_at')
  const [searchQuery, setSearchQuery] = useState('')
  
  // Price history modal state
  const [selectedProductForHistory, setSelectedProductForHistory] = useState<TrackedProduct | null>(null)
  const [priceHistory, setPriceHistory] = useState<PriceHistoryEntry[]>([])
  const [isLoadingHistory, setIsLoadingHistory] = useState(false)
  
  // Toast notifications
  const { toasts, dismissToast, showSuccess, showError } = useToast()

  // Load tracked products on component mount
  useEffect(() => {
    loadTrackedProducts()
  }, [])

  // Start auto price randomization (only once on mount)
  useEffect(() => {
    console.log('Setting up auto price randomization...');
    
    // Set next update time (1 hour from now)
    const nextUpdate = new Date(Date.now() + 3600000); // 1 hour
    setNextUpdateTime(nextUpdate);
    
    const cleanup = startAutoPriceRandomization(
      () => trackedProducts, // Pass function to get current products
      (productId, newPrice, thresholdTriggered) => {
        console.log('Price change callback:', { productId, newPrice, thresholdTriggered });
        
        // Update the product price in the list and show notification
        setTrackedProducts(prev => {
          const updatedProducts = prev.map(p => 
            p.id === productId ? { ...p, current_price: newPrice } : p
          );
          
          // Show notification if threshold was triggered
          if (thresholdTriggered) {
            const product = updatedProducts.find(p => p.id === productId);
            console.log('Threshold triggered! Product:', product);
            if (product) {
              showSuccess(
                '🎉 Price Alert!',
                `${product.product_name} dropped below your target price!`
              );
            }
          }
          
          return updatedProducts;
        });
        
        // Update next update time
        const nextUpdate = new Date(Date.now() + 3600000);
        setNextUpdateTime(nextUpdate);
      }
    );
    
    // Cleanup on unmount
    return cleanup;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Empty array - only run once on mount
  
  // Update countdown timer
  useEffect(() => {
    if (!nextUpdateTime) return;
    
    const updateCountdown = () => {
      const now = Date.now();
      const diff = nextUpdateTime.getTime() - now;
      
      if (diff <= 0) {
        setTimeUntilUpdate('Updating...');
        return;
      }
      
      const hours = Math.floor(diff / 3600000);
      const minutes = Math.floor((diff % 3600000) / 60000);
      const seconds = Math.floor((diff % 60000) / 1000);
      
      if (hours > 0) {
        setTimeUntilUpdate(`${hours}h ${minutes}m`);
      } else if (minutes > 0) {
        setTimeUntilUpdate(`${minutes}m ${seconds}s`);
      } else {
        setTimeUntilUpdate(`${seconds}s`);
      }
    };
    
    updateCountdown();
    const interval = setInterval(updateCountdown, 1000);
    
    return () => clearInterval(interval);
  }, [nextUpdateTime]);

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
      showError('Load Failed', 'Could not load tracked products. Please try again.')
    } finally {
      setIsLoadingTracked(false)
    }
  }

  /**
   * Handle threshold update
   */
  const handleUpdateThreshold = useCallback(async (productId: string, newThreshold: number) => {
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
      throw error
    } finally {
      setUpdatingThresholdId(null)
    }
  }, [showSuccess, showError])

  /**
   * Handle product deletion
   */
  const handleDeleteProduct = useCallback(async (productId: string) => {
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
      throw error
    } finally {
      setDeletingProductId(null)
    }
  }, [showSuccess, showError])

  /**
   * Handle price randomization
   */
  const handlePriceRandomized = useCallback((productId: string, newPrice: number) => {
    // Update the product in the list with the new price
    setTrackedProducts(prev =>
      prev.map(p => p.id === productId ? { ...p, current_price: newPrice } : p)
    );
    
    // Note: We don't reload from API since this is mock data for testing
    // The price change is stored in localStorage and will persist
  }, []);

  /**
   * Handle view price history
   */
  const handleViewHistory = useCallback(async (productId: string) => {
    const product = trackedProducts.find(p => p.id === productId)
    if (!product) return
    
    setSelectedProductForHistory(product)
    setIsLoadingHistory(true)
    
    try {
      // Pass the current price to generate realistic mock data
      const currentPrice = typeof product.current_price === 'string' 
        ? parseFloat(product.current_price) 
        : product.current_price;
      
      const history = await getPriceHistory(productId, currentPrice)
      setPriceHistory(history)
    } catch (error) {
      console.error('Failed to load price history:', error)
      setPriceHistory([])
      showError('History Failed', 'Could not load price history.')
    } finally {
      setIsLoadingHistory(false)
    }
  }, [trackedProducts, showError])

  /**
   * Close price history modal
   */
  const closePriceHistoryModal = useCallback(() => {
    setSelectedProductForHistory(null)
    setPriceHistory([])
  }, [])

  /**
   * Filter and sort products
   */
  const filteredAndSortedProducts = trackedProducts
    .filter(product => {
      // Platform filter
      if (filterPlatform !== 'all' && product.platform !== filterPlatform) {
        return false
      }
      
      // Search filter
      if (searchQuery && !product.product_name.toLowerCase().includes(searchQuery.toLowerCase())) {
        return false
      }
      
      return true
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.product_name.localeCompare(b.product_name)
        case 'platform':
          return a.platform.localeCompare(b.platform)
        case 'price':
          const priceA = typeof a.current_price === 'string' ? parseFloat(a.current_price) : a.current_price
          const priceB = typeof b.current_price === 'string' ? parseFloat(b.current_price) : b.current_price
          return priceA - priceB
        case 'threshold':
          const thresholdA = typeof a.price_threshold === 'string' ? parseFloat(a.price_threshold) : a.price_threshold
          const thresholdB = typeof b.price_threshold === 'string' ? parseFloat(b.price_threshold) : b.price_threshold
          return thresholdA - thresholdB
        case 'created_at':
        default:
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      }
    })

  /**
   * Get statistics
   */
  const stats = {
    total: trackedProducts.length,
    belowThreshold: trackedProducts.filter(p => {
      const currentPrice = typeof p.current_price === 'string' ? parseFloat(p.current_price) : p.current_price
      const threshold = typeof p.price_threshold === 'string' ? parseFloat(p.price_threshold) : p.price_threshold
      return currentPrice <= threshold
    }).length,
    platforms: [...new Set(trackedProducts.map(p => p.platform))].length
  }

  return (
    <div className="min-h-screen bg-transparent">
      {/* Header */}
      <div className="border-b border-white/10 backdrop-blur-xl bg-black/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              {/* Back Button */}
              <a
                href="/dashboard"
                className="w-9 h-9 rounded-lg hover:bg-white/10 flex items-center justify-center transition-colors group"
                title="Back to Dashboard"
              >
                <svg className="w-5 h-5 text-white/60 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </a>
              
              <div>
                <h1 className="text-3xl font-bold text-white">Tracked Products</h1>
                <p className="text-white/50 mt-1">Manage your price alerts and monitoring</p>
                {timeUntilUpdate && (
                  <p className="text-sm text-purple-400 mt-1">
                    ⏱️ Next auto price update in: {timeUntilUpdate}
                  </p>
                )}
              </div>
            </div>
            
            <button
              onClick={loadTrackedProducts}
              disabled={isLoadingTracked}
              className="modern-button flex items-center space-x-2"
            >
              <svg className={`w-4 h-4 ${isLoadingTracked ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>{isLoadingTracked ? 'Refreshing...' : 'Refresh'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="modern-card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-500/20 rounded-lg">
                <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-white/60">Total Products</p>
                <p className="text-2xl font-bold text-white">{stats.total}</p>
              </div>
            </div>
          </div>

          <div className="modern-card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-500/20 rounded-lg">
                <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-white/60">Below Target</p>
                <p className="text-2xl font-bold text-green-400">{stats.belowThreshold}</p>
              </div>
            </div>
          </div>

          <div className="modern-card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-500/20 rounded-lg">
                <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-white/60">Platforms</p>
                <p className="text-2xl font-bold text-purple-400">{stats.platforms}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="modern-card p-6 mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0 md:space-x-4">
            {/* Search */}
            <div className="flex-1 max-w-md">
              <div className="relative">
                <svg className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  type="text"
                  placeholder="Search products..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="modern-input w-full pl-10 pr-4 py-2"
                />
              </div>
            </div>

            {/* Filters */}
            <div className="flex items-center space-x-4">
              <select
                value={filterPlatform}
                onChange={(e) => setFilterPlatform(e.target.value)}
                className="modern-input px-3 py-2"
              >
                <option value="all">All Platforms</option>
                <option value="lazada">Lazada</option>
                <option value="shopee">Shopee</option>
                <option value="tiktokshop">TikTok Shop</option>
              </select>

              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="modern-input px-3 py-2"
              >
                <option value="created_at">Newest First</option>
                <option value="name">Product Name</option>
                <option value="platform">Platform</option>
                <option value="price">Current Price</option>
                <option value="threshold">Target Price</option>
              </select>
            </div>
          </div>
        </div>

        {/* Products List */}
        {isLoadingTracked ? (
          <div className="flex items-center justify-center py-12">
            <div className="flex items-center space-x-2 text-white/50">
              <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              <span>Loading tracked products...</span>
            </div>
          </div>
        ) : filteredAndSortedProducts.length === 0 ? (
          <div className="text-center py-12">
            <svg 
              className="mx-auto h-16 w-16 text-white/20 mb-4" 
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
            <h3 className="text-xl font-semibold text-white mb-2">
              {trackedProducts.length === 0 ? 'No Tracked Products' : 'No Products Match Your Filters'}
            </h3>
            <p className="text-white/50 max-w-md mx-auto mb-4">
              {trackedProducts.length === 0 
                ? 'Start tracking products by searching and clicking the "Track" button on products you\'re interested in.'
                : 'Try adjusting your search or filter criteria to find the products you\'re looking for.'
              }
            </p>
            {trackedProducts.length === 0 && (
              <a
                href="/"
                className="modern-button inline-flex items-center"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Search Products
              </a>
            )}
          </div>
        ) : (
          <div className="space-y-6">
            {filteredAndSortedProducts.map((product) => (
              <TrackedProductCard
                key={product.id}
                product={product}
                onUpdateThreshold={handleUpdateThreshold}
                onDelete={handleDeleteProduct}
                onViewHistory={handleViewHistory}
                onPriceRandomized={handlePriceRandomized}
                isUpdatingThreshold={updatingThresholdId === product.id}
                isDeleting={deletingProductId === product.id}
              />
            ))}
          </div>
        )}
      </div>

      {/* Price History Modal */}
      {selectedProductForHistory && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="modern-card max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-6 border-b border-white/10">
              <div>
                <h2 className="text-xl font-semibold text-white">Price History</h2>
                <p className="text-white/60 mt-1">{selectedProductForHistory.product_name}</p>
              </div>
              <button
                onClick={closePriceHistoryModal}
                className="text-white/40 hover:text-white/70 transition-fast"
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

      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} onDismiss={dismissToast} />
    </div>
  )
}