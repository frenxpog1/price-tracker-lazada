/**
 * Authentication Context
 * 
 * Provides authentication state and functions throughout the application:
 * - User authentication state (user, isAuthenticated, isLoading)
 * - Login, logout, and register functions
 * - Token storage in localStorage
 * - Automatic authentication restoration on app load
 * 
 * Requirements: 5.1, 5.4
 */

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api from '../services/api';
import { UserLogin, UserRegister, UserResponse } from '../types/auth';

/**
 * User data stored in context
 */
interface User {
  user_id: string;
  email: string;
}

/**
 * Authentication context value
 */
interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: UserLogin) => Promise<void>;
  register: (userData: UserRegister) => Promise<void>;
  logout: () => void;
}

/**
 * Authentication context
 */
const AuthContext = createContext<AuthContextValue | undefined>(undefined);

/**
 * Props for AuthProvider component
 */
interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Authentication Provider Component
 * 
 * Wraps the application and provides authentication state and functions
 * to all child components via React Context.
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Restore authentication state from localStorage on mount
   */
  useEffect(() => {
    const restoreAuth = async () => {
      try {
        // Check if token exists in localStorage
        const token = localStorage.getItem('token');
        const storedUser = localStorage.getItem('user');

        if (token && storedUser) {
          // Verify token is still valid by calling /api/auth/me
          try {
            const response = await api.get<UserResponse>('/auth/me');
            
            // Update user data from server response (in case email changed)
            setUser({
              user_id: response.data.user_id,
              email: response.data.email,
            });
            
            // Update localStorage with fresh user data
            localStorage.setItem('user', JSON.stringify({
              user_id: response.data.user_id,
              email: response.data.email,
            }));
          } catch (error) {
            // Token is invalid or expired, clear storage
            console.error('Token validation failed:', error);
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            setUser(null);
          }
        }
      } catch (error) {
        console.error('Error restoring authentication:', error);
        // Clear potentially corrupted data
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    restoreAuth();
  }, []);

  /**
   * Login function
   * 
   * Authenticates user with email and password.
   * Stores token and user data in localStorage on success.
   * 
   * @param credentials - User login credentials (email, password)
   * @throws Error if login fails
   */
  const login = async (credentials: UserLogin): Promise<void> => {
    try {
      setIsLoading(true);
      
      // Call login API endpoint
      const response = await api.post<UserResponse>('/auth/login', credentials);
      
      const { user_id, email, token } = response.data;
      
      // Store token in localStorage
      localStorage.setItem('token', token);
      
      // Store user data in localStorage
      const userData = { user_id, email };
      localStorage.setItem('user', JSON.stringify(userData));
      
      // Update context state
      setUser(userData);
    } catch (error: any) {
      // Clear any existing auth data on login failure
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setUser(null);
      
      // Re-throw error for component to handle
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Register function
   * 
   * Creates a new user account with email and password.
   * Automatically logs in the user on successful registration.
   * Stores token and user data in localStorage.
   * 
   * @param userData - User registration data (email, password)
   * @throws Error if registration fails
   */
  const register = async (userData: UserRegister): Promise<void> => {
    try {
      setIsLoading(true);
      
      // Call register API endpoint
      const response = await api.post<UserResponse>('/auth/register', userData);
      
      const { user_id, email, token } = response.data;
      
      // Store token in localStorage
      localStorage.setItem('token', token);
      
      // Store user data in localStorage
      const newUser = { user_id, email };
      localStorage.setItem('user', JSON.stringify(newUser));
      
      // Update context state
      setUser(newUser);
    } catch (error: any) {
      // Clear any existing auth data on registration failure
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setUser(null);
      
      // Re-throw error for component to handle
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Logout function
   * 
   * Clears authentication state and removes token and user data
   * from localStorage.
   */
  const logout = (): void => {
    // Clear localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    // Clear context state
    setUser(null);
  };

  /**
   * Computed authentication status
   */
  const isAuthenticated = user !== null;

  /**
   * Context value provided to children
   */
  const value: AuthContextValue = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Custom hook to use authentication context
 * 
 * Must be used within an AuthProvider component.
 * 
 * @returns Authentication context value
 * @throws Error if used outside AuthProvider
 * 
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { user, isAuthenticated, login, logout } = useAuth();
 *   
 *   if (!isAuthenticated) {
 *     return <LoginForm onLogin={login} />;
 *   }
 *   
 *   return (
 *     <div>
 *       <p>Welcome, {user.email}!</p>
 *       <button onClick={logout}>Logout</button>
 *     </div>
 *   );
 * }
 * ```
 */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
}

/**
 * Usage Example:
 * 
 * 1. Wrap your app with AuthProvider in main.tsx or App.tsx:
 * 
 * ```tsx
 * import { AuthProvider } from './contexts/AuthContext';
 * 
 * function App() {
 *   return (
 *     <AuthProvider>
 *       <Router>
 *         <Routes>
 *           <Route path="/login" element={<LoginPage />} />
 *           <Route path="/dashboard" element={<DashboardPage />} />
 *         </Routes>
 *       </Router>
 *     </AuthProvider>
 *   );
 * }
 * ```
 * 
 * 2. Use the useAuth hook in your components:
 * 
 * ```tsx
 * import { useAuth } from '../contexts/AuthContext';
 * 
 * function LoginPage() {
 *   const { login, isLoading } = useAuth();
 *   const navigate = useNavigate();
 *   
 *   const handleSubmit = async (e: React.FormEvent) => {
 *     e.preventDefault();
 *     try {
 *       await login({ email, password });
 *       navigate('/dashboard');
 *     } catch (error) {
 *       console.error('Login failed:', error);
 *     }
 *   };
 *   
 *   return <form onSubmit={handleSubmit}>...</form>;
 * }
 * ```
 * 
 * 3. Protect routes with authentication check:
 * 
 * ```tsx
 * function ProtectedRoute({ children }: { children: ReactNode }) {
 *   const { isAuthenticated, isLoading } = useAuth();
 *   
 *   if (isLoading) {
 *     return <LoadingSpinner />;
 *   }
 *   
 *   if (!isAuthenticated) {
 *     return <Navigate to="/login" replace />;
 *   }
 *   
 *   return <>{children}</>;
 * }
 * ```
 */
