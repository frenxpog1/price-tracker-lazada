# Implementation Plan: E-commerce Price Tracker

## Overview

This implementation plan breaks down the E-commerce Price Tracker feature into discrete, incremental coding tasks. The system is a full-stack web application built with Python FastAPI backend, React TypeScript frontend, PostgreSQL database, and Celery for background job processing. Each task builds on previous work, with property-based tests validating universal correctness properties and unit tests covering specific scenarios.

## Tasks

- [x] 1. Set up project infrastructure and core configuration
  - Create project directory structure for backend and frontend
  - Set up Python virtual environment and install core dependencies (FastAPI, SQLAlchemy, Alembic, Celery, Redis, Playwright, BeautifulSoup4, passlib, pytest, hypothesis)
  - Create Docker Compose configuration with PostgreSQL, Redis, backend, celery_worker, celery_beat, and frontend services
  - Configure environment variables and settings management (config.py)
  - Set up database connection and session management (core/database.py)
  - Create Alembic migration configuration
  - Set up structured logging configuration (core/logging.py)
  - Create custom exception classes (core/exceptions.py)
  - _Requirements: 10.1_

- [x] 2. Implement database models and migrations
  - [x] 2.1 Create SQLAlchemy models for User, TrackedProduct, PriceHistory, Notification, and PlatformError
    - Define all table columns, relationships, and constraints
    - Add indexes for user_id, last_checked, and timestamp fields
    - _Requirements: 5.1, 2.3, 3.5, 4.1, 9.4, 10.4, 10.5_
  
  - [ ]* 2.2 Write property test for referential integrity
    - **Property 21: Referential Integrity**
    - **Validates: Requirements 10.4, 10.5**
    - Test that tracked products reference valid users and price history entries reference valid tracked products
  
  - [x] 2.3 Create initial Alembic migration for all tables
    - Generate migration script with all table definitions
    - Test migration up and down
    - _Requirements: 10.1_

- [x] 3. Implement authentication system
  - [x] 3.1 Create security utilities for JWT and password hashing
    - Implement JWT token generation and validation (core/security.py)
    - Implement password hashing with bcrypt
    - _Requirements: 5.1, 5.3_
  
  - [x] 3.2 Create Pydantic schemas for authentication
    - Define UserRegister, UserLogin, UserResponse schemas (schemas/auth.py)
    - Add email and password validation
    - _Requirements: 5.2, 5.3_
  
  - [ ]* 3.3 Write property tests for email and password validation
    - **Property 12: Email Format Validation**
    - **Validates: Requirements 5.2, 7.2**
    - **Property 13: Password Length Validation**
    - **Validates: Requirements 5.3**
  
  - [x] 3.4 Implement UserRepository for database operations
    - Create user CRUD operations (repositories/user_repository.py)
    - _Requirements: 5.1_
  
  - [x] 3.5 Implement AuthService for business logic
    - Create user registration logic with validation (services/auth_service.py)
    - Create user login logic with credential verification
    - Implement token generation
    - _Requirements: 5.1, 5.4, 5.5, 5.6_
  
  - [ ]* 3.6 Write unit tests for authentication service
    - Test successful registration and login
    - Test login with incorrect credentials
    - Test duplicate email registration
    - _Requirements: 5.4, 5.5, 5.6_
  
  - [x] 3.7 Create authentication API endpoints
    - Implement POST /api/auth/register endpoint (api/auth.py)
    - Implement POST /api/auth/login endpoint
    - Implement GET /api/auth/me endpoint with JWT middleware
    - _Requirements: 5.1, 5.4_
  
  - [ ]* 3.8 Write integration tests for authentication endpoints
    - Test complete registration and login flow
    - Test protected endpoint access with valid/invalid tokens
    - _Requirements: 5.1, 5.4, 5.5, 5.6_

