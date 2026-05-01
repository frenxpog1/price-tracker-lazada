#!/bin/bash

echo "================================"
echo "Backend Startup Checker"
echo "================================"

echo ""
echo "1. Checking .env file..."
if [ -f ".env" ]; then
    echo "   ✓ .env file exists"
    if grep -q "USE_REAL_SCRAPERS=true" .env; then
        echo "   ✓ USE_REAL_SCRAPERS=true found in .env"
    else
        echo "   ✗ USE_REAL_SCRAPERS=true NOT found in .env"
        echo "   Current value:"
        grep "USE_REAL_SCRAPERS" .env || echo "   (not set)"
    fi
else
    echo "   ✗ .env file not found!"
fi

echo ""
echo "2. Checking Python environment..."
if command -v python3 &> /dev/null; then
    echo "   ✓ python3 found: $(python3 --version)"
else
    echo "   ✗ python3 not found"
fi

echo ""
echo "3. Checking virtual environment..."
if [ -d "venv" ]; then
    echo "   ✓ venv directory exists"
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "   ✓ Virtual environment is activated"
        echo "     Path: $VIRTUAL_ENV"
    else
        echo "   ✗ Virtual environment NOT activated"
        echo "     Run: source venv/bin/activate"
    fi
else
    echo "   ✗ venv directory not found"
    echo "     Run: python3 -m venv venv"
fi

echo ""
echo "4. Checking required files..."
files=(
    "app/scrapers/lazada_api_scraper.py"
    "app/scrapers/scraper_factory.py"
    "app/services/search_service.py"
    "app/api/products.py"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file (missing!)"
    fi
done

echo ""
echo "5. Checking if backend is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✓ Backend is running on port 8000"
else
    echo "   ✗ Backend is NOT running"
    echo "     Start with: python -m uvicorn app.main:app --reload"
fi

echo ""
echo "================================"
echo "Quick Start Commands:"
echo "================================"
echo ""
echo "# Activate virtual environment"
echo "source venv/bin/activate"
echo ""
echo "# Install dependencies (if needed)"
echo "pip install -r requirements.txt"
echo ""
echo "# Start backend with real scrapers"
echo "export USE_REAL_SCRAPERS=true"
echo "python -m uvicorn app.main:app --reload"
echo ""
echo "# Or use .env file (recommended)"
echo "# Make sure .env has: USE_REAL_SCRAPERS=true"
echo "python -m uvicorn app.main:app --reload"
echo ""
