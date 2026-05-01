# Design Document: E-commerce Price Tracker

## Overview

The E-commerce Price Tracker is a full-stack web application that enables users to monitor product prices across multiple e-commerce platforms (Lazada, Shopee, TikTok Shop) and receive email notifications when prices drop below user-defined thresholds.

### Technology Stack

**Backend:**
- **Framework**: Python 3.11+ with FastAPI
- **Task Queue**: Celery with Redis as message broker
- **Web Scraping**: Playwright for dynamic content, BeautifulSoup4 for HTML parsing
- **Authentication**: JWT tokens with passlib for password hashing
- **Email**: SMTP with Python's smtplib (compatible with Gmail, Outlook free tiers)

**Frontend:**
- **Framework**: React 18+ with TypeScript
- **State Management**: React Context API + React Query for server state
- **UI Library**: Tailwind CSS for styling
- **HTTP Client**: Axios

**Database:**
- **Primary Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy with Alembic for migrations

**Infrastructure:**
- **Containerization**: Docker and Docker Compose
- **Deployment**: Can run on free tiers (Railway, Render, fly.io) or self-hosted VPS

### System Architecture

The system follows a three-tier architecture with background job processing:

1. **Presentation Layer**: React SPA communicating via REST API
2. **Application Layer**: FastAPI backend handling business logic and API endpoints
3. **Data Layer**: PostgreSQL database with SQLAlchemy ORM
4. **Background Processing**: Celery workers for scheduled price monitoring

```mermaid
graph TB
    subgraph "Client Layer"
        UI[React Frontend]
    end
    
    subgraph "Application Layer"
        API[FastAPI Backend]
        Auth[Authentication Service]
        Search[Product Search Service]
        Track[Tracking Service]
    end
    
    subgraph "Background Processing"
        Celery[Celery Workers]
        Redis[Redis Broker]
        Monitor[Price Monitor]
        Notifier[Notification Service]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL)]
    end
    
    subgraph "External Services"
        Lazada[Lazada]
        Shopee[Shopee]
        TikTok[TikTok Shop]
        SMTP[SMTP Email]
    end
    
    UI -->|REST API| API
    API --> Auth
    API --> Search
    API --> Track
    API --> DB
    
    Search -->|Scrape| Lazada
    Search -->|Scrape| Shopee
    Search -->|Scrape| TikTok
    
    Celery --> Redis
    Celery --> Monitor
    Monitor --> DB
    Monitor -->|Scrape| Lazada
    Monitor -->|Scrape| Shopee
    Monitor -->|Scrape| TikTok
    Monitor --> Notifier
    Notifier --> SMTP
    Notifier --> DB
```

## Architecture

### Layered Architecture

**1. API Layer (FastAPI)**
- RESTful endpoints for all user operations
- JWT-based authentication middleware
- Request validation using Pydantic models
- CORS configuration for frontend communication
- Rate limiting to prevent abuse

**2. Service Layer**
- **AuthService**: User registration, login, token management
- **ProductSearchService**: Multi-platform product search orchestration
- **TrackingService**: CRUD operations for tracked products
- **ScraperService**: Platform-specific web scraping logic
- **PriceMonitorService**: Scheduled price checking logic
- **NotificationService**: Email composition and delivery

**3. Data Access Layer**
- SQLAlchemy models and repositories
- Database session management
- Transaction handling
- Query optimization

**4. Background Job Layer**
- Celery tasks for periodic price monitoring
- Celery beat scheduler for task scheduling
- Redis as message broker and result backend

### Design Patterns

**Repository Pattern**: Abstracts database operations behind repository interfaces
**Service Pattern**: Encapsulates business logic in service classes
**Factory Pattern**: Creates platform-specific scrapers
**Strategy Pattern**: Different scraping strategies per platform
**Observer Pattern**: Price change detection triggers notifications

### Scalability Considerations

- **Horizontal Scaling**: Stateless API design allows multiple FastAPI instances behind load balancer
- **Worker Scaling**: Multiple Celery workers can process price checks in parallel
- **Database Connection Pooling**: SQLAlchemy connection pool prevents connection exhaustion
- **Caching**: Redis can cache search results and reduce scraping load
- **Rate Limiting**: Prevents overwhelming external e-commerce platforms

## Modularity and Debugging

### Modular Project Structure

The codebase is organized into independent, loosely-coupled modules that can be developed, tested, and debugged in isolation:

```
backend/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration management
│   ├── dependencies.py            # Dependency injection
│   │
│   ├── api/                       # API Layer (Routes)
│   │   ├── __init__.py
│   │   ├── auth.py                # Authentication endpoints
│   │   ├── products.py            # Product search endpoints
│   │   ├── tracking.py            # Tracking endpoints
│   │   └── users.py               # User settings endpoints
│   │
│   ├── services/                  # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Authentication logic
│   │   ├── search_service.py      # Product search orchestration
│   │   ├── tracking_service.py    # Tracking CRUD operations
│   │   ├── monitor_service.py     # Price monitoring logic
│   │   └── notification_service.py # Email notification logic
│   │
│   ├── scrapers/                  # Web Scraping Layer
│   │   ├── __init__.py
│   │   ├── base_scraper.py        # Abstract base scraper
│   │   ├── scraper_factory.py     # Factory for creating scrapers
│   │   ├── lazada_scraper.py      # Lazada-specific scraper
│   │   ├── shopee_scraper.py      # Shopee-specific scraper
│   │   └── tiktok_scraper.py      # TikTok Shop-specific scraper
│   │
│   ├── repositories/              # Data Access Layer
│   │   ├── __init__.py
│   │   ├── user_repository.py     # User data operations
│   │   ├── product_repository.py  # Tracked product operations
│   │   ├── history_repository.py  # Price history operations
│   │   └── notification_repository.py # Notification log operations
│   │
│   ├── models/                    # Database Models
│   │   ├── __init__.py
│   │   ├── user.py                # User model
│   │   ├── tracked_product.py     # TrackedProduct model
│   │   ├── price_history.py       # PriceHistory model
│   │   └── notification.py        # Notification model
│   │
│   ├── schemas/                   # Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── auth.py                # Auth request/response schemas
│   │   ├── product.py             # Product schemas
│   │   └── tracking.py            # Tracking schemas
│   │
│   ├── core/                      # Core Utilities
│   │   ├── __init__.py
│   │   ├── security.py            # JWT, password hashing
│   │   ├── database.py            # Database connection
│   │   ├── logging.py             # Logging configuration
│   │   └── exceptions.py          # Custom exceptions
│   │
│   └── tasks/                     # Celery Tasks
│       ├── __init__.py
│       ├── celery_app.py          # Celery configuration
│       └── price_monitor.py       # Price monitoring tasks
│
├── alembic/                       # Database Migrations
│   ├── versions/
│   └── env.py
│
├── tests/                         # Test Suite
│   ├── unit/
│   ├── property/
│   ├── integration/
│   └── fixtures/
│
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker configuration
└── pytest.ini                     # Pytest configuration

frontend/
├── src/
│   ├── App.tsx                    # Main app component
│   ├── main.tsx                   # Entry point
│   │
│   ├── components/                # Reusable UI Components
│   │   ├── SearchBar.tsx
│   │   ├── ProductCard.tsx
│   │   ├── TrackedProductCard.tsx
│   │   ├── PriceChart.tsx
│   │   └── ThresholdEditor.tsx
│   │
│   ├── pages/                     # Page Components
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   └── DashboardPage.tsx
│   │
│   ├── services/                  # API Client Layer
│   │   ├── api.ts                 # Axios configuration
│   │   ├── authService.ts         # Auth API calls
│   │   ├── productService.ts      # Product API calls
│   │   └── trackingService.ts     # Tracking API calls
│   │
│   ├── contexts/                  # React Contexts
│   │   └── AuthContext.tsx        # Authentication state
│   │
│   ├── hooks/                     # Custom React Hooks
│   │   ├── useAuth.ts
│   │   ├── useProducts.ts
│   │   └── useTracking.ts
│   │
│   ├── types/                     # TypeScript Types
│   │   ├── auth.ts
│   │   ├── product.ts
│   │   └── tracking.ts
│   │
│   └── utils/                     # Utility Functions
│       ├── formatters.ts
│       └── validators.ts
│
├── package.json
└── tsconfig.json
```