- [x] 4. Checkpoint - Ensure authentication tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement web scraping framework
  - [x] 5.1 Create base scraper abstract class
    - Define BaseScraper interface with search() and get_current_price() methods (scrapers/base_scraper.py)
    - Add error handling and logging
    - _Requirements: 1.1, 1.2, 1.3, 3.2_
  
  - [x] 5.2 Implement Lazada scraper
    - Create LazadaScraper class extending BaseScraper (scrapers/lazada_scraper.py)
    - Implement search method with Playwright for dynamic content
    - Implement get_current_price method
    - Add robust selectors with fallbacks
    - _Requirements: 1.1, 6.1, 6.2_
  
  - [x] 5.3 Implement Shopee scraper
    - Create ShopeeScraper class extending BaseScraper (scrapers/shopee_scraper.py)
    - Implement search and get_current_price methods
    - _Requirements: 1.2, 6.1, 6.2_
  
  - [x] 5.4 Implement TikTok Shop scraper
    - Create TikTokScraper class extending BaseScraper (scrapers/tiktok_scraper.py)
    - Implement search and get_current_price methods
    - _Requirements: 1.3, 6.1, 6.2_
  
  - [x] 5.5 Create scraper factory
    - Implement ScraperFactory to instantiate platform-specific scrapers (scrapers/scraper_factory.py)
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [ ]* 5.6 Write unit tests for scrapers
    - Test each scraper with mocked HTML responses
    - Test unavailable product filtering
    - Test error handling for malformed HTML
    - _Requirements: 6.2, 9.1_

- [x] 6. Implement product search functionality
  - [x] 6.1 Create Pydantic schemas for product search
    - Define ProductResult and SearchResults schemas (schemas/product.py)
    - _Requirements: 1.5_
  
  - [x] 6.2 Implement ProductSearchService
    - Create search_all_platforms method with concurrent execution (services/search_service.py)
    - Implement 10-second timeout for search operations
    - Add platform error handling and warning messages
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 6.3, 6.4, 9.1_
  
  - [ ]* 6.3 Write property tests for search functionality
    - **Property 1: Search Result Completeness**
    - **Validates: Requirements 1.5**
    - **Property 14: Unavailable Product Filtering**
    - **Validates: Requirements 6.2**
    - **Property 15: Unicode Query Handling**
    - **Validates: Requirements 6.3**
  
  - [ ]* 6.4 Write unit tests for search service
    - Test empty search results display message
    - Test platform unavailable during search
    - Test timeout handling
    - _Requirements: 1.6, 9.1_
  
  - [x] 6.5 Create product search API endpoint
    - Implement GET /api/products/search endpoint (api/products.py)
    - Add authentication middleware
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  
  - [ ]* 6.6 Write integration tests for search endpoint
    - Test search with mocked scrapers
    - Test authentication requirement
    - _Requirements: 1.1, 1.2, 1.3_

