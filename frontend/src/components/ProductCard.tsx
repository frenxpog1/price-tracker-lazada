/**
 * ProductCard Component
 * 
 * Displays individual product information from search results.
 * 
 * Features:
 * - Product image display with clickable modal
 * - Product name with line clamping
 * - Current price and currency
 * - Platform badge (Lazada, Shopee, TikTok Shop)
 * - Availability status indicator
 * - "Track This Product" button
 * - Hover effects and animations
 * - Responsive design with Tailwind CSS
 * 
 * Requirements: 1.5
 */

import { useState } from 'react';
import { ProductResult } from '../types/product';
import ImageModal from './ImageModal';

/**
 * Local placeholder image as SVG data URI
 * This avoids relying on external services like via.placeholder.com
 */
const PLACEHOLDER_IMAGE = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300"%3E%3Crect fill="%23f3f4f6" width="300" height="300"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="18" fill="%239ca3af"%3ENo Image%3C/text%3E%3C/svg%3E';

interface ProductCardProps {
  /**
   * Product data to display
   */
  product: ProductResult;
  
  /**
   * Callback function when "Track" button is clicked
   */
  onTrack: (product: ProductResult) => void;
  
  /**
   * Whether the track button is disabled (e.g., during API call)
   */
  isTracking?: boolean;
}

/**
 * Get platform-specific badge color
 */
const getPlatformBadgeColor = (platform: string): string => {
  const platformLower = platform.toLowerCase();
  
  if (platformLower.includes('lazada')) {
    return 'bg-blue-100 text-blue-800';
  } else if (platformLower.includes('shopee')) {
    return 'bg-orange-100 text-orange-800';
  } else if (platformLower.includes('tiktok')) {
    return 'bg-pink-100 text-pink-800';
  }
  
  // Default color for unknown platforms
  return 'bg-primary-100 text-primary-800';
};

/**
 * Format price with currency
 */
const formatPrice = (price: number | string, currency: string): string => {
  // Convert price to number if it's a string
  const numPrice = typeof price === 'string' ? parseFloat(price) : price;
  
  // Handle invalid numbers
  if (isNaN(numPrice)) {
    return `${currency} --`;
  }
  
  // Handle different currency formats
  if (currency === 'PHP' || currency === '₱') {
    return `₱${numPrice.toFixed(2)}`;
  } else if (currency === 'USD' || currency === '$') {
    return `$${numPrice.toFixed(2)}`;
  }
  
  // Default format
  return `${currency} ${numPrice.toFixed(2)}`;
};

export default function ProductCard({ 
  product, 
  onTrack, 
  isTracking = false 
}: ProductCardProps) {
  const [isImageModalOpen, setIsImageModalOpen] = useState(false);

  /**
   * Handle track button click
   */
  const handleTrackClick = () => {
    if (!isTracking) {
      onTrack(product);
    }
  };

  /**
   * Handle image error (fallback to placeholder)
   */
  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    e.currentTarget.src = PLACEHOLDER_IMAGE;
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
   * Handle product name/card click - go to product page
   */
  const handleProductClick = () => {
    window.open(product.product_url, '_blank', 'noopener,noreferrer');
  };

  /**
   * Close image modal
   */
  const closeImageModal = () => {
    setIsImageModalOpen(false);
  };

  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-200 hover:-translate-y-1 overflow-hidden">
      {/* Product Image */}
      <div className="aspect-square bg-neutral-100 relative group">
        <img 
          src={product.image_url || PLACEHOLDER_IMAGE} 
          alt={product.product_name}
          onError={handleImageError}
          onClick={handleImageClick}
          className="w-full h-full object-cover cursor-pointer transition-transform duration-200 group-hover:scale-105"
          title="Click to view full size image"
        />
        
        {/* Image overlay with zoom icon */}
        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-200 flex items-center justify-center opacity-0 group-hover:opacity-100">
          <svg 
            className="w-8 h-8 text-white drop-shadow-lg" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" 
            />
          </svg>
        </div>
        
        {/* Availability Badge (overlay on image) */}
        {!product.availability && (
          <div className="absolute top-2 right-2 bg-error-500 text-white px-2.5 py-1 rounded-full text-xs font-semibold shadow-md">
            Out of Stock
          </div>
        )}
      </div>

      {/* Product Details */}
      <div className="p-5">
        {/* Platform Badge */}
        <div className="flex items-center justify-between mb-2">
          <span 
            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPlatformBadgeColor(product.platform)}`}
          >
            {product.platform}
          </span>
          
          {/* Availability Indicator (text) */}
          {product.availability && (
            <span className="text-xs text-success-600 font-medium flex items-center">
              <svg 
                className="w-3 h-3 mr-1" 
                fill="currentColor" 
                viewBox="0 0 20 20"
                aria-hidden="true"
              >
                <path 
                  fillRule="evenodd" 
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" 
                  clipRule="evenodd" 
                />
              </svg>
              In Stock
            </span>
          )}
        </div>

        {/* Product Name */}
        <h3 
          className="text-lg font-semibold text-neutral-900 mb-2 line-clamp-2 min-h-[3.5rem] cursor-pointer hover:text-primary-600 transition-colors"
          onClick={handleProductClick}
          title="Click to view product page"
        >
          {product.product_name}
        </h3>

        {/* Price */}
        <p className="text-2xl font-bold text-primary-500 mb-4">
          {formatPrice(product.current_price, product.currency)}
        </p>

        {/* Track Button */}
        <button
          onClick={handleTrackClick}
          disabled={isTracking || !product.availability}
          className={`w-full py-2.5 px-4 rounded-lg font-semibold transition-fast ${
            isTracking || !product.availability
              ? 'bg-neutral-300 text-neutral-500 cursor-not-allowed'
              : 'bg-primary-500 text-white hover:bg-primary-600 active:bg-primary-700'
          }`}
          aria-label={`Track ${product.product_name}`}
        >
          {isTracking ? (
            <span className="flex items-center justify-center">
              <svg 
                className="animate-spin h-5 w-5 mr-2" 
                fill="none" 
                viewBox="0 0 24 24"
                aria-hidden="true"
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
              Tracking...
            </span>
          ) : !product.availability ? (
            'Unavailable'
          ) : (
            'Track This Product'
          )}
        </button>

        {/* Product URL Link (optional - for accessibility) */}
        <a
          href={product.product_url}
          target="_blank"
          rel="noopener noreferrer"
          className="block mt-3 text-center text-sm text-neutral-600 hover:text-primary-500 transition-fast"
        >
          View on {product.platform}
          <svg 
            className="inline-block w-3 h-3 ml-1" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" 
            />
          </svg>
        </a>
      </div>

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
