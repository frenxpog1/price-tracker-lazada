/**
 * PriceChart Component
 * 
 * A line chart component for displaying price history over time.
 * 
 * Features:
 * - Interactive line chart with Recharts
 * - Price history visualization
 * - Threshold line indicator
 * - Responsive design
 * - Hover tooltips with price and date
 * - Price drop indicators
 * - Loading and empty states
 * - Currency formatting
 * 
 * Requirements: 3.5
 */

import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  ReferenceLine,
  Legend
} from 'recharts';
import { PriceHistoryEntry } from '../services/trackingService';

interface PriceChartProps {
  /**
   * Price history data
   */
  priceHistory: PriceHistoryEntry[];
  
  /**
   * Current threshold price for reference line
   */
  thresholdPrice?: number;
  
  /**
   * Currency code for formatting
   */
  currency?: string;
  
  /**
   * Chart height in pixels
   */
  height?: number;
  
  /**
   * Whether data is loading
   */
  isLoading?: boolean;
  
  /**
   * Product name for chart title
   */
  productName?: string;
}

/**
 * Format price for display
 */
function formatPrice(price: number | string, currency: string = 'USD'): string {
  // Convert to number if it's a string
  const numPrice = typeof price === 'string' ? parseFloat(price) : price;
  
  // Handle invalid numbers
  if (isNaN(numPrice)) {
    return `${currency} --`;
  }
  
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
  return `${symbol}${numPrice.toFixed(2)}`;
}

/**
 * Format date for display
 */
function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * Custom tooltip component
 */
function CustomTooltip({ active, payload, label }: any) {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="modern-card p-3">
        <p className="text-sm font-semibold text-white mb-1">
          {formatDate(label)}
        </p>
        <p className="text-sm text-white/60 mb-1">
          Price: <span className="font-semibold text-white">
            {formatPrice(data.price, data.currency)}
          </span>
        </p>
        {!data.is_available && (
          <p className="text-xs text-yellow-400">
            ⚠️ Product unavailable
          </p>
        )}
      </div>
    );
  }
  return null;
}

export default function PriceChart({
  priceHistory,
  thresholdPrice,
  currency = 'USD',
  height = 300,
  isLoading = false,
  productName,
}: PriceChartProps) {
  // Loading state
  if (isLoading) {
    return (
      <div className="modern-card p-6">
        <div className="flex items-center justify-center" style={{ height }}>
          <div className="flex items-center space-x-2 text-white/50">
            <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            <span>Loading price history...</span>
          </div>
        </div>
      </div>
    );
  }

  // Empty state
  if (!priceHistory || priceHistory.length === 0) {
    return (
      <div className="modern-card p-6">
        <div className="flex flex-col items-center justify-center text-center" style={{ height }}>
          <svg className="w-12 h-12 text-white/20 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <h3 className="text-lg font-semibold text-white mb-1">No Price History</h3>
          <p className="text-white/50 max-w-sm">
            Price history will appear here once we start monitoring this product.
          </p>
        </div>
      </div>
    );
  }

  // Prepare chart data
  const chartData = priceHistory.map(entry => ({
    timestamp: entry.timestamp,
    price: typeof entry.price === 'string' ? parseFloat(entry.price) : entry.price,
    currency: entry.currency,
    is_available: entry.is_available,
    // Format timestamp for X-axis
    formattedDate: formatDate(entry.timestamp),
  }));

  // Calculate price range for better Y-axis scaling
  const prices = priceHistory.map(entry => typeof entry.price === 'string' ? parseFloat(entry.price) : entry.price);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const priceRange = maxPrice - minPrice;
  const yAxisMin = Math.max(0, minPrice - (priceRange * 0.1));
  const yAxisMax = maxPrice + (priceRange * 0.1);

  return (
    <div className="modern-card p-6">
      {/* Chart Header */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white mb-1">
          Price History
          {productName && (
            <span className="text-sm font-normal text-white/60 ml-2">
              for {productName}
            </span>
          )}
        </h3>
        <p className="text-sm text-white/60">
          {priceHistory.length} price {priceHistory.length === 1 ? 'record' : 'records'} 
          {priceHistory.length > 0 && (
            <span className="ml-2">
              • Latest: {formatPrice(priceHistory[priceHistory.length - 1].price, currency)}
            </span>
          )}
        </p>
      </div>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={height}>
        <LineChart
          data={chartData}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          
          <XAxis 
            dataKey="formattedDate"
            tick={{ fontSize: 12, fill: 'rgba(255,255,255,0.5)' }}
            tickLine={{ stroke: 'rgba(255,255,255,0.1)' }}
            axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
          />
          
          <YAxis 
            domain={[yAxisMin, yAxisMax]}
            tick={{ fontSize: 12, fill: 'rgba(255,255,255,0.5)' }}
            tickLine={{ stroke: 'rgba(255,255,255,0.1)' }}
            axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
            tickFormatter={(value) => formatPrice(value, currency)}
          />
          
          <Tooltip content={<CustomTooltip />} />
          
          {/* Threshold reference line */}
          {thresholdPrice && (
            <ReferenceLine 
              y={thresholdPrice} 
              stroke="#ef4444" 
              strokeDasharray="5 5"
              label={{ 
                value: `Target: ${formatPrice(thresholdPrice, currency)}`, 
                position: 'top',
                style: { fontSize: '12px', fill: '#ef4444' }
              }}
            />
          )}
          
          {/* Price line */}
          <Line
            type="monotone"
            dataKey="price"
            stroke="#60a5fa"
            strokeWidth={2}
            dot={{ 
              fill: '#60a5fa', 
              strokeWidth: 2, 
              r: 4,
              stroke: '#0A0A0A'
            }}
            activeDot={{ 
              r: 6, 
              stroke: '#60a5fa', 
              strokeWidth: 2,
              fill: '#0A0A0A'
            }}
            connectNulls={false}
          />
          
          <Legend 
            content={() => (
              <div className="flex items-center justify-center space-x-6 mt-4 text-sm">
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-0.5 bg-blue-400"></div>
                  <span className="text-white/60">Price</span>
                </div>
                {thresholdPrice && (
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-0.5 bg-red-500 border-dashed"></div>
                    <span className="text-white/60">Target Price</span>
                  </div>
                )}
              </div>
            )}
          />
        </LineChart>
      </ResponsiveContainer>

      {/* Chart Footer with Statistics */}
      {priceHistory.length > 1 && (
        <div className="mt-4 pt-4 border-t border-white/10">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-sm text-white/50">Lowest Price</p>
              <p className="text-lg font-semibold text-green-400">
                {formatPrice(minPrice, currency)}
              </p>
            </div>
            <div>
              <p className="text-sm text-white/50">Highest Price</p>
              <p className="text-lg font-semibold text-red-400">
                {formatPrice(maxPrice, currency)}
              </p>
            </div>
            <div>
              <p className="text-sm text-white/50">Price Range</p>
              <p className="text-lg font-semibold text-white">
                {formatPrice(priceRange, currency)}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Usage Examples:
 * 
 * // Basic usage
 * <PriceChart
 *   priceHistory={priceHistoryData}
 *   thresholdPrice={99.99}
 *   currency="USD"
 *   productName="iPhone 15 Pro"
 * />
 * 
 * // With loading state
 * <PriceChart
 *   priceHistory={[]}
 *   isLoading={true}
 *   height={400}
 * />
 * 
 * // Custom height
 * <PriceChart
 *   priceHistory={priceHistoryData}
 *   thresholdPrice={50.00}
 *   currency="EUR"
 *   height={250}
 * />
 */