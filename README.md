# E-commerce Price Tracker

A modern web application that tracks product prices across multiple e-commerce platforms (Lazada, Shopee, TikTok Shop) and sends email notifications when prices drop below user-defined thresholds.

## Features

- 🔍 **Multi-Platform Search**: Search products across Lazada, Shopee, and TikTok Shop simultaneously
- 📊 **Price Tracking**: Save products and monitor price changes automatically
- 📧 **Email Notifications**: Get notified when prices drop below your target
- 📈 **Price History**: View price trends over time with interactive charts
- 🎨 **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- 🔐 **Secure Authentication**: JWT-based user authentication
- ⚡ **Real-time Updates**: Background workers check prices every 24 hours

## Tech Stack

### Backend
- **Framework**: Python 3.11+ with FastAPI
- **Database**: PostgreSQL 15+
- **Task Queue**: Celery with Redis
- **Web Scraping**: Playwright + BeautifulSoup4
- **Authentication**: JWT tokens with bcrypt

### Frontend
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context + React Query
- **Charts**: Recharts

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest + Hypothesis (property-based testing)

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)

### Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce-price-tracker
```

2. Copy environment variables:
```bash
cp backend/.env.example backend/.env
```

3. Start all services:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the development server:
```bash
uvicorn app.main:app --reload
```

#### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core utilities (database, logging, etc.)
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── scrapers/         # Web scraping modules
│   │   ├── repositories/     # Data access layer
│   │   └── tasks/            # Celery tasks
│   ├── alembic/              # Database migrations
│   ├── tests/                # Test suite
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API client
│   │   ├── contexts/         # React contexts
│   │   └── types/            # TypeScript types
│   └── package.json          # Node dependencies
└── docker-compose.yml        # Docker services configuration
```

## Testing

### Run Backend Tests

```bash
cd backend
pytest
```

### Run Property-Based Tests

```bash
pytest -m property_test
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

## Configuration

Key environment variables (see `backend/.env.example`):

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT secret key
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`: Email configuration
- `PRICE_CHECK_INTERVAL_HOURS`: How often to check prices (default: 24)

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.