### Module Independence Principles

**1. Single Responsibility**
- Each module has one clear purpose
- Services handle business logic only
- Repositories handle data access only
- Scrapers handle platform-specific scraping only
- API routes handle HTTP request/response only

**2. Dependency Injection**
- Services receive dependencies through constructor injection
- Makes testing easier (can inject mocks)
- Reduces coupling between modules
- Example:
```python
class TrackingService:
    def __init__(
        self, 
        product_repo: ProductRepository,
        history_repo: HistoryRepository,
        notification_service: NotificationService
    ):
        self.product_repo = product_repo
        self.history_repo = history_repo
        self.notification_service = notification_service
```

**3. Interface-Based Design**
- Abstract base classes define contracts
- Concrete implementations can be swapped
- Example: `BaseScraper` interface allows adding new platforms without changing existing code

**4. Clear Module Boundaries**
- API layer never directly accesses database
- Services never directly access external APIs (use scrapers)
- Repositories never contain business logic
- Each layer only depends on the layer below it

### Debugging Features

**1. Structured Logging**

Every module includes comprehensive logging with context:

```python
import logging
from app.core.logging import get_logger

logger = get_logger(__name__)

class LazadaScraper(BaseScraper):
    async def search(self, query: str) -> List[ProductResult]:
        logger.info(
            "Starting Lazada search",
            extra={
                "platform": "lazada",
                "query": query,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        try:
            results = await self._perform_search(query)
            logger.info(
                "Lazada search completed",
                extra={
                    "platform": "lazada",
                    "query": query,
                    "result_count": len(results)
                }
            )
            return results
        except Exception as e:
            logger.error(
                "Lazada search failed",
                extra={
                    "platform": "lazada",
                    "query": query,
                    "error": str(e),
                    "error_type": type(e).__name__
                },
                exc_info=True
            )
            raise
```

**2. Debug Endpoints**

Development environment includes debug endpoints:

```python
# Only available in development mode
if settings.DEBUG:
    @app.get("/debug/scrapers/{platform}/test")
    async def test_scraper(platform: str, query: str):
        """Test a specific scraper in isolation"""
        scraper = scraper_factory.get_scraper(platform)
        results = await scraper.search(query)
        return {"platform": platform, "results": results}
    
    @app.get("/debug/database/health")
    async def database_health():
        """Check database connection and table status"""
        # Return database connection info, table counts, etc.
        pass
    
    @app.post("/debug/notifications/test")
    async def test_notification(email: str):
        """Send a test notification email"""
        # Send test email to verify SMTP configuration
        pass
```

**3. Request/Response Logging**

Middleware logs all API requests and responses:

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    
    logger.info(
        "Incoming request",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host
        }
    )
    
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        "Request completed",
        extra={
            "request_id": request_id,
            "status_code": response.status_code,
            "duration_ms": duration * 1000
        }
    )
    
    return response
```

**4. Error Tracking**

Custom exception handler provides detailed error context:

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception",
        extra={
            "path": request.url.path,
            "method": request.method,
            "error": str(exc),
            "error_type": type(exc).__name__,
            "traceback": traceback.format_exc()
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "request_id": request.state.request_id
            }
        }
    )
```

**5. Database Query Logging**

SQLAlchemy configured to log slow queries:

```python
# Log queries that take longer than 1 second
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# In production, log only slow queries
if not settings.DEBUG:
    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())
    
    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info['query_start_time'].pop(-1)
        if total > 1.0:  # Log queries slower than 1 second
            logger.warning(
                "Slow query detected",
                extra={
                    "duration_seconds": total,
                    "query": statement[:200]  # First 200 chars
                }
            )
```

**6. Celery Task Monitoring**

Celery tasks include detailed logging and monitoring:

```python
@celery_app.task(bind=True, max_retries=3)
def check_product_price(self, tracked_product_id: str):
    logger.info(
        "Starting price check",
        extra={
            "task_id": self.request.id,
            "product_id": tracked_product_id,
            "retry_count": self.request.retries
        }
    )
    
    try:
        result = monitor_service.check_product_price(tracked_product_id)
        
        logger.info(
            "Price check completed",
            extra={
                "task_id": self.request.id,
                "product_id": tracked_product_id,
                "old_price": result.old_price,
                "new_price": result.new_price,
                "notification_sent": result.notification_sent
            }
        )
        
        return result
    except Exception as exc:
        logger.error(
            "Price check failed",
            extra={
                "task_id": self.request.id,
                "product_id": tracked_product_id,
                "error": str(exc),
                "retry_count": self.request.retries
            },
            exc_info=True
        )
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

**7. Frontend Error Boundaries**

React error boundaries catch and log component errors:

```typescript
class ErrorBoundary extends React.Component {
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Component error:', {
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
      timestamp: new Date().toISOString()
    });
    
    // Send to error tracking service in production
    if (import.meta.env.PROD) {
      // Send to Sentry, LogRocket, etc.
    }
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

**8. Development Tools**

- **Hot Reload**: FastAPI auto-reload and React HMR for instant feedback
- **Interactive API Docs**: FastAPI automatic OpenAPI/Swagger UI at `/docs`
- **Database Admin**: Optional pgAdmin container for database inspection
- **Redis Commander**: Optional Redis GUI for queue inspection
- **Flower**: Celery monitoring dashboard at `/flower`

### Debugging Workflow Examples

**Example 1: Debugging a Failed Scraper**

1. Check logs for scraper errors: `docker logs backend | grep "lazada_scraper"`
2. Use debug endpoint to test scraper in isolation: `GET /debug/scrapers/lazada/test?query=laptop`
3. Inspect HTML response in scraper code with breakpoint
4. Update selectors and retry
5. Run unit tests: `pytest tests/unit/scrapers/test_lazada_scraper.py -v`

**Example 2: Debugging Missing Notifications**

1. Check notification service logs: `docker logs backend | grep "notification_service"`
2. Verify email configuration: `GET /debug/notifications/test`
3. Check Celery task status: Open Flower dashboard at `http://localhost:5555`
4. Inspect notification table: `SELECT * FROM notifications WHERE user_id = '...'`
5. Check SMTP logs for delivery failures

