/**
 * TrackPriceModal Component
 * 
 * A beautiful modal for setting price tracking thresholds.
 * 
 * Features:
 * - Product information display
 * - Current price vs target price comparison
 * - Input validation with real-time feedback
 * - Percentage savings calculation
 * - Smooth animations and transitions
 * - Keyboard accessibility (ESC to close)
 * - Form validation and error handling
 */

import { useState, useEffect } from 'react';
import { ProductResult } from '../types/product';

interface TrackPriceModalProps {
  /**
   * Product to track
   */
  product: ProductResult | null;
  
  /**
   * Whether the modal is open
   */
  isOpen: boolean;
  
  /**
   * Callback when modal should be closed
   */
  onClose: () => void;
  
  /**
   * Callback when tracking is confirmed
   */
  onConfirm: (product: ProductResult, threshold: number) => Promise<void>;
  
  /**
   * Whether tracking is in progress
   */
  isTracking?: boolean;
}

/**
 * Format price with currency
 */
const formatPrice = (price: number | string, currency: string): string => {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price;
  
  if (isNaN(numPrice)) {
    return `${currency} --`;
  }
  
  if (currency === 'PHP' || currency === '₱') {
    return `₱${numPrice.toFixed(2)}`;
  }
  
  return `${currency} ${numPrice.toFixed(2)}`;
};

/**
 * Calculate percentage difference
 */
const calculatePercentage = (current: number, target: number): number => {
  if (current === 0) return 0;
  return ((current - target) / current) * 100;
};

