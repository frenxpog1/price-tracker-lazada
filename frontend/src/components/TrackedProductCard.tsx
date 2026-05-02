/**
 * TrackedProductCard Component
 * 
 * Displays a tracked product with current price, threshold, and controls.
 * 
 * Features:
 * - Product information display (name, platform, clickable image)
 * - Current price vs threshold comparison
 * - Price drop indicator
 * - Edit threshold functionality
 * - Delete product functionality
 * - Price history chart placeholder
 * - Responsive design with Tailwind CSS
 * 
 * Requirements: 2.4, 2.5, 8.1
 */

import { useState } from 'react';
import { TrackedProduct } from '../services/trackingService';
import ImageModal from './ImageModal';

/**
 * Local placeholder image as SVG data URI
 * This avoids relying on external services like via.placeholder.com
 */
const PLACEHOLDER_IMAGE = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80"%3E%3Crect fill="%23f3f4f6" width="80" height="80"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="12" fill="%239ca3af"%3ENo Image%3C/text%3E%3C/svg%3E';

interface TrackedProductCardProps {
  /**
   * The tracked product to display
   */
  product: TrackedProduct;
  
  /**
   * Callback when threshold is updated
   */
  onUpdateThreshold?: (productId: string, newThreshold: number) => Promise<void>; // Changed from number to string
  
  /**
   * Callback when product is deleted
   */
  onDelete?: (productId: string) => Promise<void>; // Changed from number to string
  
  /**
   * Callback when price history is requested
   */
  onViewHistory?: (productId: string) => void; // Changed from number to string
  
  /**
   * Whether threshold update is in progress
   */
  isUpdatingThreshold?: boolean;
  
  /**
   * Whether deletion is in progress
   */
  isDeleting?: boolean;
}

/**
 * Format price with currency symbol
 */
function formatPrice(price: number | string | null | undefined, currency: string = 'USD'): string {
  const currencySymbols: { [key: string]: string } = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
    'SGD': 'S$',
    'PHP': '₱',
    'MYR': 'RM',
    'THB': '฿',
  };
  
  // Handle null, undefined, or invalid values
  if (price === null || price === undefined) {
    return `${currencySymbols[currency] || currency} --`;
  }
  
  // Convert to number if it's a string
  const numPrice = typeof price === 'string' ? parseFloat(price) : price;
  
  // Handle invalid numbers
  if (isNaN(numPrice)) {
    return `${currencySymbols[currency] || currency} --`;
  }
  
  const symbol = currencySymbols[currency] || currency;
  return `${symbol}${numPrice.toFixed(2)}`;
}

/**
 * Get platform badge color
 */
function getPlatformBadgeColor(platform: string): string {
  const colors: { [key: string]: string } = {
    'lazada': 'bg-orange-100 text-orange-800',
    'shopee': 'bg-red-100 text-red-800',
    'tiktokshop': 'bg-purple-100 text-purple-800',
  };
  
  return colors[platform.toLowerCase()] || 'bg-neutral-100 text-neutral-800';
}