**Example 3: Debugging Slow API Response**

1. Check request logs for duration: `docker logs backend | grep "duration_ms"`
2. Check slow query logs: `docker logs backend | grep "Slow query"`
3. Use database EXPLAIN to analyze query: `EXPLAIN ANALYZE SELECT ...`
4. Add database indexes if needed
5. Profile code with cProfile if needed

### Module Testing in Isolation

Each module can be tested independently:

```python
# Test scraper without database or API
def test_lazada_scraper():
    scraper = LazadaScraper()
    results = await scraper.search("laptop")
    assert len(results) > 0

# Test service with mocked repository
def test_tracking_service():
    mock_repo = Mock(spec=ProductRepository)
    service = TrackingService(product_repo=mock_repo)
    # Test service logic without real database

# Test API endpoint with mocked service
def test_tracking_endpoint():
    mock_service = Mock(spec=TrackingService)
    client = TestClient(app)
    # Test endpoint without real service
```

This modular structure ensures:
- **Easy debugging**: Isolate and test individual components
- **Fast development**: Work on one module without affecting others
- **Simple maintenance**: Update one module without breaking others
- **Clear ownership**: Each module has a clear purpose and responsibility

## Components and Interfaces

### 1. API Endpoints

#### Authentication Endpoints
```
POST /api/auth/register
  Request: { email: string, password: string }
  Response: { user_id: string, email: string, token: string }

POST /api/auth/login
  Request: { email: string, password: string }
  Response: { user_id: string, email: string, token: string }

GET /api/auth/me
  Headers: { Authorization: "Bearer <token>" }
  Response: { user_id: string, email: string }
```

#### Product Search Endpoints
```
GET /api/products/search?q={query}
  Headers: { Authorization: "Bearer <token>" }
  Response: {
    results: [
      {
        platform: string,
        product_name: string,
        current_price: number,
        currency: string,
        product_url: string,
        image_url: string
      }
    ],
    warnings: string[]
  }
```

#### Tracking Endpoints
```
POST /api/tracking/products
  Headers: { Authorization: "Bearer <token>" }
  Request: {
    platform: string,
    product_name: string,
    product_url: string,
    current_price: number,
    price_threshold: number
  }
  Response: { tracked_product_id: string, ...product_data }

GET /api/tracking/products
  Headers: { Authorization: "Bearer <token>" }
  Response: {
    tracked_products: [
      {
        id: string,
        platform: string,
        product_name: string,
        product_url: string,
        current_price: number,
        price_threshold: number,
        created_at: timestamp,
        last_checked: timestamp
      }
    ]
  }

DELETE /api/tracking/products/{id}
  Headers: { Authorization: "Bearer <token>" }
  Response: { success: boolean }

PATCH /api/tracking/products/{id}/threshold
  Headers: { Authorization: "Bearer <token>" }
  Request: { price_threshold: number }
  Response: { tracked_product_id: string, new_threshold: number }
```

#### User Settings Endpoints
```
PATCH /api/users/email
  Headers: { Authorization: "Bearer <token>" }
  Request: { email: string }
  Response: { user_id: string, email: string }
```

#### Price History Endpoints
```
GET /api/tracking/products/{id}/history
  Headers: { Authorization: "Bearer <token>" }
  Response: {
    history: [
      {
        price: number,
        checked_at: timestamp
      }
    ]
  }
```

### 2. Service Interfaces

#### ProductSearchService
```python
class ProductSearchService:
    async def search_all_platforms(
        self, 
        query: str
    ) -> SearchResults:
        """
        Searches all platforms concurrently and aggregates results.
        Returns results within 10 seconds or times out.
        """
        pass
    
    async def search_platform(
        self, 
        platform: Platform, 
        query: str
    ) -> List[ProductResult]:
        """
        Searches a specific platform using appropriate scraper.
        """
        pass
```

#### ScraperService
```python
class ScraperService:
    def get_scraper(self, platform: Platform) -> BaseScraper:
        """Factory method to get platform-specific scraper."""
        pass

class BaseScraper(ABC):
    @abstractmethod
    async def search(self, query: str) -> List[ProductResult]:
        """Search for products on the platform."""
        pass
    
    @abstractmethod
    async def get_current_price(self, product_url: str) -> Optional[float]:
        """Get current price for a specific product URL."""
        pass
```

#### PriceMonitorService
```python
class PriceMonitorService:
    async def check_all_tracked_products(self) -> None:
        """
        Celery task that checks all tracked products.
        Runs every 24 hours via Celery Beat.
        """
        pass
    
    async def check_product_price(
        self, 
        tracked_product_id: str
    ) -> PriceCheckResult:
        """
        Checks a single product's current price.
        Updates database and triggers notification if needed.
        """
        pass
    
    async def retry_with_backoff(
        self, 
        func: Callable, 
        max_retries: int = 3
    ) -> Any:
        """
        Retries a function with exponential backoff.
        """
        pass
```

#### NotificationService
```python
class NotificationService:
    async def send_price_drop_notification(
        self, 
        user_email: str,
        price_drops: List[PriceDrop]
    ) -> bool:
        """
        Sends email notification for price drops.
        Consolidates multiple drops into single email.
        """
        pass
    
    def compose_email(
        self, 
        price_drops: List[PriceDrop]
    ) -> EmailMessage:
        """
        Composes HTML email with price drop details.
        """
        pass
```

#### TrackingService
```python
class TrackingService:
    async def create_tracked_product(
        self, 
        user_id: str,
        product_data: TrackedProductCreate
    ) -> TrackedProduct:
        """Creates a new tracked product for user."""
        pass
    
    async def get_user_tracked_products(
        self, 
        user_id: str
    ) -> List[TrackedProduct]:
        """Retrieves all tracked products for a user."""
        pass
    
    async def update_threshold(
        self, 
        tracked_product_id: str,
        user_id: str,
        new_threshold: float
    ) -> TrackedProduct:
        """
        Updates price threshold and checks if immediate 
        notification is needed.
        """
        pass
    
    async def delete_tracked_product(
        self, 
        tracked_product_id: str,
        user_id: str
    ) -> bool:
        """Deletes a tracked product."""
        pass
```

### 3. Frontend Components

```
App
├── AuthProvider (Context)
├── Router
│   ├── LoginPage
│   ├── RegisterPage
│   ├── DashboardPage
│   │   ├── SearchBar
│   │   ├── SearchResults
│   │   │   └── ProductCard
│   │   ├── TrackedProductsList
│   │   │   └── TrackedProductCard
│   │   │       ├── PriceChart
│   │   │       └── ThresholdEditor
│   │   └── UserSettings
│   └── ProtectedRoute
```

**Key Frontend Components:**

- **SearchBar**: Input with debounced search, loading states
- **ProductCard**: Displays search result with "Track" button
- **TrackedProductCard**: Shows tracked product with current price, threshold, price history chart, edit/delete actions
- **PriceChart**: Line chart showing price history over time
- **ThresholdEditor**: Inline editor for updating price threshold
- **UserSettings**: Form for updating email address

