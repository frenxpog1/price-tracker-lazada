# PriceTracker

A modern e-commerce price tracking application that monitors product prices across multiple platforms (Lazada, Shopee, TikTok Shop) and alerts you when prices drop below your target.

## Features

- 🔍 **Multi-Platform Search** - Search products across Lazada, Shopee, and TikTok Shop
- 📊 **Price History** - Track price changes over time with interactive charts
- 🎯 **Price Alerts** - Set target prices and get notified when products drop below threshold
- 🔄 **Auto Price Updates** - Automatic hourly price checks with small variations
- 📱 **Modern UI** - Clean 2026 design inspired by Apple/Stripe/Linear
- 🔔 **Notifications** - Real-time alerts when your tracked products hit target prices
- 💾 **Persistent Data** - Price history and changes stored locally

## Tech Stack

### Frontend
- React + TypeScript
- Vite
- TailwindCSS
- React Router
- Recharts (for price history graphs)

### Backend
- Python + FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migrations)
- Playwright/Selenium (web scraping)

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL

### Installation

1. Clone the repository
```bash
git clone https://github.com/Frenxpog1/pricetracker.git
cd pricetracker
```

2. Setup Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
alembic upgrade head
python -m uvicorn app.main:app --reload
```

3. Setup Frontend
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your backend URL
npm run dev
```

4. Open http://localhost:3000

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/pricetracker
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

### Backend (Render/Railway)
- Connect your GitHub repository
- Set environment variables
- Deploy from main branch

## Project Structure

```
pricetracker/
├── frontend/           # React frontend
│   ├── src/
│   │   ├── components/ # Reusable UI components
│   │   ├── pages/      # Page components
│   │   ├── services/   # API services
│   │   └── types/      # TypeScript types
│   └── package.json
├── backend/            # FastAPI backend
│   ├── app/
│   │   ├── api/        # API routes
│   │   ├── models/     # Database models
│   │   ├── scrapers/   # Web scrapers
│   │   └── services/   # Business logic
│   └── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Author

**Frenxpog1**
- GitHub: [@Frenxpog1](https://github.com/Frenxpog1)
- Email: frenzterp@gmail.com

---

Built with ❤️ using React, FastAPI, and modern web technologies.
