#!/bin/bash

echo "🚀 RapidAPI Scraper - Installation and Testing"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    echo "💡 Please run this script from the rapidapi_version directory"
    exit 1
fi

echo "📦 Step 1: Installing dependencies..."
echo "This may take a few minutes..."
echo ""

pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Installation failed!"
    echo "💡 Try running: pip3 install --upgrade pip"
    exit 1
fi

echo ""
echo "✅ Dependencies installed successfully!"
echo ""
echo "🧪 Step 2: Running verification tests..."
echo "This will test each scraper (takes 30-60 seconds)..."
echo ""

python3 verify_scrapers.py

exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo "🎉 All tests passed! Your API is ready!"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Start the API: python3 run_api.py"
    echo "   2. Visit: http://localhost:8000/docs"
    echo "   3. Test the API: python3 test_api.py"
else
    echo "⚠️  Some tests failed. Check the output above."
fi

exit $exit_code
