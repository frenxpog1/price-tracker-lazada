# E-Commerce Price Tracker

A full-stack application for tracking product prices across e-commerce platforms in the Philippines, with a production-ready Lazada API.

## 🚀 Quick Start

### Main Application (Full Stack)
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Lazada API (Production Ready)
```bash
cd lazada_api_production
pip install -r requirements.txt
python3 main.py
# Open test_dashboard.html in browser
```

## 📦 What's Included

### 1. **Full Stack Price Tracker** (`backend/`, `frontend/`)
- Track products from multiple platforms
- Price history visualization
- User authentication
- Email notifications
- PostgreSQL database

### 2. **Lazada API** (`lazada_api_production/`)
- ✅ Production-ready REST API
- ✅ Fast (6-8 second response)
- ✅ Pagination & sorting
- ✅ Real product data with images
- ✅ Ready to deploy

## 🛠️ Tech Stack

**Backend:** FastAPI, PostgreSQL, SQLAlchemy, Selenium  
**Frontend:** React 18, TypeScript, Tailwind CSS, Recharts  
**API:** FastAPI, Selenium, ChromeDriver

## 📖 Documentation

- **Main App:** See `backend/README.md` and `frontend/README.md`
- **Lazada API:** See `lazada_api_production/README.md`
- **API Docs:** http://localhost:8000/docs (when running)

## 🌐 Deploy

The Lazada API is ready to deploy to:
- Railway.app
- Render.com
- Heroku
- Fly.io
- Any Docker platform

See `lazada_api_production/README.md` for deployment guides.

## 📝 License

MIT