export default function TrackedProductCard({
  product,
  onUpdateThreshold,
  onDelete,
  onViewHistory,
  isUpdatingThreshold = false,
  isDeleting = false,
}: TrackedProductCardProps) {
  const [isEditingThreshold, setIsEditingThreshold] = useState(false);
  const thresholdValue = typeof product.price_threshold === 'string' ? product.price_threshold : product.price_threshold.toString();
  const [newThreshold, setNewThreshold] = useState(thresholdValue);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [isImageModalOpen, setIsImageModalOpen] = useState(false);

  // Calculate if price is below threshold
  const currentPriceNum = typeof product.current_price === 'string' ? parseFloat(product.current_price) : product.current_price;
  const thresholdNum = typeof product.price_threshold === 'string' ? parseFloat(product.price_threshold) : product.price_threshold;
  
  const isBelowThreshold = currentPriceNum <= thresholdNum;
  const priceDifference = currentPriceNum - thresholdNum;

  /**
   * Handle threshold update
   */
  const handleUpdateThreshold = async () => {
    const threshold = parseFloat(newThreshold);
    
    if (isNaN(threshold) || threshold <= 0) {
      alert('Please enter a valid price threshold');
      return;
    }
    
    if (onUpdateThreshold) {
      try {
        await onUpdateThreshold(product.id, threshold);
        setIsEditingThreshold(false);
      } catch (error) {
        console.error('Failed to update threshold:', error);
        alert('Failed to update threshold. Please try again.');
      }
    }
  };

  /**
   * Handle product deletion
   */
  const handleDelete = async () => {
    if (onDelete) {
      try {
        await onDelete(product.id);
      } catch (error) {
        console.error('Failed to delete product:', error);
        alert('Failed to delete product. Please try again.');
      }
    }
    setShowDeleteConfirm(false);
  };

  /**
   * Cancel threshold editing
   */
  const handleCancelEdit = () => {
    const thresholdValue = typeof product.price_threshold === 'string' ? product.price_threshold : product.price_threshold.toString();
    setNewThreshold(thresholdValue);
    setIsEditingThreshold(false);
  };

  /**
   * Handle image click - open in modal
   */
  const handleImageClick = () => {
    if (product.image_url && product.image_url !== PLACEHOLDER_IMAGE) {
      setIsImageModalOpen(true);
    }
  };

  /**
   * Close image modal
   */
  const closeImageModal = () => {
    setIsImageModalOpen(false);
  };

  return (
    <div className="modern-card overflow-hidden">
      {/* Product Header */}
      <div className="p-6">
        <div className="flex items-start space-x-4">
          {/* Product Image */}
          <div className="flex-shrink-0">
            {product.image_url ? (
              <div className="relative group">
                <img
                  src={product.image_url}
                  alt={product.product_name}
                  onClick={handleImageClick}
                  className="w-20 h-20 rounded-lg object-cover cursor-pointer transition-transform duration-200 group-hover:scale-105"
                  onError={(e) => {
                    // Fallback to placeholder if image fails to load
                    e.currentTarget.src = PLACEHOLDER_IMAGE;
                  }}
                  title="Click to view full size image"
                />
                {/* Hover overlay */}
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-200 flex items-center justify-center opacity-0 group-hover:opacity-100 rounded-lg">
                  <svg 
                    className="w-6 h-6 text-white drop-shadow-lg" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      strokeWidth={2} 
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" 
                    />
                  </svg>
                </div>
              </div>
            ) : (
              <div className="w-20 h-20 rounded-lg bg-neutral-100 flex items-center justify-center">
                <svg className="w-8 h-8 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            )}
          </div>

          {/* Product Info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between mb-2">
              <div className="flex-1 min-w-0">
                <h3 className="text-lg font-semibold text-white mb-1 line-clamp-2">
                  {product.product_name}
                </h3>
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPlatformBadgeColor(product.platform)}`}>
                  {product.platform}
                </span>
              </div>
              
              {/* Actions Menu */}
              <div className="flex items-center space-x-2 ml-4">
                <button
                  onClick={() => onViewHistory?.(product.id)}
                  className="text-white/40 hover:text-white/70 transition-fast"
                  title="View price history"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </button>
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  disabled={isDeleting}
                  className="text-white/40 hover:text-red-400 transition-fast disabled:opacity-50"
                  title="Delete tracked product"
                >
                  {isDeleting ? (
                    <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                    </svg>
                  ) : (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {/* Availability Status */}
            {product.is_available === false && (
              <div className="mb-3">
                <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-warning-100 text-warning-800">
                  <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  Currently Unavailable
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Price Information */}
        <div className="mt-4 grid grid-cols-3 gap-4">
          {/* Current Price */}
          <div>
            <p className="text-sm text-white/50 mb-1">Current Price</p>
            <p className="text-2xl font-bold text-white">
              {formatPrice(product.current_price, product.currency)}
            </p>
          </div>

          {/* Target Price */}
          <div>
            <p className="text-sm text-white/50 mb-1">Target Price</p>
            {isEditingThreshold ? (
              <div className="flex items-center space-x-2">
                <input
                  type="number"
                  value={newThreshold}
                  onChange={(e) => setNewThreshold(e.target.value)}
                  className="w-20 px-2 py-1 text-sm modern-input"
                  step="0.01"
                  min="0"
                />
                <button
                  onClick={handleUpdateThreshold}
                  disabled={isUpdatingThreshold}
                  className="text-green-400 hover:text-green-300 disabled:opacity-50"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </button>
                <button
                  onClick={handleCancelEdit}
                  className="text-white/40 hover:text-white/70"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <p className="text-2xl font-bold text-white">
                  {formatPrice(product.price_threshold, product.currency)}
                </p>
                <button
                  onClick={() => setIsEditingThreshold(true)}
                  className="text-white/40 hover:text-white transition-fast"
                  title="Edit threshold"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
              </div>
            )}
          </div>

          {/* Status */}
          <div>
            <p className="text-sm text-white/50 mb-1">Status</p>
            {isBelowThreshold ? (
              <div className="flex items-center">
                <span className="inline-flex items-center text-green-400 font-semibold">
                  <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                  Below target!
                </span>
                {product.price_drop_detected && (
                  <span className="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-success-100 text-success-800">
                    New Drop
                  </span>
                )}
              </div>
            ) : (
              <span className="inline-flex items-center text-yellow-400 font-semibold">
                <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                </svg>
                {formatPrice(Math.abs(priceDifference), product.currency)} above
              </span>
            )}
          </div>
        </div>

        {/* Last Checked */}
        {product.last_checked && (
          <div className="mt-4 text-sm text-white/40">
            Last checked: {new Date(product.last_checked).toLocaleString()}
          </div>
        )}
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="modern-card p-6 max-w-sm mx-4">
            <h3 className="text-lg font-semibold text-white mb-2">Delete Tracked Product</h3>
            <p className="text-white/60 mb-4">
              Are you sure you want to stop tracking "{product.product_name}"? This action cannot be undone.
            </p>
            <div className="flex space-x-3">
              <button
                onClick={handleDelete}
                disabled={isDeleting}
                className="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50 transition-fast"
              >
                {isDeleting ? 'Deleting...' : 'Delete'}
              </button>
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="flex-1 px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-fast"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Image Modal */}
      <ImageModal
        imageUrl={product.image_url || PLACEHOLDER_IMAGE}
        altText={product.product_name}
        isOpen={isImageModalOpen}
        onClose={closeImageModal}
        productName={product.product_name}
      />
    </div>
  );
}