## Modern UI Design Specifications

### Design Philosophy

The UI follows modern web design principles with emphasis on:
- **Clean & Minimal**: Uncluttered interface with plenty of white space
- **User-Friendly**: Intuitive navigation and clear visual hierarchy
- **Responsive**: Mobile-first design that works on all screen sizes
- **Accessible**: WCAG 2.1 AA compliant with proper contrast and keyboard navigation
- **Delightful**: Smooth animations and micro-interactions

### Design System

#### Color Palette

**Primary Colors:**
```css
--primary-50: #eff6ff;    /* Light blue background */
--primary-100: #dbeafe;   /* Hover states */
--primary-500: #3b82f6;   /* Primary actions, links */
--primary-600: #2563eb;   /* Primary hover */
--primary-700: #1d4ed8;   /* Primary active */
```

**Semantic Colors:**
```css
--success-50: #f0fdf4;    /* Success background */
--success-500: #22c55e;   /* Price drop indicator */
--success-600: #16a34a;   /* Success hover */

--warning-50: #fffbeb;    /* Warning background */
--warning-500: #f59e0b;   /* Price increase indicator */
--warning-600: #d97706;   /* Warning hover */

--error-50: #fef2f2;      /* Error background */
--error-500: #ef4444;     /* Error states */
--error-600: #dc2626;     /* Error hover */

--neutral-50: #f9fafb;    /* Page background */
--neutral-100: #f3f4f6;   /* Card background */
--neutral-200: #e5e7eb;   /* Borders */
--neutral-400: #9ca3af;   /* Placeholder text */
--neutral-600: #4b5563;   /* Secondary text */
--neutral-900: #111827;   /* Primary text */
```

#### Typography

**Font Family:**
```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
```

**Font Sizes:**
```css
--text-xs: 0.75rem;      /* 12px - Labels, captions */
--text-sm: 0.875rem;     /* 14px - Secondary text */
--text-base: 1rem;       /* 16px - Body text */
--text-lg: 1.125rem;     /* 18px - Emphasized text */
--text-xl: 1.25rem;      /* 20px - Card titles */
--text-2xl: 1.5rem;      /* 24px - Section headings */
--text-3xl: 1.875rem;    /* 30px - Page titles */
--text-4xl: 2.25rem;     /* 36px - Hero text */
```

**Font Weights:**
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

#### Spacing

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

#### Border Radius

```css
--radius-sm: 0.375rem;   /* 6px - Buttons, inputs */
--radius-md: 0.5rem;     /* 8px - Cards */
--radius-lg: 0.75rem;    /* 12px - Modals */
--radius-xl: 1rem;       /* 16px - Large cards */
--radius-full: 9999px;   /* Circular elements */
```

#### Shadows

```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
```

#### Animations

```css
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
```

### Page Layouts

#### 1. Login/Register Pages

**Layout:**
- Centered card on gradient background
- Split layout on desktop (left: branding, right: form)
- Single column on mobile
- Smooth transitions between login/register

**Visual Elements:**
```
┌─────────────────────────────────────────┐
│  [Gradient Background]                  │
│                                         │
│    ┌─────────────────────────────┐     │
│    │  🎯 PriceTracker            │     │
│    │                             │     │
│    │  Welcome Back               │     │
│    │                             │     │
│    │  [Email Input]              │     │
│    │  [Password Input]           │     │
│    │                             │     │
│    │  [Login Button - Primary]   │     │
│    │                             │     │
│    │  Don't have an account?     │     │
│    │  [Sign up - Link]           │     │
│    └─────────────────────────────┘     │
│                                         │
└─────────────────────────────────────────┘
```

**Design Details:**
- Card: White background, rounded-xl, shadow-xl
- Gradient background: Blue to purple gradient
- Logo: Modern icon with brand name
- Inputs: Large, rounded-md, with icons
- Button: Full width, rounded-md, primary color
- Links: Primary color, hover underline

#### 2. Dashboard Page

**Layout:**
- Top navigation bar with logo, search, and user menu
- Main content area with search results and tracked products
- Responsive grid layout (1 column mobile, 2-3 columns desktop)
- Sticky header on scroll

