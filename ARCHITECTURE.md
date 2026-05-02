# System Architecture

## Overview

The E-commerce Price Tracker is a distributed system with three main components deployed across different platforms.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                           USER BROWSER                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vercel)                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  React + TypeScript + Vite                               │  │
│  │  - Login/Register pages                                  │  │
│  │  - Product search interface                              │  │
│  │  - Tracked products dashboard                            │  │
│  │  - Price history charts                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  URL: https://price-tracker-lazada.vercel.app                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API (HTTPS)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND API (Vercel)                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  FastAPI (Python)                                        │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  /api/auth     - Google OAuth, JWT tokens          │ │  │
│  │  │  /api/products - Search products                    │ │  │
│  │  │  /api/tracking - Track/untrack products             │ │  │
│  │  │  /health       - Health check                       │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│  URL: https://price-tracker-lazada-uuyz.vercel.app             │
└────────┬───────────────────────────────┬────────────────────────┘
         │                               │
         │ SQL                           │ HTTP API
         ▼                               ▼
┌─────────────────────┐    ┌──────────────────────────────────────┐
│  DATABASE           │    │  LAZADA SCRAPER (Render)             │
│  (Supabase)         │    │  ┌────────────────────────────────┐  │
│  ┌───────────────┐  │    │  │  FastAPI + Selenium            │  │
│  │ PostgreSQL    │  │    │  │  ┌──────────────────────────┐  │  │
│  │               │  │    │  │  │  /search - Search Lazada │  │  │
│  │ - users       │  │    │  │  │  /health - Health check  │  │  │
│  │ - products    │  │    │  │  └──────────────────────────┘  │  │
│  │ - tracking    │  │    │  │                                │  │
│  │ - history     │  │    │  │  Chrome + ChromeDriver         │  │
│  │               │  │    │  │  (Headless browser)            │  │
│  └───────────────┘  │    │  └────────────────────────────────┘  │
│                     │    │  URL: https://your-service.onrender.com│
└─────────────────────┘    └────────────────┬─────────────────────┘
                                            │
                                            │ Web Scraping
                                            ▼
                           ┌──────────────────────────────────┐
                           │  LAZADA.COM.PH                   │
                           │  (E-commerce Website)            │
                           └──────────────────────────────────┘
```

## Component Details

### 1. Frontend (Vercel)
**Technology:** React, TypeScript, Vite, TailwindCSS
**Hosting:** Vercel (Serverless)
**Responsibilities:**
- User interface and interactions
- Google OAuth login flow
- Product search and display
- Price tracking management
- Price history visualization

**Environment Variables:**
- `VITE_GOOGLE_CLIENT_ID` - Google OAuth client ID
- `VITE_API_URL` - Backend API URL

### 2. Backend API (Vercel)
**Technology:** FastAPI (Python), SQLAlchemy, Pydantic
**Hosting:** Vercel (Serverless Functions)
**Responsibilities:**
- User authentication (Google OAuth + JWT)
- Product search orchestration
- Price tracking management
- Database operations
- API endpoints

**Environment Variables:**
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth secret
- `CORS_ORIGINS` - Allowed frontend origins
- `LAZADA_API_URL` - Lazada scraper service URL

**Key Endpoints:**
```
POST   /api/auth/google/login    - Google OAuth login
GET    /api/auth/me              - Get current user
GET    /api/products/search      - Search products
POST   /api/tracking/track       - Track a product
GET    /api/tracking/products    - Get tracked products
DELETE /api/tracking/{id}        - Untrack a product
GET    /health                   - Health check
```

### 3. Database (Supabase)
**Technology:** PostgreSQL
**Hosting:** Supabase (Managed PostgreSQL)
**Responsibilities:**
- Store user accounts
- Store tracked products
- Store price history
- Store notifications

**Tables:**
```sql
users
  - id (UUID, primary key)
  - email (unique)
  - google_id (unique)
  - created_at

tracked_products
  - id (UUID, primary key)
  - user_id (foreign key)
  - platform (lazada/shopee/tiktokshop)
  - product_url (unique per user)
  - product_name
  - current_price
  - target_price
  - created_at

price_history
  - id (UUID, primary key)
  - tracked_product_id (foreign key)
  - price
  - checked_at

notifications
  - id (UUID, primary key)
  - user_id (foreign key)
  - tracked_product_id (foreign key)
  - notification_type
  - sent_at
```

### 4. Lazada Scraper (Render)
**Technology:** FastAPI, Selenium, Chrome
**Hosting:** Render (Container)
**Responsibilities:**
- Web scraping Lazada.com.ph
- Product search with pagination
- Price extraction
- Image URL extraction

**Why Separate Service?**
- Vercel serverless functions don't support browser automation
- Render provides persistent containers with Chrome/ChromeDriver
- Can be scaled independently
- Isolates scraping logic from main backend

**Environment Variables:**
- None required (standalone service)

**Key Endpoints:**
```
GET /search?q={query}&page={page}&per_page={limit}&sort_by={sort}
GET /health
GET /platform-info
```

## Data Flow

### Product Search Flow
```
1. User enters search query in frontend
   ↓
