/**
 * RegisterPage Component
 * 
 * Provides user registration interface with:
 * - Email and password input fields with validation
 * - Email format validation (Requirement 5.2)
 * - Password length validation - minimum 8 characters (Requirement 5.3)
 * - Integration with AuthContext for registration functionality
 * - Loading states during registration
 * - Error message display for failed registration (e.g., duplicate email)
 * - Redirect to dashboard on successful registration
 * - Link to login page
 * 
 * Requirements: 5.1, 5.2, 5.3
 */

import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [emailError, setEmailError] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [confirmPasswordError, setConfirmPasswordError] = useState('')
  
  const { register, isLoading } = useAuth()
  const navigate = useNavigate()

  /**
   * Validates email format
   * Requirements: 5.2
   */
  const validateEmail = (email: string): boolean => {
    if (!email) {
      setEmailError('Email is required')
      return false
    }
    
    // Basic email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      setEmailError('Please enter a valid email address')
      return false
    }
    
    setEmailError('')
    return true
  }

  /**
   * Validates password requirements
   * Requirements: 5.3 - Minimum 8 characters
   */
  const validatePassword = (password: string): boolean => {
    if (!password) {
      setPasswordError('Password is required')
      return false
    }
    
    if (password.length < 8) {
      setPasswordError('Password must be at least 8 characters')
      return false
    }
    
    setPasswordError('')
    return true
  }

  /**
   * Validates password confirmation
   */
  const validateConfirmPassword = (confirmPassword: string): boolean => {
    if (!confirmPassword) {
      setConfirmPasswordError('Please confirm your password')
      return false
    }
    
    if (confirmPassword !== password) {
      setConfirmPasswordError('Passwords do not match')
      return false
    }
    
    setConfirmPasswordError('')
    return true
  }

  /**
   * Handles form submission
   * Validates inputs, calls register service, and redirects on success
   * Requirements: 5.1, 5.2, 5.3
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Clear previous errors
    setError('')
    setEmailError('')
    setPasswordError('')
    setConfirmPasswordError('')
    
    // Validate inputs
    const isEmailValid = validateEmail(email)
    const isPasswordValid = validatePassword(password)
    const isConfirmPasswordValid = validateConfirmPassword(confirmPassword)
    
    if (!isEmailValid || !isPasswordValid || !isConfirmPasswordValid) {
      return
    }
    
    try {
      // Call register function from AuthContext
      await register({ email, password })
      
      // Redirect to dashboard on successful registration
      navigate('/dashboard')
    } catch (err: any) {
      // Display error message for failed registration
      if (err.response?.status === 400 && err.response?.data?.detail?.includes('already exists')) {
        setError('An account with this email already exists. Please login instead.')
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else {
        setError('An error occurred during registration. Please try again.')
      }
      
      console.error('Registration error:', err)
    }
  }

  /**
   * Handles email input change with validation
   */
  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setEmail(value)
    
    // Clear email error when user starts typing
    if (emailError) {
      setEmailError('')
    }
    
    // Clear general error when user starts typing
    if (error) {
      setError('')
    }
  }

  /**
   * Handles password input change with validation
   */
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setPassword(value)
    
    // Clear password error when user starts typing
    if (passwordError) {
      setPasswordError('')
    }
    
    // Clear general error when user starts typing
    if (error) {
      setError('')
    }
    
    // Re-validate confirm password if it's already filled
    if (confirmPassword && confirmPasswordError) {
      setConfirmPasswordError('')
    }
  }

  /**
   * Handles confirm password input change with validation
   */
  const handleConfirmPasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setConfirmPassword(value)
    
    // Clear confirm password error when user starts typing
    if (confirmPasswordError) {
      setConfirmPasswordError('')
    }
    
    // Clear general error when user starts typing
    if (error) {
      setError('')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 via-primary-600 to-purple-600 px-4">
      <div className="w-full max-w-md">
        {/* Logo and Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-white rounded-2xl shadow-lg mb-4">
            <svg className="w-10 h-10 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">PriceTracker</h1>
          <p className="text-primary-100">Start tracking prices today</p>
        </div>

        {/* Register Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <h2 className="text-2xl font-bold text-neutral-900 mb-6">Create Account</h2>
          
          {/* General Error Message */}
          {error && (
            <div className="mb-5 p-4 bg-error-50 border border-error-200 rounded-lg">
              <div className="flex items-start">
                <svg className="h-5 w-5 text-error-500 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-sm text-error-700">{error}</p>
              </div>
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Email Input */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-neutral-700 mb-2">
                Email Address
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </div>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={handleEmailChange}
                  onBlur={() => validateEmail(email)}
                  className={`block w-full pl-10 pr-3 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-fast ${
                    emailError ? 'border-error-500' : 'border-neutral-200'
                  }`}
                  placeholder="you@example.com"
                  required
                  disabled={isLoading}
                />
              </div>
              {emailError && (
                <p className="mt-2 text-sm text-error-600">{emailError}</p>
              )}
            </div>

            {/* Password Input */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-neutral-700 mb-2">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={handlePasswordChange}
                  onBlur={() => validatePassword(password)}
                  className={`block w-full pl-10 pr-3 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-fast ${
                    passwordError ? 'border-error-500' : 'border-neutral-200'
                  }`}
                  placeholder="••••••••"
                  minLength={8}
                  required
                  disabled={isLoading}
                />
              </div>
              {passwordError && (
                <p className="mt-2 text-sm text-error-600">{passwordError}</p>
              )}
              {!passwordError && (
                <p className="mt-1 text-xs text-neutral-500">Must be at least 8 characters</p>
              )}
            </div>

            {/* Confirm Password Input */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-neutral-700 mb-2">
                Confirm Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={handleConfirmPasswordChange}
                  onBlur={() => validateConfirmPassword(confirmPassword)}
                  className={`block w-full pl-10 pr-3 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-fast ${
                    confirmPasswordError ? 'border-error-500' : 'border-neutral-200'
                  }`}
                  placeholder="••••••••"
                  required
                  disabled={isLoading}
                />
              </div>
              {confirmPasswordError && (
                <p className="mt-2 text-sm text-error-600">{confirmPasswordError}</p>
              )}
            </div>

            {/* Register Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-primary-500 text-white py-3 px-4 rounded-lg font-semibold hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-fast disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Creating account...
                </span>
              ) : (
                'Create Account'
              )}
            </button>
          </form>

          {/* Login Link */}
          <div className="mt-6 text-center">
            <p className="text-sm text-neutral-600">
              Already have an account?{' '}
              <Link to="/login" className="font-semibold text-primary-500 hover:text-primary-600 transition-fast">
                Sign in
              </Link>
            </p>
          </div>
        </div>

        {/* Footer */}
        <p className="mt-8 text-center text-sm text-primary-100">
          Free forever • No credit card required
        </p>
      </div>
    </div>
  )
}