**Visual Elements:**
```
┌─────────────────────────────────────────────────────────┐
│ 🎯 PriceTracker    [Search Bar]         [User Menu ▾]  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Track Your Favorite Products                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 🔍 Search products across Lazada, Shopee...    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Search Results (3)                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ [Image]  │  │ [Image]  │  │ [Image]  │            │
│  │ Product  │  │ Product  │  │ Product  │            │
│  │ $99.99   │  │ $149.99  │  │ $79.99   │            │
│  │ [Track]  │  │ [Track]  │  │ [Track]  │            │
│  └──────────┘  └──────────┘  └──────────┘            │
│                                                         │
│  Your Tracked Products (5)                             │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Image] Laptop ASUS ROG                         │   │
│  │         Current: $899.99  Target: $850.00      │   │
│  │         [Price Chart ───────]                   │   │
│  │         [Edit] [Delete]                         │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Image] iPhone 15 Pro                           │   │
│  │         Current: $999.99  Target: $950.00      │   │
│  │         ↓ $50 below target! 🎉                  │   │
│  │         [Price Chart ───────]                   │   │
│  │         [Edit] [Delete]                         │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Design Details:**
- Navigation: White background, shadow-sm, sticky
- Search bar: Large, prominent, with icon and loading spinner
- Product cards: White background, rounded-lg, shadow-md, hover lift effect
- Price indicators: Green for below target, orange for above
- Charts: Smooth line charts with gradient fill
- Buttons: Rounded-md, appropriate colors (primary for track, red for delete)

### Component Specifications

#### SearchBar Component

**Visual Design:**
```
┌─────────────────────────────────────────────────────┐
│ 🔍  Search products...                    [Spinner] │
└─────────────────────────────────────────────────────┘
```

**Specifications:**
- Height: 56px (large, easy to tap)
- Border: 2px solid neutral-200, focus: primary-500
- Border radius: rounded-lg
- Icon: Search icon (left), loading spinner (right when searching)
- Placeholder: "Search products across Lazada, Shopee, TikTok Shop..."
- Debounce: 500ms
- Animation: Smooth border color transition on focus

#### ProductCard Component

**Visual Design:**
```
┌─────────────────────────────┐
│  ┌───────────────────────┐  │
│  │                       │  │
│  │   [Product Image]     │  │
│  │                       │  │
│  └───────────────────────┘  │
│                             │
│  Product Name Here          │
│  Platform: Lazada           │
│                             │
│  $99.99                     │
│                             │
│  [Track This Product]       │
│                             │
└─────────────────────────────┘
```

**Specifications:**
- Card: White background, rounded-lg, shadow-md
- Hover: Lift effect (translateY(-4px)), shadow-lg
- Image: Aspect ratio 1:1, rounded-md, object-fit cover
- Product name: text-lg, font-semibold, 2 lines max with ellipsis
- Platform badge: Small pill badge with platform color
- Price: text-2xl, font-bold, primary color
- Button: Full width, primary color, rounded-md
- Transition: All 200ms ease

#### TrackedProductCard Component

**Visual Design:**
```
┌─────────────────────────────────────────────────────┐
│  ┌────┐  Laptop ASUS ROG Strix G15              ⋮  │
│  │IMG │  Platform: Lazada                           │
│  └────┘                                             │
│                                                     │
│  Current Price    Target Price    Status           │
│  $899.99          $850.00         ↑ Above target   │
│                                                     │
│  Price History (Last 30 Days)                      │
│  ┌─────────────────────────────────────────────┐   │
│  │     ╱╲                                      │   │
│  │    ╱  ╲    ╱╲                               │   │
│  │   ╱    ╲  ╱  ╲                              │   │
│  │  ╱      ╲╱    ╲                             │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  [Edit Target]  [Delete]                           │
└─────────────────────────────────────────────────────┘
```

**Specifications:**
- Card: White background, rounded-xl, shadow-lg, padding-6
- Image: 80x80px, rounded-md
- Product name: text-xl, font-semibold
- Price display: Large numbers with labels
- Status indicator: Color-coded (green below, orange above)
- Chart: Smooth line with gradient fill, responsive height
- Action buttons: Secondary style, rounded-md
- Menu: Three-dot menu (⋮) for additional actions
- Hover: Subtle shadow increase

#### PriceChart Component

**Visual Design:**
```
┌─────────────────────────────────────────────┐
│ $1000 ┤                                     │
│       │     ╱╲                              │
│  $950 ┤    ╱  ╲    ╱╲                       │
│       │   ╱    ╲  ╱  ╲                      │
│  $900 ┤  ╱      ╲╱    ╲                     │
│       │ ╱                                   │
│  $850 ┼─────────────────────────────────────│
│       └─────────────────────────────────────┘
│        Jan 1    Jan 15    Jan 30            │
└─────────────────────────────────────────────┘
```

**Specifications:**
- Library: Recharts or Chart.js
- Line: Smooth curve, 2px width, primary color
- Fill: Gradient from primary-500 to transparent
- Grid: Subtle horizontal lines (neutral-200)
- Axes: neutral-600 color, text-sm
- Tooltip: White background, shadow-lg, rounded-md
- Threshold line: Dashed line at target price (warning-500)
- Responsive: Maintains aspect ratio on all screens

#### ThresholdEditor Component

**Visual Design:**
```
┌─────────────────────────────────────┐
│ Target Price                        │
│ ┌─────────────────────────────────┐ │
│ │ $ 850.00                    [✓] │ │
│ └─────────────────────────────────┘ │
│ You'll be notified when price drops │
│ below this amount                   │
└─────────────────────────────────────┘
```

**Specifications:**
- Input: Large, rounded-md, with currency symbol
- Validation: Real-time, shows error for invalid values
- Save button: Checkmark icon, success color
- Help text: text-sm, neutral-600
- Inline editing: Click to edit, blur to save
- Animation: Smooth transition between view/edit modes

### Responsive Design

#### Breakpoints

```css
--screen-sm: 640px;   /* Mobile landscape */
--screen-md: 768px;   /* Tablet */
--screen-lg: 1024px;  /* Desktop */
--screen-xl: 1280px;  /* Large desktop */
```

#### Mobile (< 640px)
- Single column layout
- Full-width cards
- Stacked navigation
- Larger touch targets (min 44px)
- Simplified charts

#### Tablet (640px - 1024px)
- Two column grid for product cards
- Side-by-side price display
- Collapsible navigation

#### Desktop (> 1024px)
- Three column grid for product cards
- Full navigation bar
- Larger charts with more detail
- Hover effects enabled

### Accessibility Features

**Keyboard Navigation:**
- Tab order follows visual flow
- Focus indicators: 2px solid primary-500 outline
- Skip to main content link
- Escape key closes modals

**Screen Reader Support:**
- Semantic HTML (nav, main, article, section)
- ARIA labels for icons and interactive elements
- ARIA live regions for dynamic content (search results, notifications)
- Alt text for all images

**Color Contrast:**
- Text on background: Minimum 4.5:1 ratio
- Large text: Minimum 3:1 ratio
- Interactive elements: Clear visual states

**Motion:**
- Respect prefers-reduced-motion
- Disable animations for users who prefer reduced motion

### Micro-interactions

**Button Hover:**
- Scale: 1.02
- Shadow: Increase from md to lg
- Transition: 150ms ease

**Card Hover:**
- Transform: translateY(-4px)
- Shadow: Increase from md to xl
- Transition: 200ms ease

**Input Focus:**
- Border color: primary-500
- Ring: 3px primary-100
- Transition: 150ms ease

**Loading States:**
- Skeleton screens for content loading
- Spinner for actions
- Progress bar for long operations

**Success Feedback:**
- Checkmark animation
- Green flash on card
- Toast notification

**Error Feedback:**
- Shake animation
- Red border on input
- Error message slide-in

### Dark Mode Support (Optional Enhancement)

**Color Adjustments:**
```css
@media (prefers-color-scheme: dark) {
  --neutral-50: #18181b;    /* Page background */
  --neutral-100: #27272a;   /* Card background */
  --neutral-900: #fafafa;   /* Primary text */
  /* Adjust other colors for dark mode */
}
```

### UI Component Library Recommendations

**Recommended Libraries:**
- **Headless UI**: Accessible components (modals, dropdowns, tabs)
- **Heroicons**: Beautiful icon set
- **Recharts**: Responsive charts
- **React Hot Toast**: Toast notifications
- **Framer Motion**: Smooth animations (optional)

**Tailwind CSS Plugins:**
- @tailwindcss/forms: Better form styling
- @tailwindcss/typography: Better text styling
- @tailwindcss/aspect-ratio: Aspect ratio utilities

## Data Models

### Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tracked products table
CREATE TABLE tracked_products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    product_name VARCHAR(500) NOT NULL,
    product_url TEXT NOT NULL,
    current_price DECIMAL(10, 2) NOT NULL,
    price_threshold DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_checked TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_tracked_products_user_id ON tracked_products(user_id);
CREATE INDEX idx_tracked_products_last_checked ON tracked_products(last_checked);

-- Price history table
CREATE TABLE price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tracked_product_id UUID NOT NULL REFERENCES tracked_products(id) ON DELETE CASCADE,
    price DECIMAL(10, 2) NOT NULL,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tracked_product FOREIGN KEY (tracked_product_id) 
        REFERENCES tracked_products(id)
);

CREATE INDEX idx_price_history_product_id ON price_history(tracked_product_id);
CREATE INDEX idx_price_history_checked_at ON price_history(checked_at);

-- Notifications log table
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tracked_product_id UUID NOT NULL REFERENCES tracked_products(id) ON DELETE CASCADE,
    old_price DECIMAL(10, 2) NOT NULL,
    new_price DECIMAL(10, 2) NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_status VARCHAR(50) DEFAULT 'sent',
    CONSTRAINT fk_notification_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_notification_product FOREIGN KEY (tracked_product_id) 
        REFERENCES tracked_products(id)
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_sent_at ON notifications(sent_at);

-- Platform errors log table
CREATE TABLE platform_errors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform VARCHAR(50) NOT NULL,
    error_type VARCHAR(100) NOT NULL,
    error_message TEXT,
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_platform_errors_occurred_at ON platform_errors(occurred_at);
```