- [x] 7. Checkpoint - Ensure search functionality tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement product tracking functionality
  - [x] 8.1 Create Pydantic schemas for tracking
    - Define TrackedProductCreate, TrackedProductResponse, ThresholdUpdate schemas (schemas/tracking.py)
    - Add validation for positive price values
    - _Requirements: 2.1, 2.2, 8.2_
  
  - [ ]* 8.2 Write property test for price threshold validation
    - **Property 17: Price Threshold Validation**
    - **Validates: Requirements 8.2**
  
  - [x] 8.3 Implement ProductRepository
    - Create CRUD operations for tracked products (repositories/product_repository.py)
    - Implement user-scoped queries
    - _Requirements: 2.3, 2.4, 2.5, 2.6, 5.7_
  
  - [x] 8.4 Implement HistoryRepository
    - Create operations for price history (repositories/history_repository.py)
    - _Requirements: 3.5_
  
  - [x] 8.5 Implement TrackingService
    - Create create_tracked_product method (services/tracking_service.py)
    - Implement get_user_tracked_products method
    - Implement update_threshold method with immediate notification check
    - Implement delete_tracked_product method
    - Add database transaction handling
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 8.1, 8.3, 8.4, 10.2, 10.3_
  
  - [ ]* 8.6 Write property tests for tracking functionality
    - **Property 2: Tracked Product Data Preservation**
    - **Validates: Requirements 2.3**
    - **Property 3: Product Deletion Completeness**
    - **Validates: Requirements 2.5**
    - **Property 4: User Data Isolation**
    - **Validates: Requirements 2.6, 5.7**
    - **Property 18: Updated Threshold Application**
    - **Validates: Requirements 8.3**
  
  - [ ]* 8.7 Write unit tests for tracking service
    - Test database write failure handling
    - Test user data isolation
    - _Requirements: 10.3, 5.7_
  
  - [x] 8.8 Create tracking API endpoints
    - Implement POST /api/tracking/products endpoint (api/tracking.py)
    - Implement GET /api/tracking/products endpoint
    - Implement DELETE /api/tracking/products/{id} endpoint
    - Implement PATCH /api/tracking/products/{id}/threshold endpoint
    - Add authentication and authorization checks
    - _Requirements: 2.1, 2.2, 2.4, 2.5, 8.1_
  
  - [ ]* 8.9 Write integration tests for tracking endpoints
    - Test complete tracking workflow
    - Test authorization boundaries
    - _Requirements: 2.1, 2.2, 2.4, 2.5, 5.7_

- [ ] 9. Implement price history functionality
  - [ ] 9.1 Create Pydantic schemas for price history
    - Define PriceHistoryEntry and PriceHistoryResponse schemas (schemas/product.py)
    - _Requirements: 3.5_
  
  - [ ] 9.2 Create price history API endpoint
    - Implement GET /api/tracking/products/{id}/history endpoint (api/tracking.py)
    - Add authentication and authorization checks
    - _Requirements: 3.5_
  
  - [ ]* 9.3 Write property test for price history recording
    - **Property 5: Price History Recording**
    - **Validates: Requirements 3.5**
  
  - [ ]* 9.4 Write integration test for price history endpoint
    - Test price history retrieval
    - _Requirements: 3.5_

- [ ] 10. Checkpoint - Ensure tracking and history tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Implement notification service
  - [ ] 11.1 Implement NotificationRepository
    - Create operations for notification logging (repositories/notification_repository.py)
    - _Requirements: 4.1, 4.2, 4.3_
  
  - [ ] 11.2 Implement NotificationService
    - Create send_price_drop_notification method (services/notification_service.py)
    - Implement compose_email method with HTML template
    - Configure SMTP client with retry logic
    - Implement notification consolidation logic
    - Add delivery status logging
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 7.3, 7.4_
  
  - [ ]* 11.3 Write property tests for notification functionality
    - **Property 7: Notification Trigger Condition**
    - **Validates: Requirements 4.1, 8.4**
    - **Property 8: Notification Content Completeness**
    - **Validates: Requirements 4.2**
    - **Property 9: Notification Consolidation**
    - **Validates: Requirements 4.4**
    - **Property 10: Notification Idempotence**
    - **Validates: Requirements 4.5**
    - **Property 11: Notification on Threshold Re-crossing**
    - **Validates: Requirements 4.6**
    - **Property 16: Current Email Address Usage**
    - **Validates: Requirements 7.3**
  
  - [ ]* 11.4 Write unit tests for notification service
    - Test email composition
    - Test SMTP error handling
    - Test delivery failure logging
    - _Requirements: 4.2, 7.4_

- [ ] 12. Implement price monitoring service
  - [ ] 12.1 Implement PriceMonitorService
    - Create check_product_price method (services/monitor_service.py)
    - Implement price comparison logic
    - Add price history recording
    - Integrate with NotificationService for price drops
    - Implement retry logic with exponential backoff
    - Add platform error logging
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 9.2, 9.3, 9.4_
  
  - [ ]* 12.2 Write property tests for price monitoring
    - **Property 6: Price Update Persistence**
    - **Validates: Requirements 3.3**
    - **Property 19: Retry with Exponential Backoff**
    - **Validates: Requirements 9.2**
    - **Property 20: Platform Error Logging**
    - **Validates: Requirements 9.4**
  
  - [ ]* 12.3 Write unit tests for price monitoring service
    - Test price check failure and retry
    - Test all retry attempts fail scenario
    - _Requirements: 3.4, 9.3_

