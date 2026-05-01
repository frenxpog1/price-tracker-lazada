/**
 * Axios API client configuration
 * 
 * This module configures an Axios instance with:
 * - Base URL pointing to the backend API
 * - Request interceptor for JWT token injection
 * - Response interceptor for error handling
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

// Get API base URL from environment variable or default to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Configured Axios instance for API requests
 */
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 90000, // 90 second timeout for slow scraping
});

/**
 * Request interceptor to inject JWT token from localStorage
 */
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Get token from localStorage
    const token = localStorage.getItem('token');
    
    // If token exists, add it to Authorization header
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    // Handle request error
    return Promise.reject(error);
  }
);

/**
 * Response interceptor for centralized error handling
 */
api.interceptors.response.use(
  (response) => {
    // Return successful response as-is
    return response;
  },
  (error: AxiosError) => {
    // Handle different error scenarios
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      
      switch (status) {
        case 401:
          // Unauthorized - clear token and redirect to login
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          
          // Only redirect if not already on login/register page
          if (!window.location.pathname.includes('/login') && 
              !window.location.pathname.includes('/register')) {
            window.location.href = '/login';
          }
          break;
          
        case 403:
          // Forbidden - user doesn't have permission
          console.error('Access forbidden:', error.response.data);
          break;
          
        case 404:
          // Not found
          console.error('Resource not found:', error.response.data);
          break;
          
        case 422:
          // Validation error
          console.error('Validation error:', error.response.data);
          break;
          
        case 500:
          // Internal server error
          console.error('Server error:', error.response.data);
          break;
          
        default:
          console.error('API error:', error.response.data);
      }
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network error: No response from server');
    } else {
      // Something else happened
      console.error('Request error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default api;

/**
 * Usage Examples:
 * 
 * // Import the configured API client
 * import api from '@/services/api';
 * 
 * // Make a GET request
 * const response = await api.get('/products/search?q=laptop');
 * 
 * // Make a POST request
 * const response = await api.post('/auth/login', {
 *   email: 'user@example.com',
 *   password: 'password123'
 * });
 * 
 * // Make a PATCH request
 * const response = await api.patch('/tracking/products/123/threshold', {
 *   price_threshold: 999.99
 * });
 * 
 * // Make a DELETE request
 * const response = await api.delete('/tracking/products/123');
 * 
 * // The JWT token is automatically injected from localStorage
 * // Error handling is centralized in the response interceptor
 */