2. Frontend sends GET /api/products/search?q=laptop
   ↓
3. Backend receives request, validates JWT token
   ↓
4. Backend calls Lazada Scraper: GET /search?q=laptop
   ↓
5. Scraper launches Chrome, navigates to Lazada
   ↓
6. Scraper extracts product data (name, price, image, URL)
   ↓
7. Scraper returns JSON response to backend
   ↓
8. Backend formats response and returns to frontend
   ↓
9. Frontend displays products with images and prices
```

### Track Product Flow
```
1. User clicks "Track Price" on a product
   ↓
2. Frontend sends POST /api/tracking/track with product data
   ↓
3. Backend validates JWT token and product data
   ↓
4. Backend saves to database (tracked_products table)
   ↓
5. Backend creates initial price_history entry
   ↓
6. Backend returns success response
   ↓
7. Frontend shows "Product tracked" notification
```

### Price Check Flow (Background Job - Not Yet Implemented)
```
1. Celery beat triggers periodic task (every 24 hours)
   ↓
2. Task fetches all tracked products from database
   ↓
3. For each product:
   a. Call Lazada Scraper to get current price
   b. Compare with previous price
   c. Save to price_history table
   d. If price dropped below target, create notification
   ↓
4. Send email notifications to users (if configured)
```

## Deployment Platforms

| Component | Platform | Plan | Cost | URL |
|-----------|----------|------|------|-----|
| Frontend | Vercel | Hobby | Free | https://price-tracker-lazada.vercel.app |
| Backend | Vercel | Hobby | Free | https://price-tracker-lazada-uuyz.vercel.app |
| Database | Supabase | Free | Free | db.jnruinihotolqgmcwyhs.supabase.co |
| Scraper | Render | Free/Starter | $0-7/mo | https://your-service.onrender.com |

## Performance Characteristics

### Response Times
- **Frontend Load:** 1-2 seconds
- **Backend API:** 100-500ms (excluding scraping)
- **Product Search:** 6-10 seconds (normal)
- **Product Search:** 30-60 seconds (cold start on Render free tier)
- **Database Queries:** 50-200ms

### Limitations
- **Render Free Tier:** Spins down after 15 minutes of inactivity
- **Vercel Free Tier:** 100GB bandwidth/month, 100 hours serverless execution
- **Supabase Free Tier:** 500MB database, 2GB bandwidth

## Security

### Authentication
- Google OAuth 2.0 for user login
- JWT tokens for API authentication
- Tokens expire after 24 hours

### Data Protection
- HTTPS for all communications
- Database credentials in environment variables
- CORS restrictions on API
- SQL injection prevention via SQLAlchemy ORM

### Secrets Management
- Environment variables stored in Vercel/Render
- No secrets in code or Git repository
- Separate secrets for dev/staging/production

## Scalability

### Current Capacity
- **Users:** Unlimited (limited by database)
- **Searches:** ~1000/day (Render free tier)
- **Tracked Products:** Unlimited (limited by database)

### Scaling Options
1. **Upgrade Render to Starter ($7/mo):**
   - No cold starts
   - Better performance
   - More CPU/memory

2. **Add More Scraper Services:**
   - Deploy Shopee scraper
   - Deploy TikTok Shop scraper
   - Load balance across multiple instances

3. **Upgrade Database:**
   - Supabase Pro ($25/mo)
   - More storage and bandwidth
   - Better performance

4. **Add Caching:**
   - Redis for search results
   - Cache product data for 1 hour
   - Reduce scraper load

## Monitoring

### Health Checks
- Frontend: Vercel automatic monitoring
- Backend: `/health` endpoint
- Scraper: `/health` endpoint
- Database: Supabase dashboard

### Logs
- Frontend: Vercel logs
- Backend: Vercel function logs
- Scraper: Render logs
- Database: Supabase logs

### Alerts (To Be Implemented)
- Email on scraper failures
- Email on database errors
- Slack notifications for critical errors

## Future Enhancements

1. **Additional Platforms:**
   - Shopee scraper
   - TikTok Shop scraper

2. **Background Jobs:**
   - Celery for periodic price checks
   - Email notifications

3. **Advanced Features:**
   - Price drop predictions
   - Price history analytics
   - Product recommendations
   - Price alerts via SMS

4. **Performance:**
   - Redis caching
   - CDN for images
   - Database indexing optimization

## Conclusion

This architecture provides a scalable, maintainable, and cost-effective solution for tracking e-commerce prices across multiple platforms. The separation of concerns (frontend, backend, scraper, database) allows each component to be developed, deployed, and scaled independently.