- [ ] 13. Implement Celery background tasks
  - [ ] 13.1 Configure Celery application
    - Create Celery app configuration (tasks/celery_app.py)
    - Configure Redis as broker and result backend
    - Set up Celery Beat scheduler
    - _Requirements: 3.1_
  
  - [ ] 13.2 Create price monitoring Celery task
    - Implement check_product_price task (tasks/price_monitor.py)
    - Configure task retries and timeouts
    - Add comprehensive task logging
    - _Requirements: 3.1, 3.2_
  
  - [ ] 13.3 Create scheduled task for checking all products
    - Implement check_all_tracked_products periodic task
    - Configure Celery Beat schedule (every 24 hours)
    - _Requirements: 3.1_
  
  - [ ]* 13.4 Write integration tests for Celery tasks
    - Test task execution with mocked scrapers
    - Test task retry on failure
    - _Requirements: 3.1, 3.2, 9.2_

- [ ] 14. Checkpoint - Ensure monitoring and notification tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 15. Implement user settings functionality
  - [ ] 15.1 Create user settings API endpoint
    - Implement PATCH /api/users/email endpoint (api/users.py)
    - Add email validation
    - Add authentication middleware
    - _Requirements: 7.1, 7.2_
  
  - [ ]* 15.2 Write integration test for email update
    - Test email update and validation
    - _Requirements: 7.1, 7.2_

- [ ] 16. Add debugging and monitoring features
  - [ ] 16.1 Implement request/response logging middleware
    - Create middleware for logging all API requests (main.py)
    - Add request ID tracking
    - _Requirements: All_
  
  - [ ] 16.2 Implement global exception handler
    - Create exception handler with detailed error context (main.py)
    - Return consistent error response format
    - _Requirements: All_
  
  - [ ] 16.3 Add debug endpoints (development only)
    - Create /debug/scrapers/{platform}/test endpoint
    - Create /debug/database/health endpoint
    - Create /debug/notifications/test endpoint
    - _Requirements: All_
  
  - [ ] 16.4 Configure database query logging
    - Set up SQLAlchemy slow query logging
    - _Requirements: All_

- [x] 17. Set up React frontend project
  - [x] 17.1 Initialize React TypeScript project
    - Create React app with TypeScript and Vite
    - Install dependencies (React Router, Axios, Tailwind CSS, React Query)
    - Configure Tailwind CSS
    - _Requirements: All frontend_
  
  - [x] 17.2 Create TypeScript type definitions
    - Define types for auth, product, and tracking (types/)
    - _Requirements: All frontend_
  
  - [x] 17.3 Set up Axios API client
    - Configure Axios with base URL and interceptors (services/api.ts)
    - Add JWT token injection
    - _Requirements: All frontend_
  
  - [x] 17.4 Create authentication context
    - Implement AuthContext with login/logout/register (contexts/AuthContext.tsx)
    - Add token storage in localStorage
    - _Requirements: 5.1, 5.4_

- [x] 18. Implement frontend authentication pages
  - [x] 18.1 Create LoginPage component
    - Build login form with email and password fields (pages/LoginPage.tsx)
    - Add form validation
    - Integrate with authService
    - _Requirements: 5.4, 5.5, 5.6_
  
  - [x] 18.2 Create RegisterPage component
    - Build registration form (pages/RegisterPage.tsx)
    - Add email and password validation
    - Integrate with authService
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [x] 18.3 Create ProtectedRoute component
    - Implement route protection with authentication check
    - Redirect to login if not authenticated
    - _Requirements: 5.7_

