#!/usr/bin/env python3
"""
Simple script to run the E-commerce Scraper API locally for testing.
"""

import uvicorn
import sys
import os
import webbrowser
import time
from threading import Timer

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def open_dashboard():
    """Open the test dashboard in browser after a delay"""
    time.sleep(2)  # Wait for server to start
    dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_dashboard.html')
    if os.path.exists(dashboard_path):
        webbrowser.open(f'file://{dashboard_path}')
        print("\n🎨 Test dashboard opened in your browser!")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 E-commerce Scraper API - Starting...")
    print("=" * 60)
    print("\n📍 API Endpoints:")
    print("   📖 Documentation: http://localhost:8000/docs")
    print("   🏥 Health Check:  http://localhost:8000/health")
    print("   🔍 Search:        http://localhost:8000/search?q=phone&per_page=5")
    print("\n🎨 Test Dashboard:")
    print("   Opening test_dashboard.html in your browser...")
    print("\n⚠️  Important Notes:")
    print("   • First request may be slow (Chrome driver downloads)")
    print("   • Each search takes 5-15 seconds per platform")
    print("   • Press Ctrl+C to stop the server")
    print("\n" + "=" * 60)
    print("Starting server...\n")
    
    # Open dashboard in browser after server starts
    Timer(2.0, open_dashboard).start()
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("👋 API server stopped")
        print("=" * 60)