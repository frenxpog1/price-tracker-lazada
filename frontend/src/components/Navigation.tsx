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
  // Reserved for future use
}

export default function Navigation({}: NavigationProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const [trackedCount, setTrackedCount] = useState(0);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState<Array<{
    id: string;
    title: string;
    message: string;
    time: string;
    read: boolean;
  }>>([
    {
      id: '1',
      title: 'Price Drop Alert',
      message: 'Samsung Galaxy A54 dropped below your target price!',
      time: '2 hours ago',
      read: false
    },
    {
      id: '2',
      title: 'Welcome!',
      message: 'Start tracking products to get price alerts',
      time: '1 day ago',
      read: true
    }
  ]);

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
   * Mark notification as read
   */
  const markAsRead = (id: string) => {
    setNotifications(prev =>
      prev.map(n => n.id === id ? { ...n, read: true } : n)
    );
  };

  /**
   * Clear all notifications
   */
  const clearAllNotifications = () => {
    setNotifications([]);
    setShowNotifications(false);
  };

  /**
   * Get unread count
   */
  const unreadCount = notifications.filter(n => !n.read).length;

  /**
   * Check if a path is active
   */
  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <nav className="border-b border-white/10 backdrop-blur-xl bg-black/50 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center gap-2 group">
            <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <span className="text-lg font-semibold">PriceTracker</span>
          </Link>

          {/* Nav Links */}
          <div className="hidden md:flex items-center gap-1">
            <Link
              to="/dashboard"
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive('/dashboard')
                  ? 'bg-white/10 text-white'
                  : 'text-white/60 hover:text-white hover:bg-white/5'
              }`}
            >
              Search
            </Link>

            <Link
              to="/tracked"
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 ${
                isActive('/tracked')
                  ? 'bg-white/10 text-white'
                  : 'text-white/60 hover:text-white hover:bg-white/5'
              }`}
            >
              Tracked
              {trackedCount > 0 && (
                <span className="bg-white text-black text-xs px-1.5 py-0.5 rounded-md font-semibold">
                  {trackedCount}
                </span>
              )}
            </Link>
          </div>

          {/* Right side */}
          <div className="flex items-center gap-3">
            {/* Notifications */}
            <div className="relative">
              <button 
                onClick={() => setShowNotifications(!showNotifications)}
                className="w-9 h-9 rounded-lg hover:bg-white/5 flex items-center justify-center transition-colors relative"
              >
                <svg className="w-5 h-5 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                {unreadCount > 0 && (
                  <span className="absolute top-1 right-1 w-2 h-2 bg-blue-500 rounded-full"></span>
                )}
              </button>

              {/* Notifications Dropdown */}
              {showNotifications && (
                <div className="absolute right-0 mt-2 w-80 modern-card p-0 max-h-96 overflow-hidden flex flex-col">
                  {/* Header */}
                  <div className="flex items-center justify-between p-4 border-b border-white/10">
                    <div>
                      <h3 className="text-sm font-semibold text-white">Notifications</h3>
                      {unreadCount > 0 && (
                        <p className="text-xs text-white/50 mt-0.5">{unreadCount} unread</p>
                      )}
                    </div>
                    {notifications.length > 0 && (
                      <button
                        onClick={clearAllNotifications}
                        className="text-xs text-white/50 hover:text-white/70 transition-colors"
                      >
                        Clear all
                      </button>
                    )}
                  </div>

                  {/* Notifications List */}
                  <div className="overflow-y-auto max-h-80">
                    {notifications.length === 0 ? (
                      <div className="p-8 text-center">
                        <svg className="w-12 h-12 text-white/20 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                        </svg>
                        <p className="text-sm text-white/50">No notifications</p>
                      </div>
                    ) : (
                      notifications.map((notification) => (
                        <button
                          key={notification.id}
                          onClick={() => markAsRead(notification.id)}
                          className={`w-full text-left p-4 border-b border-white/5 hover:bg-white/5 transition-colors ${
                            !notification.read ? 'bg-white/5' : ''
                          }`}
                        >
                          <div className="flex items-start gap-3">
                            <div className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${
                              !notification.read ? 'bg-blue-500' : 'bg-transparent'
                            }`} />
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium text-white mb-1">
                                {notification.title}
                              </p>
                              <p className="text-xs text-white/60 mb-1">
                                {notification.message}
                              </p>
                              <p className="text-xs text-white/40">
                                {notification.time}
                              </p>
                            </div>
                          </div>
                        </button>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* User Menu */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="w-9 h-9 bg-white/10 rounded-lg flex items-center justify-center hover:bg-white/15 transition-colors"
              >
                <span className="text-sm font-medium">U</span>
              </button>

              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-48 modern-card p-2">
                  <div className="px-3 py-2 text-sm text-white/50 border-b border-white/10 mb-2">
                    User
                  </div>
                  
                  <Link
                    to="/dashboard"
                    className="block px-3 py-2 text-sm text-white/80 hover:bg-white/5 rounded-lg transition-colors"
                    onClick={() => setShowUserMenu(false)}
                  >
                    Search
                  </Link>
                  
                  <Link
                    to="/tracked"
                    className="block px-3 py-2 text-sm text-white/80 hover:bg-white/5 rounded-lg transition-colors"
                    onClick={() => setShowUserMenu(false)}
                  >
                    Tracked ({trackedCount})
                  </Link>
                  
                  <div className="border-t border-white/10 mt-2 pt-2">
                    <button
                      onClick={handleLogout}
                      className="block w-full text-left px-3 py-2 text-sm text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                    >
                      Sign Out
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {(showUserMenu || showNotifications) && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => {
            setShowUserMenu(false);
            setShowNotifications(false);
          }}
        />
      )}
    </nav>
  );
}