- [x] 19. Implement frontend product search
  - [x] 19.1 Create API service methods
    - Implement searchProducts method (services/productService.ts)
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [x] 19.2 Create SearchBar component
    - Build search input with debouncing (components/SearchBar.tsx)
    - Add loading states
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [x] 19.3 Create ProductCard component
    - Display product information (components/ProductCard.tsx)
    - Add "Track" button
    - _Requirements: 1.5_
  
  - [x] 19.4 Create search results display
    - Build search results list in DashboardPage
    - Handle empty results message
    - Display platform warnings
    - _Requirements: 1.5, 1.6, 9.1_

- [x] 20. Implement frontend product tracking
  - [x] 20.1 Create API service methods for tracking
    - Implement trackProduct, getTrackedProducts, deleteTrackedProduct, updateThreshold methods (services/trackingService.ts)
    - _Requirements: 2.1, 2.2, 2.4, 2.5, 8.1_
  
  - [x] 20.2 Create TrackedProductCard component
    - Display tracked product information (components/TrackedProductCard.tsx)
    - Add delete button
    - Show current price and threshold
    - _Requirements: 2.4_
  
  - [x] 20.3 Create ThresholdEditor component
    - Build inline threshold editor (components/ThresholdEditor.tsx)
    - Add validation for positive numbers
    - _Requirements: 8.1, 8.2_
  
  - [x] 20.4 Create PriceChart component
    - Build line chart for price history (components/PriceChart.tsx)
    - Use a charting library (e.g., Recharts)
    - _Requirements: 3.5_
  
  - [x] 20.5 Integrate tracking into DashboardPage
    - Display tracked products list
    - Add track product functionality from search results
    - _Requirements: 2.1, 2.2, 2.4, 2.5_

- [ ] 21. Implement frontend user settings
  - [ ] 21.1 Create UserSettings component
    - Build email update form (components/UserSettings.tsx or pages/DashboardPage.tsx)
    - Add email validation
    - Integrate with API
    - _Requirements: 7.1, 7.2_

- [ ] 22. Add frontend error handling and polish
  - [ ] 22.1 Create ErrorBoundary component
    - Implement error boundary for component errors
    - Add error logging
    - _Requirements: All frontend_
  
  - [ ] 22.2 Add loading states and error messages
    - Implement loading spinners for async operations
    - Display user-friendly error messages
    - _Requirements: All frontend_
  
  - [ ] 22.3 Add responsive design
    - Ensure mobile-friendly layout with Tailwind
    - _Requirements: All frontend_

- [ ] 23. Checkpoint - Ensure frontend integrates with backend
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 24. Create comprehensive test suite
  - [ ]* 24.1 Run all property-based tests
    - Execute all 21 property tests with 100 iterations each
    - Verify all properties hold
    - _Requirements: All_
  
  - [ ]* 24.2 Run all unit tests with coverage
    - Execute unit test suite
    - Verify minimum 80% code coverage
    - _Requirements: All_
  
  - [ ]* 24.3 Run all integration tests
    - Execute integration test suite
    - Verify end-to-end workflows
    - _Requirements: All_

- [ ] 25. Finalize deployment configuration
  - [ ] 25.1 Create production Docker Compose configuration
    - Configure production environment variables
    - Set up health checks
    - _Requirements: All_
  
  - [ ] 25.2 Create deployment documentation
    - Document environment variables
    - Document deployment steps
    - Document monitoring setup
    - _Requirements: All_
  
  - [ ] 25.3 Set up CI/CD pipeline configuration
    - Create GitHub Actions or GitLab CI configuration
    - Add linting, testing, and build steps
    - _Requirements: All_

- [ ] 26. Final checkpoint - Complete system verification
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- Integration tests validate end-to-end workflows
- Checkpoints ensure incremental validation throughout development
- The implementation follows a bottom-up approach: infrastructure → backend services → background jobs → frontend
- All 21 correctness properties from the design document are covered by property-based tests
- Testing tasks are marked optional to allow flexibility in development pace
