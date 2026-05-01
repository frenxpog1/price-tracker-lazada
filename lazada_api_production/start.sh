#!/bin/bash

echo "=================================="
echo "Lazada API - Quick Start"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "   Please install Python 3.9 or higher"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed"
    exit 1
fi

echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "🚀 Starting Lazada API..."
echo ""
echo "   API will be available at:"
echo "   - http://localhost:8000"
echo "   - http://localhost:8000/docs (API Documentation)"
echo ""
echo "   Test dashboard:"
echo "   - Open test_dashboard.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 main.py