### SQLAlchemy Models

```python
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tracked_products = relationship("TrackedProduct", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

class TrackedProduct(Base):
    __tablename__ = "tracked_products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    product_name = Column(String(500), nullable=False)
    product_url = Column(Text, nullable=False)
    current_price = Column(Numeric(10, 2), nullable=False)
    price_threshold = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="USD")
    image_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_checked = Column(DateTime)
    
    user = relationship("User", back_populates="tracked_products")
    price_history = relationship("PriceHistory", back_populates="tracked_product", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="tracked_product", cascade="all, delete-orphan")

class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tracked_product_id = Column(UUID(as_uuid=True), ForeignKey("tracked_products.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow)
    
    tracked_product = relationship("TrackedProduct", back_populates="price_history")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    tracked_product_id = Column(UUID(as_uuid=True), ForeignKey("tracked_products.id"), nullable=False)
    old_price = Column(Numeric(10, 2), nullable=False)
    new_price = Column(Numeric(10, 2), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    delivery_status = Column(String(50), default="sent")
    
    user = relationship("User", back_populates="notifications")
    tracked_product = relationship("TrackedProduct", back_populates="notifications")

class PlatformError(Base):
    __tablename__ = "platform_errors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform = Column(String(50), nullable=False)
    error_type = Column(String(100), nullable=False)
    error_message = Column(Text)
    occurred_at = Column(DateTime, default=datetime.utcnow)
```

### Pydantic Schemas (API Models)

```python
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# Auth schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: str
    email: str
    token: str

# Product schemas
class ProductResult(BaseModel):
    platform: str
    product_name: str
    current_price: Decimal
    currency: str = "USD"
    product_url: HttpUrl
    image_url: Optional[HttpUrl] = None

class SearchResults(BaseModel):
    results: List[ProductResult]
    warnings: List[str] = []

# Tracking schemas
class TrackedProductCreate(BaseModel):
    platform: str
    product_name: str
    product_url: HttpUrl
    current_price: Decimal = Field(..., gt=0)
    price_threshold: Decimal = Field(..., gt=0)
    image_url: Optional[HttpUrl] = None

class TrackedProductResponse(BaseModel):
    id: str
    platform: str
    product_name: str
    product_url: str
    current_price: Decimal
    price_threshold: Decimal
    currency: str
    image_url: Optional[str]
    created_at: datetime
    last_checked: Optional[datetime]

class ThresholdUpdate(BaseModel):
    price_threshold: Decimal = Field(..., gt=0)

class PriceHistoryEntry(BaseModel):
    price: Decimal
    checked_at: datetime

class PriceHistoryResponse(BaseModel):
    history: List[PriceHistoryEntry]
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

Before writing the correctness properties, I need to analyze the acceptance criteria to determine which are suitable for property-based testing.



### Property 1: Search Result Completeness

*For any* set of search results returned by the Product Search Engine, all results SHALL include product name, current price, platform name, and product URL.

**Validates: Requirements 1.5**

### Property 2: Tracked Product Data Preservation

*For any* valid tracked product data, saving it to the system and then retrieving it SHALL return all the original data fields (product name, current price, platform, product URL, price threshold) unchanged.

**Validates: Requirements 2.3**

### Property 3: Product Deletion Completeness

*For any* tracked product in a user's list, deleting that product SHALL result in it no longer appearing in the user's tracked products list.

**Validates: Requirements 2.5**

### Property 4: User Data Isolation

*For any* two distinct users A and B, user A SHALL NOT be able to view, modify, or delete any tracked products belonging to user B.

**Validates: Requirements 2.6, 5.7**

### Property 5: Price History Recording

*For any* sequence of price checks performed on a tracked product, all price values SHALL be recorded in the price history with their corresponding timestamps.

**Validates: Requirements 3.5**

### Property 6: Price Update Persistence

*For any* price check that completes successfully, the tracked product's current_price field in the database SHALL be updated to reflect the newly retrieved price.

**Validates: Requirements 3.3**

### Property 7: Notification Trigger Condition

*For any* tracked product where the current price falls below the user's price threshold, a notification SHALL be triggered and sent to the user.

**Validates: Requirements 4.1, 8.4**

### Property 8: Notification Content Completeness

*For any* price drop notification email, the email content SHALL include the product name, old price, new price, price threshold, and product URL.

**Validates: Requirements 4.2**

### Property 9: Notification Consolidation

*For any* set of price drops detected simultaneously for the same user, exactly one email SHALL be sent containing all price drop information.

**Validates: Requirements 4.4**

### Property 10: Notification Idempotence

*For any* price drop event, repeated price checks while the price remains below the threshold SHALL NOT trigger additional notifications until the price rises above the threshold and drops below it again.

**Validates: Requirements 4.5**

### Property 11: Notification on Threshold Re-crossing

*For any* tracked product where the price rises above the threshold and then drops below it again, a new notification SHALL be sent for the new price drop event.

**Validates: Requirements 4.6**

### Property 12: Email Format Validation

*For any* string input provided as an email address (during registration or email update), the system SHALL correctly identify whether it conforms to valid email format and reject invalid formats.

**Validates: Requirements 5.2, 7.2**

### Property 13: Password Length Validation

*For any* string input provided as a password during registration, the system SHALL accept it only if it contains at least 8 characters.

**Validates: Requirements 5.3**

### Property 14: Unavailable Product Filtering

*For any* set of search results that includes products marked as unavailable or out of stock, those products SHALL be excluded from the final results presented to the user.

**Validates: Requirements 6.2**

### Property 15: Unicode Query Handling

*For any* valid Unicode string (including special characters and non-English text) submitted as a search query, the system SHALL process it without errors.

**Validates: Requirements 6.3**

### Property 16: Current Email Address Usage

*For any* user who has updated their email address, all subsequent notifications SHALL be sent to the most recently updated email address.

**Validates: Requirements 7.3**

### Property 17: Price Threshold Validation

*For any* number provided as a price threshold, the system SHALL accept it only if it is a positive number (greater than zero).

**Validates: Requirements 8.2**

### Property 18: Updated Threshold Application

*For any* tracked product where the price threshold is updated, all subsequent price drop detection SHALL use the new threshold value.

**Validates: Requirements 8.3**

### Property 19: Retry with Exponential Backoff

*For any* failed attempt to retrieve a product price from an e-commerce platform, the system SHALL retry up to 3 times with exponentially increasing delays between attempts.

**Validates: Requirements 9.2**

### Property 20: Platform Error Logging

*For any* platform connection failure or scraping error, an error log entry SHALL be created with the platform name, error type, error message, and timestamp.

**Validates: Requirements 9.4**

### Property 21: Referential Integrity

*For any* tracked product or price history entry in the database, it SHALL reference a valid parent record (tracked products reference valid users, price history entries reference valid tracked products).

**Validates: Requirements 10.4, 10.5**

## Error Handling

### Error Categories and Strategies

**1. External Platform Errors**
- **Scenario**: E-commerce platform is unreachable, returns errors, or times out
- **Strategy**: 
  - Implement retry logic with exponential backoff (3 attempts)
  - Log all failures to `platform_errors` table
  - During search: Return results from available platforms with warning message
  - During monitoring: Skip failed products and retry in next cycle
  - Use circuit breaker pattern to temporarily disable failing platforms

**2. Database Errors**
- **Scenario**: Database connection fails, write operations fail, constraint violations
- **Strategy**:
  - Use connection pooling with automatic reconnection
  - Wrap all database operations in try-catch blocks
  - Return appropriate HTTP error codes (500 for server errors)
  - Log all database errors with stack traces
  - Use database transactions to ensure atomicity
  - Rollback on failure and return error to user

**3. Authentication Errors**
- **Scenario**: Invalid credentials, expired tokens, missing tokens
- **Strategy**:
  - Return 401 Unauthorized for invalid/expired tokens
  - Return 403 Forbidden for insufficient permissions
  - Clear error messages without exposing security details
  - Rate limit login attempts to prevent brute force

**4. Validation Errors**
- **Scenario**: Invalid email format, negative price threshold, missing required fields
- **Strategy**:
  - Use Pydantic for automatic request validation
  - Return 422 Unprocessable Entity with detailed field errors
  - Validate on both frontend and backend
  - Provide clear, user-friendly error messages

**5. Email Delivery Errors**
- **Scenario**: SMTP connection fails, email bounces, invalid recipient
- **Strategy**:
  - Log delivery failures to `notifications` table with status
  - Retry email delivery up to 3 times
  - Don't block price monitoring on email failures
  - Provide user notification in UI if email delivery consistently fails

**6. Scraping Errors**
- **Scenario**: HTML structure changes, anti-bot measures, rate limiting
- **Strategy**:
  - Use robust selectors with fallbacks
  - Implement user-agent rotation
  - Add delays between requests to avoid rate limiting
  - Log scraping failures for manual investigation
  - Gracefully handle missing data (e.g., no image URL)

**7. Celery Task Errors**
- **Scenario**: Task fails, worker crashes, Redis connection lost
- **Strategy**:
  - Configure task retries with exponential backoff
  - Use task result backend to track failures
  - Implement task timeout to prevent hanging
  - Monitor worker health and restart on failure
  - Log all task failures with context

### Error Response Format

All API errors follow consistent JSON format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "specific field error"
    }
  }
}
```

