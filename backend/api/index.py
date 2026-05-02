"""
Vercel serverless function entry point for FastAPI backend.
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

# Vercel expects a variable named 'app' or 'handler'
handler = app
