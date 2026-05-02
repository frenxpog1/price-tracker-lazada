#!/bin/bash

# Startup script for Render deployment
# Ensures Playwright browsers are installed before starting the API

echo "🚀 Starting Lazada API..."

# Check if Playwright browsers are installed
if [ ! -d "/opt/render/.cache/ms-playwright" ]; then
    echo "📦 Installing Playwright browsers (first time setup)..."
    playwright install --with-deps chromium
    echo "✅ Playwright browsers installed!"
else
    echo "✅ Playwright browsers already installed"
fi

# Start the FastAPI application
echo "🌐 Starting FastAPI server..."
python main.py
