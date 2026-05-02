/**
 * Navigation Component
 * 
 * Shared navigation bar for the application.
 * 
 * Features:
 * - Logo and branding
 * - Navigation links with active states
 * - User menu with logout
 * - Responsive design
 * - Badge for tracked products count
 */

import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { getTrackedProducts } from '../services/trackingService';

interface NavigationProps {
  /**
   * Optional additional class names
   */
  className?: string;
}

export default function Navigation({ className = '' }: NavigationProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const [trackedCount, setTrackedCount] = useState(0);
  const [showUserMenu, setShowUserMenu] = useState(false);

  // Load tracked products count
  useEffect(() => {
    const loadTrackedCount = async () => {
      try {
        const products = await getTrackedProducts();
        setTrackedCount(products.length);
      } catch (error) {
        // Silently fail - user might not be authenticated
        setTrackedCount(0);
      }
    };

    loadTrackedCount();
    
    // Refresh count every 30 seconds
    const interval = setInterval(loadTrackedCount, 30000);
    return () => clearInterval(interval);
  }, []);

  /**
   * Handle logout
   */
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  /**
   * Check if a path is active
   */
  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <nav className={`glass backdrop-blur-xl border-b border-dark-200/30 sticky top-0 z-50 ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link to="/dashboard" className="flex items-center group">
              <div className="w-10 h-10 bg-gradient-to-br from-accent-blue to-accent-purple rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <span className="ml-3 text-xl font-bold gradient-text">PriceTracker</span>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-2">
            <Link
              to="/dashboard"
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                isActive('/dashboard')
                  ? 'bg-accent-blue/20 text-accent-blue shadow-lg shadow-accent-blue/20'
                  : 'text-dark-600 hover:text-dark-900 hover:bg-dark-100/50'
              }`}
            >
              <div className="flex items-center space-x-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span>Search</span>
              </div>
            </Link>

            <Link
              to="/tracked"
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all relative ${
                isActive('/tracked')
                  ? 'bg-accent-purple/20 text-accent-purple shadow-lg shadow-accent-purple/20'
                  : 'text-dark-600 hover:text-dark-900 hover:bg-dark-100/50'
              }`}
            >
              <div className="flex items-center space-x-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span>Tracked</span>
                {trackedCount > 0 && (
                  <span className="inline-flex items-center justify-center px-2 py-0.5 text-xs font-bold leading-none text-white bg-gradient-to-r from-accent-pink to-accent-orange rounded-full animate-pulse-slow">
                    {trackedCount}
                  </span>
                )}
              </div>
            </Link>
          </div>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            {/* Notifications */}
            <button className="text-dark-500 hover:text-accent-blue transition-colors relative pulse-ring">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <span className="absolute top-0 right-0 w-2 h-2 bg-accent-pink rounded-full"></span>
            </button>

            {/* User Dropdown */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-2 text-dark-700 hover:text-dark-900 transition-colors"
              >
                <div className="w-9 h-9 bg-gradient-to-br from-accent-blue to-accent-purple rounded-full flex items-center justify-center shadow-lg">
                  <span className="text-sm font-bold text-white">U</span>
                </div>
                <svg className="w-4 h-4 text-dark-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {/* Dropdown Menu */}
              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-56 glass backdrop-blur-xl rounded-2xl shadow-2xl py-2 z-50 border border-dark-200/30 animate-slide-down">
                  <div className="px-4 py-3 text-sm text-dark-600 border-b border-dark-200/30">
                    Signed in as <span className="font-semibold text-dark-900">User</span>
                  </div>
                  
                  <Link
                    to="/dashboard"
                    className="block px-4 py-2.5 text-sm text-dark-700 hover:bg-accent-blue/10 hover:text-accent-blue transition-all mx-2 rounded-xl mt-2"
                    onClick={() => setShowUserMenu(false)}
                  >
                    <div className="flex items-center space-x-3">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                      <span>Search Products</span>
                    </div>
                  </Link>
                  
                  <Link
                    to="/tracked"
                    className="block px-4 py-2.5 text-sm text-dark-700 hover:bg-accent-purple/10 hover:text-accent-purple transition-all mx-2 rounded-xl"
                    onClick={() => setShowUserMenu(false)}
                  >
                    <div className="flex items-center space-x-3">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                      <span>Tracked ({trackedCount})</span>
                    </div>
                  </Link>
                  
                  <div className="border-t border-dark-200/30 mt-2 pt-2">
                    <button
                      onClick={handleLogout}
                      className="block w-full text-left px-4 py-2.5 text-sm text-error-500 hover:bg-error-500/10 transition-all mx-2 rounded-xl mb-2"
                    >
                      <div className="flex items-center space-x-3">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        <span>Sign Out</span>
                      </div>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Click outside to close dropdown */}
      {showUserMenu && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setShowUserMenu(false)}
        />
      )}
    </nav>
  );
}