### HTTP Status Codes

- **200 OK**: Successful request
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request format
- **401 Unauthorized**: Authentication required or failed
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation errors
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server-side error
- **503 Service Unavailable**: Service temporarily unavailable

## Testing Strategy

### Testing Approach

The testing strategy employs a dual approach combining property-based testing for universal correctness guarantees with example-based testing for specific scenarios and integration points.

### Property-Based Testing

**Framework**: Hypothesis (Python)

**Configuration**:
- Minimum 100 iterations per property test
- Each test tagged with comment referencing design property
- Tag format: `# Feature: ecommerce-price-tracker, Property {number}: {property_text}`

**Property Test Coverage**:

All 21 correctness properties defined above will be implemented as property-based tests. Each property test will:
1. Generate random valid inputs using Hypothesis strategies
2. Execute the system behavior
3. Assert the property holds for all generated inputs
4. Use mocks for external dependencies (scrapers, SMTP)

**Example Property Test Structure**:

```python
from hypothesis import given, strategies as st
import pytest

# Feature: ecommerce-price-tracker, Property 2: Tracked Product Data Preservation
@given(
    product_name=st.text(min_size=1, max_size=500),
    current_price=st.decimals(min_value=0.01, max_value=999999.99, places=2),
    platform=st.sampled_from(["lazada", "shopee", "tiktok"]),
    product_url=st.from_regex(r'https://[a-z]+\.com/product/[0-9]+', fullmatch=True),
    price_threshold=st.decimals(min_value=0.01, max_value=999999.99, places=2)
)
@pytest.mark.property_test
async def test_tracked_product_round_trip(
    product_name, current_price, platform, product_url, price_threshold, 
    db_session, test_user
):
    """Property 2: For any valid tracked product data, saving and retrieving 
    should preserve all fields."""
    
    # Create tracked product
    original_data = TrackedProductCreate(
        platform=platform,
        product_name=product_name,
        product_url=product_url,
        current_price=current_price,
        price_threshold=price_threshold
    )
    
    # Save to database
    tracking_service = TrackingService(db_session)
    saved_product = await tracking_service.create_tracked_product(
        user_id=test_user.id,
        product_data=original_data
    )
    
    # Retrieve from database
    retrieved_products = await tracking_service.get_user_tracked_products(
        user_id=test_user.id
    )
    
    # Assert data preservation
    assert len(retrieved_products) == 1
    retrieved = retrieved_products[0]
    assert retrieved.platform == platform
    assert retrieved.product_name == product_name
    assert retrieved.product_url == product_url
    assert retrieved.current_price == current_price
    assert retrieved.price_threshold == price_threshold
```

### Unit Testing

**Framework**: pytest

**Coverage Areas**:
- Service layer business logic
- Input validation edge cases
- Error handling scenarios
- Authentication and authorization
- Email composition
- Data transformations

**Example Unit Tests**:
- Empty search results display message (Req 1.6)
- Login with correct credentials (Req 5.4, 5.5)
- Login with incorrect credentials (Req 5.6)
- Platform unavailable during search (Req 9.1)
- All retry attempts fail (Req 9.3)
- Database write failure (Req 10.3)

### Integration Testing

**Framework**: pytest with TestClient (FastAPI)

**Coverage Areas**:
- API endpoint integration
- Database operations
- Celery task execution
- Email delivery (with mocked SMTP)
- Multi-platform search coordination
- End-to-end user workflows

**Example Integration Tests**:
- Complete user registration and login flow
- Search products across all platforms (with mocked scrapers)
- Track product and verify database persistence
- Price monitoring cycle execution
- Notification delivery on price drop

### Frontend Testing

**Framework**: Jest + React Testing Library

**Coverage Areas**:
- Component rendering
- User interactions
- Form validation
- API integration
- State management
- Error handling

**Test Types**:
- Component unit tests
- Integration tests with mocked API
- End-to-end tests with Playwright

### Test Data Management

**Strategies**:
- Use factories (factory_boy) for generating test data
- Database fixtures for common test scenarios
- Mocked scraper responses for consistent testing
- Separate test database with automatic cleanup
- Hypothesis strategies for property test data generation

### Continuous Integration

**CI Pipeline**:
1. Lint code (flake8, black, mypy)
2. Run unit tests with coverage report (minimum 80% coverage)
3. Run property tests (100 iterations each)
4. Run integration tests
5. Build Docker images
6. Run security scans (bandit, safety)

### Test Organization

```
tests/
├── unit/
│   ├── services/
│   │   ├── test_auth_service.py
│   │   ├── test_tracking_service.py
│   │   ├── test_search_service.py
│   │   ├── test_notification_service.py
│   │   └── test_price_monitor_service.py
│   ├── scrapers/
│   │   ├── test_lazada_scraper.py
│   │   ├── test_shopee_scraper.py
│   │   └── test_tiktok_scraper.py
│   └── validators/
│       └── test_validators.py
├── property/
│   ├── test_data_properties.py
│   ├── test_notification_properties.py
│   ├── test_validation_properties.py
│   └── test_integrity_properties.py
├── integration/
│   ├── test_api_endpoints.py
│   ├── test_celery_tasks.py
│   └── test_end_to_end_flows.py
├── fixtures/
│   ├── database.py
│   ├── users.py
│   └── products.py
└── conftest.py
```