export default function TrackPriceModal({
  product,
  isOpen,
  onClose,
  onConfirm,
  isTracking = false
}: TrackPriceModalProps) {
  const [threshold, setThreshold] = useState('');
  const [error, setError] = useState('');
  const [isValid, setIsValid] = useState(false);

  // Get current price as number
  const currentPrice = product ? (typeof product.current_price === 'string' ? parseFloat(product.current_price) : product.current_price) : 0;

  // Handle ESC key press
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && !isTracking) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscKey);
      // Prevent body scroll when modal is open
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscKey);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose, isTracking]);

  // Reset form when modal opens
  useEffect(() => {
    if (isOpen && product) {
      setThreshold(currentPrice.toFixed(2));
      setError('');
      setIsValid(true);
    }
  }, [isOpen, product, currentPrice]);

  // Validate threshold input
  useEffect(() => {
    const thresholdNum = parseFloat(threshold);
    
    if (!threshold.trim()) {
      setError('Please enter a target price');
      setIsValid(false);
    } else if (isNaN(thresholdNum)) {
      setError('Please enter a valid number');
      setIsValid(false);
    } else if (thresholdNum <= 0) {
      setError('Price must be greater than 0');
      setIsValid(false);
    } else if (thresholdNum > currentPrice * 2) {
      setError('Target price seems too high');
      setIsValid(false);
    } else {
      setError('');
      setIsValid(true);
    }
  }, [threshold, currentPrice]);

  /**
   * Handle form submission
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!product || !isValid || isTracking) return;
    
    const thresholdNum = parseFloat(threshold);
    
    try {
      await onConfirm(product, thresholdNum);
      onClose();
    } catch (error) {
      // Error handling is done in the parent component
    }
  };

  /**
   * Handle backdrop click (close modal)
   */
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget && !isTracking) {
      onClose();
    }
  };

  if (!isOpen || !product) return null;

  const thresholdNum = parseFloat(threshold) || 0;
  const savings = currentPrice - thresholdNum;
  const savingsPercentage = calculatePercentage(currentPrice, thresholdNum);
  const isBelow = thresholdNum < currentPrice;

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
    >
      {/* Modal Content */}
      <div className="modern-card max-w-md w-full transform transition-all">
        {/* Header */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center">
                <svg 
                  className="w-5 h-5 text-white" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" 
                  />
                </svg>
              </div>
              <div>
                <h2 className="text-xl font-semibold text-white">Track Price</h2>
                <p className="text-sm text-white/60">Set your target price alert</p>
              </div>
            </div>
            
            {!isTracking && (
              <button
                onClick={onClose}
                className="text-white/40 hover:text-white/70 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        </div>

        {/* Product Info */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-start space-x-4">
            {/* Product Image */}
            <div className="flex-shrink-0">
              <img
                src={product.image_url || 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60"%3E%3Crect fill="%23f3f4f6" width="60" height="60"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="12" fill="%239ca3af"%3ENo Image%3C/text%3E%3C/svg%3E'}
                alt={product.product_name}
                className="w-16 h-16 rounded-lg object-cover"
                onError={(e) => {
                  e.currentTarget.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60"%3E%3Crect fill="%23f3f4f6" width="60" height="60"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="12" fill="%239ca3af"%3ENo Image%3C/text%3E%3C/svg%3E';
                }}
              />
            </div>
            
            {/* Product Details */}
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-white line-clamp-2 mb-1">
                {product.product_name}
              </h3>
              <div className="flex items-center space-x-2">
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-500/20 text-blue-300">
                  {product.platform}
                </span>
                <span className="text-sm text-white/60">
                  Current: {formatPrice(currentPrice, product.currency)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6">
          {/* Target Price Input */}
          <div className="mb-6">
            <label htmlFor="threshold" className="block text-sm font-medium text-white/70 mb-2">
              Target Price
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span className="text-white/50 text-lg">
                  {product.currency === 'PHP' ? '₱' : product.currency}
                </span>
              </div>
              <input
                id="threshold"
                type="number"
                value={threshold}
                onChange={(e) => setThreshold(e.target.value)}
                step="0.01"
                min="0"
                disabled={isTracking}
                className={`
                  modern-input block w-full pl-8 pr-3 py-3 text-lg font-semibold
                  disabled:opacity-50 disabled:cursor-not-allowed
                  ${error ? 'border-red-500/50' : ''}
                `}
                placeholder="0.00"
              />
            </div>
            
            {/* Error Message */}
            {error && (
              <p className="mt-2 text-sm text-red-400 flex items-center">
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {error}
              </p>
            )}
          </div>

          {/* Price Comparison */}
          {isValid && thresholdNum > 0 && (
            <div className="mb-6 p-4 bg-white/5 rounded-lg border border-white/10">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-white/50 mb-1">Current Price</p>
                  <p className="font-semibold text-white">
                    {formatPrice(currentPrice, product.currency)}
                  </p>
                </div>
                <div>
                  <p className="text-white/50 mb-1">Target Price</p>
                  <p className="font-semibold text-white">
                    {formatPrice(thresholdNum, product.currency)}
                  </p>
                </div>
              </div>
              
              {/* Savings Indicator */}
              <div className="mt-3 pt-3 border-t border-white/10">
                {isBelow ? (
                  <div className="flex items-center text-green-400">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                    <span className="text-sm font-medium">
                      You'll save {formatPrice(savings, product.currency)} ({savingsPercentage.toFixed(1)}%)
                    </span>
                  </div>
                ) : (
                  <div className="flex items-center text-yellow-400">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                    </svg>
                    <span className="text-sm font-medium">
                      Target is {formatPrice(Math.abs(savings), product.currency)} above current price
                    </span>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button
              type="button"
              onClick={onClose}
              disabled={isTracking}
              className="flex-1 px-4 py-3 text-white bg-white/10 rounded-lg hover:bg-white/20 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!isValid || isTracking}
              className="flex-1 modern-button py-3 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isTracking ? (
                <>
                  <svg className="animate-spin w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                  </svg>
                  Tracking...
                </>
              ) : (
                'Start Tracking'
              )}
            </button>
          </div>
        </form>

        {/* Footer Info */}
        <div className="px-6 pb-6">
          <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-blue-400 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="text-sm text-blue-300">
                <p className="font-medium mb-1">How it works:</p>
                <p className="text-blue-200/80">We'll check this product's price regularly and notify you when it drops to or below your target price.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}