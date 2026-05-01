/**
 * ImageModal Component
 * 
 * A modal for displaying product images in full size with zoom functionality.
 * 
 * Features:
 * - Full-screen image display
 * - Click outside to close
 * - ESC key to close
 * - Zoom in/out functionality
 * - Loading state
 * - Error handling for broken images
 */

import { useEffect, useState } from 'react';

interface ImageModalProps {
  /**
   * Image URL to display
   */
  imageUrl: string;
  
  /**
   * Alt text for the image
   */
  altText: string;
  
  /**
   * Whether the modal is open
   */
  isOpen: boolean;
  
  /**
   * Callback when modal should be closed
   */
  onClose: () => void;
  
  /**
   * Product name for context
   */
  productName?: string;
}

export default function ImageModal({ 
  imageUrl, 
  altText, 
  isOpen, 
  onClose, 
  productName 
}: ImageModalProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const [isZoomed, setIsZoomed] = useState(false);

  // Handle ESC key press
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
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
  }, [isOpen, onClose]);

  // Reset states when modal opens/closes
  useEffect(() => {
    if (isOpen) {
      setIsLoading(true);
      setHasError(false);
      setIsZoomed(false);
    }
  }, [isOpen, imageUrl]);

  /**
   * Handle image load success
   */
  const handleImageLoad = () => {
    setIsLoading(false);
    setHasError(false);
  };

  /**
   * Handle image load error
   */
  const handleImageError = () => {
    setIsLoading(false);
    setHasError(true);
  };

  /**
   * Handle backdrop click (close modal)
   */
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  /**
   * Toggle zoom
   */
  const toggleZoom = () => {
    setIsZoomed(!isZoomed);
  };

  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
    >
      {/* Modal Content */}
      <div className="relative max-w-7xl max-h-full w-full h-full flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between mb-4 text-white">
          <div className="flex-1">
            {productName && (
              <h2 className="text-lg font-semibold truncate">{productName}</h2>
            )}
          </div>
          
          <div className="flex items-center space-x-2 ml-4">
            {/* Zoom Toggle */}
            <button
              onClick={toggleZoom}
              className="p-2 rounded-lg bg-black bg-opacity-50 hover:bg-opacity-70 transition-all"
              title={isZoomed ? 'Zoom Out' : 'Zoom In'}
            >
              <svg 
                className="w-5 h-5" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                {isZoomed ? (
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10h-3m-3 0h3m0 0V7m0 3v3" 
                  />
                ) : (
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" 
                  />
                )}
              </svg>
            </button>
            
            {/* Close Button */}
            <button
              onClick={onClose}
              className="p-2 rounded-lg bg-black bg-opacity-50 hover:bg-opacity-70 transition-all"
              title="Close (ESC)"
            >
              <svg 
                className="w-5 h-5" 
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
          </div>
        </div>

        {/* Image Container */}
        <div className="flex-1 flex items-center justify-center relative overflow-hidden">
          {/* Loading State */}
          {isLoading && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="flex items-center space-x-2 text-white">
                <svg 
                  className="animate-spin w-8 h-8" 
                  fill="none" 
                  viewBox="0 0 24 24"
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
                <span>Loading image...</span>
              </div>
            </div>
          )}

          {/* Error State */}
          {hasError && (
            <div className="flex flex-col items-center text-white">
              <svg 
                className="w-16 h-16 mb-4 text-neutral-400" 
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
              <h3 className="text-lg font-semibold mb-2">Failed to load image</h3>
              <p className="text-neutral-300 text-center">
                The image could not be loaded. It may have been moved or deleted.
              </p>
            </div>
          )}

          {/* Image */}
          <img
            src={imageUrl}
            alt={altText}
            onLoad={handleImageLoad}
            onError={handleImageError}
            onClick={toggleZoom}
            className={`
              max-w-full max-h-full object-contain cursor-pointer transition-transform duration-300
              ${isZoomed ? 'scale-150' : 'scale-100'}
              ${isLoading ? 'opacity-0' : 'opacity-100'}
            `}
            style={{ display: hasError ? 'none' : 'block' }}
          />
        </div>

        {/* Footer */}
        <div className="mt-4 text-center text-neutral-300 text-sm">
          <p>Click image to zoom • Click outside or press ESC to close</p>
        </div>
      </div>
    </div>
  );
}