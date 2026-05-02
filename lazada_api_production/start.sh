#!/bin/bash

# Startup script for Render deployment
# Browsers should already be installed during build phase

echo "🚀 Starting Lazada API..."

# Start the FastAPI application
echo "🌐 Starting FastAPI server..."
python main.py