### Performance Testing

**Tools**: Locust for load testing

**Scenarios**:
- Concurrent user searches
- Simultaneous product tracking
- Bulk price monitoring
- Database query performance

**Targets**:
- Search response time < 10 seconds (Req 1.4)
- API response time < 500ms for CRUD operations
- Support 100+ concurrent users
- Process 1000+ tracked products per monitoring cycle

### Security Testing

**Areas**:
- SQL injection prevention (parameterized queries)
- XSS prevention (input sanitization)
- CSRF protection (CORS configuration)
- Authentication bypass attempts
- Authorization boundary testing
- Password security (hashing, minimum length)
- Rate limiting effectiveness

## Implementation Phases

### Phase 1: Core Infrastructure (Week 1-2)
- Set up project structure and dependencies
- Configure PostgreSQL database and migrations
- Implement user authentication (registration, login, JWT)
- Create base API structure with FastAPI
- Set up Docker and Docker Compose
- Implement basic frontend with React and routing

### Phase 2: Product Search (Week 3-4)
- Implement scraper framework and base scraper class
- Develop platform-specific scrapers (Lazada, Shopee, TikTok)
- Create search API endpoint
- Implement search results aggregation
- Build search UI component
- Add error handling for platform failures

### Phase 3: Product Tracking (Week 5-6)
- Implement tracking service and CRUD operations
- Create tracking API endpoints
- Build tracked products list UI
- Implement price threshold management
- Add product deletion functionality
- Create price history tracking

### Phase 4: Price Monitoring (Week 7-8)
- Set up Celery and Redis
- Implement price monitoring service
- Create Celery tasks for scheduled checks
- Configure Celery Beat scheduler
- Implement retry logic with exponential backoff
- Add comprehensive error logging

### Phase 5: Notifications (Week 9-10)
- Implement notification service
- Configure SMTP email delivery
- Create email templates
- Implement notification consolidation logic
- Add notification idempotence
- Build email preference management

### Phase 6: Testing & Polish (Week 11-12)
- Write property-based tests for all 21 properties
- Implement unit tests for all services
- Create integration tests for API endpoints
- Add frontend tests
- Perform security testing
- Optimize performance
- Write documentation

### Phase 7: Deployment (Week 13)
- Set up production environment
- Configure CI/CD pipeline
- Deploy to hosting platform
- Set up monitoring and logging
- Perform load testing
- Create user documentation

## Deployment Architecture

### Development Environment
```yaml
# docker-compose.yml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: price_tracker_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  backend:
    build: ./backend
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://dev_user:dev_password@db:5432/price_tracker_dev
      REDIS_URL: redis://redis:6379/0
  
  celery_worker:
    build: ./backend
    command: celery -A tasks worker --loglevel=info
    volumes:
      - ./backend:/app
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://dev_user:dev_password@db:5432/price_tracker_dev
      REDIS_URL: redis://redis:6379/0
  
  celery_beat:
    build: ./backend
    command: celery -A tasks beat --loglevel=info
    volumes:
      - ./backend:/app
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://dev_user:dev_password@db:5432/price_tracker_dev
      REDIS_URL: redis://redis:6379/0
  
  frontend:
    build: ./frontend
    command: npm run dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000
```

### Production Deployment Options

**Option 1: Railway (Free Tier)**
- PostgreSQL database (500MB free)
- Redis (100MB free)
- Backend service (512MB RAM, $5/month after free tier)
- Celery worker (separate service)
- Frontend (static hosting)

**Option 2: Render (Free Tier)**
- PostgreSQL database (free tier available)
- Redis (free tier available)
- Backend web service (free tier with limitations)
- Background worker (separate service)
- Static site for frontend (free)

**Option 3: Self-Hosted VPS**
- Single VPS (e.g., DigitalOcean $6/month droplet)
- Docker Compose deployment
- Nginx reverse proxy
- Let's Encrypt SSL certificates
- Full control over resources

### Environment Variables

```bash
# Backend
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://host:6379/0
SECRET_KEY=your-secret-key-for-jwt
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FRONTEND_URL=https://your-frontend-url.com

# Frontend
REACT_APP_API_URL=https://your-backend-url.com
```

### Monitoring and Logging

**Logging Strategy**:
- Structured logging with Python's logging module
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Separate log files for different components
- Centralized logging with timestamps and context

**Monitoring**:
- Health check endpoints for all services
- Database connection monitoring
- Celery task success/failure rates
- Platform scraping success rates
- Email delivery success rates
- API response times

**Alerting**:
- Email alerts for critical errors
- Slack/Discord webhooks for monitoring alerts
- Database connection failures
- High error rates in scraping
- Email delivery failures

## Security Considerations

### Authentication & Authorization
- JWT tokens with expiration (24 hours)
- Secure password hashing with bcrypt
- Password minimum length enforcement (8 characters)
- Email validation on registration and updates
- User data isolation enforced at database query level

### Data Protection
- HTTPS only in production
- Environment variables for sensitive configuration
- Database credentials not in code
- CORS configuration to restrict API access
- SQL injection prevention via parameterized queries

### Rate Limiting
- API rate limiting to prevent abuse
- Login attempt rate limiting (prevent brute force)
- Search rate limiting per user
- Scraping rate limiting to avoid platform bans

### Input Validation
- Pydantic models for all API inputs
- Email format validation
- URL validation for product URLs
- Numeric validation for prices and thresholds
- XSS prevention through input sanitization

### Scraping Ethics
- Respect robots.txt
- Implement delays between requests
- Use appropriate user agents
- Don't overwhelm platform servers
- Cache results when appropriate

## Future Enhancements

### Phase 2 Features
- Price drop percentage alerts (e.g., notify on 20% drop)
- Price charts and analytics
- Product comparison tool
- Browser extension for quick tracking
- Mobile app (React Native)
- Webhook notifications (Slack, Discord, Telegram)
- Multiple notification channels
- Price prediction using historical data
- Wishlist sharing between users
- Product categories and tags

### Scalability Improvements
- Implement caching layer (Redis) for search results
- Use message queue for notification delivery
- Implement database read replicas
- Add CDN for frontend assets
- Implement API versioning
- Add GraphQL API option
- Microservices architecture for large scale

### Advanced Features
- AI-powered price prediction
- Automatic coupon code detection
- Price comparison with historical trends
- Product recommendation engine
- Multi-currency support
- International platform support
- Affiliate link integration
- Price alert scheduling (only check during certain hours)

---

## Conclusion

This design document provides a comprehensive blueprint for implementing the E-commerce Price Tracker system using free and open-source technologies. The architecture is scalable, maintainable, and testable, with strong emphasis on correctness through property-based testing. The phased implementation approach allows for incremental development and testing, ensuring a robust final product.
