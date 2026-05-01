/**
 * ThresholdEditor Component
 * 
 * An inline editor for updating price thresholds with validation.
 * 
 * Features:
 * - Inline editing with input field
 * - Real-time validation for positive numbers
 * - Save/cancel actions
 * - Loading states
 * - Error handling
 * - Currency formatting
 * - Keyboard shortcuts (Enter to save, Escape to cancel)
 * 
 * Requirements: 8.1, 8.2
 */

import { useState, useEffect, useRef } from 'react';

interface ThresholdEditorProps {
  /**
   * Current threshold value
   */
  currentThreshold: number;
  
  /**
   * Currency code (e.g., 'USD', 'EUR')
   */
  currency?: string;
  
  /**
   * Callback when threshold is saved
   */
  onSave: (newThreshold: number) => Promise<void>;
  
  /**
   * Callback when editing is cancelled
   */
  onCancel: () => void;
  
  /**
   * Whether save operation is in progress
   */
  isSaving?: boolean;
  
  /**
   * Whether the editor is in edit mode
   */
  isEditing: boolean;
  
  /**
   * Additional CSS classes
   */
  className?: string;
  
  /**
   * Minimum allowed threshold value
   */
  minValue?: number;
  
  /**
   * Maximum allowed threshold value
   */
  maxValue?: number;
}

/**
 * Format price with currency symbol
 */
function formatPrice(price: number, currency: string = 'USD'): string {
  const currencySymbols: { [key: string]: string } = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
    'SGD': 'S$',
    'MYR': 'RM',
    'THB': '฿',
  };
  
  const symbol = currencySymbols[currency] || currency;
  return `${symbol}${price.toFixed(2)}`;
}

export default function ThresholdEditor({
  currentThreshold,
  currency = 'USD',
  onSave,
  onCancel,
  isSaving = false,
  isEditing,
  className = '',
  minValue = 0.01,
  maxValue = 999999.99,
}: ThresholdEditorProps) {
  const [inputValue, setInputValue] = useState(currentThreshold.toString());
  const [validationError, setValidationError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Focus input when entering edit mode
  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [isEditing]);

  // Reset input value when currentThreshold changes
  useEffect(() => {
    setInputValue(currentThreshold.toString());
    setValidationError(null);
  }, [currentThreshold]);

  /**
   * Validate the input value
   */
  const validateInput = (value: string): string | null => {
    if (!value.trim()) {
      return 'Threshold is required';
    }

    const numValue = parseFloat(value);
    
    if (isNaN(numValue)) {
      return 'Please enter a valid number';
    }

    if (numValue < minValue) {
      return `Threshold must be at least ${formatPrice(minValue, currency)}`;
    }

    if (numValue > maxValue) {
      return `Threshold cannot exceed ${formatPrice(maxValue, currency)}`;
    }

    return null;
  };

  /**
   * Handle input change with validation
   */
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInputValue(value);
    
    // Clear validation error when user starts typing
    if (validationError) {
      setValidationError(null);
    }
  };

  /**
   * Handle save action
   */
  const handleSave = async () => {
    const error = validateInput(inputValue);
    
    if (error) {
      setValidationError(error);
      return;
    }

    const newThreshold = parseFloat(inputValue);
    
    // Don't save if value hasn't changed
    if (newThreshold === currentThreshold) {
      onCancel();
      return;
    }

    try {
      await onSave(newThreshold);
    } catch (error) {
      console.error('Failed to save threshold:', error);
      setValidationError('Failed to save threshold. Please try again.');
    }
  };

  /**
   * Handle cancel action
   */
  const handleCancel = () => {
    setInputValue(currentThreshold.toString());
    setValidationError(null);
    onCancel();
  };

  /**
   * Handle keyboard shortcuts
   */
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSave();
    } else if (e.key === 'Escape') {
      e.preventDefault();
      handleCancel();
    }
  };

  if (!isEditing) {
    return (
      <span className={`text-2xl font-bold text-neutral-900 ${className}`}>
        {formatPrice(currentThreshold, currency)}
      </span>
    );
  }

  return (
    <div className={`space-y-2 ${className}`}>
      {/* Input Field */}
      <div className="flex items-center space-x-2">
        <div className="relative">
          <input
            ref={inputRef}
            type="number"
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            className={`w-32 px-3 py-2 text-lg font-semibold border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-fast ${
              validationError 
                ? 'border-error-300 bg-error-50' 
                : 'border-neutral-300 bg-white'
            }`}
            step="0.01"
            min={minValue}
            max={maxValue}
            disabled={isSaving}
            placeholder="0.00"
            aria-label="Price threshold"
          />
          
          {/* Currency Symbol Overlay */}
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-neutral-500 pointer-events-none">
            {currency === 'USD' && '$'}
            {currency === 'EUR' && '€'}
            {currency === 'GBP' && '£'}
            {currency === 'JPY' && '¥'}
            {currency === 'SGD' && 'S$'}
            {currency === 'MYR' && 'RM'}
            {currency === 'THB' && '฿'}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center space-x-1">
          <button
            onClick={handleSave}
            disabled={isSaving || !!validationError}
            className="p-2 text-success-600 hover:text-success-700 hover:bg-success-50 rounded-lg transition-fast disabled:opacity-50 disabled:cursor-not-allowed"
            title="Save threshold (Enter)"
            aria-label="Save threshold"
          >
            {isSaving ? (
              <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>
          
          <button
            onClick={handleCancel}
            disabled={isSaving}
            className="p-2 text-neutral-400 hover:text-neutral-600 hover:bg-neutral-50 rounded-lg transition-fast disabled:opacity-50"
            title="Cancel editing (Escape)"
            aria-label="Cancel editing"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Validation Error */}
      {validationError && (
        <div className="flex items-start space-x-2 text-sm text-error-600">
          <svg className="w-4 h-4 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{validationError}</span>
        </div>
      )}

      {/* Helper Text */}
      {!validationError && (
        <div className="text-xs text-neutral-500">
          Press Enter to save, Escape to cancel
        </div>
      )}
    </div>
  );
}

/**
 * Usage Examples:
 * 
 * // Basic usage
 * <ThresholdEditor
 *   currentThreshold={99.99}
 *   currency="USD"
 *   isEditing={isEditing}
 *   onSave={async (newThreshold) => {
 *     await updateThreshold(productId, newThreshold);
 *     setIsEditing(false);
 *   }}
 *   onCancel={() => setIsEditing(false)}
 * />
 * 
 * // With custom validation limits
 * <ThresholdEditor
 *   currentThreshold={50.00}
 *   currency="EUR"
 *   isEditing={true}
 *   minValue={1.00}
 *   maxValue={1000.00}
 *   onSave={handleSave}
 *   onCancel={handleCancel}
 *   isSaving={isSaving}
 * />
 * 
 * // With custom styling
 * <ThresholdEditor
 *   currentThreshold={25.99}
 *   isEditing={editMode}
 *   className="my-custom-class"
 *   onSave={handleThresholdUpdate}
 *   onCancel={() => setEditMode(false)}
 * />
 */