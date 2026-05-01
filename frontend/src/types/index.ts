/**
 * Central export file for all TypeScript type definitions.
 * Import types from this file in your components.
 * 
 * Example usage:
 *   import { UserLogin, ProductResult, TrackedProductResponse } from '@/types';
 */

// Auth types
export type {
  UserRegister,
  UserLogin,
  UserResponse,
  TokenData,
} from './auth';

// Product types
export type {
  ProductResult,
  SearchResults,
  PriceHistoryEntry,
  PriceHistoryResponse,
} from './product';

// Tracking types
export type {
  TrackedProductCreate,
  TrackedProductResponse,
  ThresholdUpdate,
} from './tracking';
