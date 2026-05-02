# E-commerce Price Tracker

A full-stack web application for tracking product prices across multiple e-commerce platforms (Lazada, Shopee, TikTok Shop) in the Philippines.

## 🚀 Live Demo

- **Frontend**: https://price-tracker-lazada.vercel.app
- **Backend API**: https://price-tracker-lazada-uuyz.vercel.app
- **API Docs**: https://price-tracker-lazada-uuyz.vercel.app/docs

## ✨ Features

- 🔍 **Multi-Platform Search**: Search products across Lazada, Shopee, and TikTok Shop
- 📊 **Price Tracking**: Track product prices and get notified when prices drop
- 📈 **Price History**: View historical price data with interactive charts
- 🔐 **Google OAuth**: Secure authentication with Google Sign-In
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- ⚡ **Real-Time Data**: Fresh product data scraped in real-time

## 🏗️ Architecture

```
User → Frontend (Vercel) → Backend API (Vercel) → Scraper Service (Render) → E-commerce Sites
                                ↓
                          Database (Supabase)
```

### Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite
- TailwindCSS
- Recharts (for price history charts)
- Google OAuth

**Backend:**
- FastAPI (Python)
- SQLAlchemy + Alembic
- PostgreSQL (Supabase)
- JWT Authentication
- Pydantic for validation

**Scraper Service:**
- FastAPI
- Selenium + Chrome
- BeautifulSoup4

## 📋 Deployment Status

| Component | Platform | Status | URL |
|-----------|----------|--------|-----|
| Frontend | Vercel | ✅ Live | https://price-tracker-lazada.vercel.app |
| Backend | Vercel | ✅ Live | https://price-tracker-lazada-uuyz.vercel.app |
| Scraper | Render | ⚠️ Deploy needed | - |
| Database | Supabase | ✅ Live | - |

## 🚀 Quick Deployment

**Need to deploy? Follow these guides in order:**

1. **[QUICK_START.md](QUICK_START.md)** - 4-step quick deployment (5 minutes)
2. **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete step-by-step guide (20 minutes)
3. **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Interactive checklist with checkboxes
4. **[VISUAL_GUIDE.md](VISUAL_GUIDE.md)** - Visual guide with diagrams

**Additional Documentation:**
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and data flow
- **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)** - Recent changes for Vercel deployment
- **[VERCEL_ENV_VARIABLES.md](VERCEL_ENV_VARIABLES.md)** - Environment variables setup

## 🎯 Current Status

### ✅ Completed
- [x] Frontend UI (React + TypeScript)
- [x] Backend API (FastAPI)
- [x] Database schema (PostgreSQL)
- [x] Google OAuth authentication
- [x] Product search functionality
- [x] Price tracking system
- [x] Price history charts
- [x] Lazada scraper (Selenium)
- [x] Deployment configuration for Vercel
- [x] Separate scraper service for Render

### 🚧 In Progress
- [ ] Deploy scraper service to Render
- [ ] Background price checking (Celery)
- [ ] Email notifications
- [ ] Shopee scraper
- [ ] TikTok Shop scraper

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Chrome/Chromium (for scraping)

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd price-tracker
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and configure .env
cp .env.example .env
# Edit .env with your database URL, Google OAuth credentials, etc.

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

3. **Frontend Setup**
```bash
cd frontend
npm install

# Copy and configure .env
cp .env.example .env
# Edit .env with your backend API URL and Google Client ID

# Start the dev server
npm run dev
```

4. **Scraper Service Setup** (Optional for local development)
```bash
cd lazada_api_production
pip install -r requirements.txt

# Start the scraper service
uvicorn main:app --reload --port 8001
```

### Environment Variables

**Backend (.env):**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/price_tracker
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
LAZADA_API_URL=http://localhost:8001  # For local development
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

```
POST   /api/auth/google/login    - Google OAuth login
GET    /api/auth/me              - Get current user
GET    /api/products/search      - Search products
POST   /api/tracking/track       - Track a product
GET    /api/tracking/products    - Get tracked products
DELETE /api/tracking/{id}        - Untrack a product
GET    /health                   - Health check
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Project Structure

```
.
├── backend/                    # FastAPI backend
│   ├── alembic/               # Database migrations
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Core utilities
│   │   ├── models/            # SQLAlchemy models
│   │   ├── repositories/      # Data access layer
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── scrapers/          # Web scrapers
│   │   └── services/          # Business logic
│   └── tests/                 # Backend tests
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── contexts/          # React contexts
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   └── types/             # TypeScript types
│   └── public/                # Static assets
│
├── lazada_api_production/     # Scraper service (Render)
│   ├── scrapers/              # Scraper implementations
│   └── main.py                # FastAPI app
│
└── docs/                      # Documentation
    ├── QUICK_START.md
    ├── DEPLOYMENT_GUIDE.md
    ├── DEPLOYMENT_CHECKLIST.md
    ├── ARCHITECTURE.md
    └── ...
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - JavaScript library for building UIs
- [Vercel](https://vercel.com/) - Deployment platform
- [Render](https://render.com/) - Cloud platform for scraper service
- [Supabase](https://supabase.com/) - PostgreSQL database hosting

## 📞 Support

For deployment help, see:
- [QUICK_START.md](QUICK_START.md) - Quick deployment guide
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Detailed deployment instructions
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Step-by-step checklist

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for price-conscious shoppers in the Philippines**
