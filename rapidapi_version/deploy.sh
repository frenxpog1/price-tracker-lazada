#!/bin/bash

# E-commerce Scraper API Deployment Script
# This script helps deploy the API to various platforms

set -e

echo "🚀 E-commerce Scraper API Deployment"
echo "===================================="

# Function to display usage
usage() {
    echo "Usage: $0 [OPTION]"
    echo "Options:"
    echo "  local     - Run locally for development"
    echo "  docker    - Build and run with Docker"
    echo "  test      - Run API tests"
    echo "  build     - Build Docker image only"
    echo "  clean     - Clean up Docker containers and images"
    echo "  help      - Show this help message"
    exit 1
}

# Function to run locally
run_local() {
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    echo "🔧 Starting API server locally..."
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
}

# Function to build Docker image
build_docker() {
    echo "🐳 Building Docker image..."
    docker build -t ecommerce-scraper-api:latest .
    echo "✅ Docker image built successfully!"
}

# Function to run with Docker
run_docker() {
    build_docker
    
    echo "🚀 Starting API with Docker..."
    docker run -d \
        --name ecommerce-scraper-api \
        -p 8000:8000 \
        --restart unless-stopped \
        ecommerce-scraper-api:latest
    
    echo "✅ API is running at http://localhost:8000"
    echo "📚 API docs available at http://localhost:8000/docs"
}

# Function to run tests
run_tests() {
    echo "🧪 Running API tests..."
    
    # Start API in background
    uvicorn main:app --host 0.0.0.0 --port 8001 &
    API_PID=$!
    
    # Wait for API to start
    sleep 5
    
    # Test health endpoint
    echo "Testing health endpoint..."
    curl -f http://localhost:8001/health || { echo "❌ Health check failed"; kill $API_PID; exit 1; }
    
    # Test search endpoint
    echo "Testing search endpoint..."
    curl -f "http://localhost:8001/search?q=test" || { echo "❌ Search test failed"; kill $API_PID; exit 1; }
    
    # Test platforms endpoint
    echo "Testing platforms endpoint..."
    curl -f http://localhost:8001/platforms || { echo "❌ Platforms test failed"; kill $API_PID; exit 1; }
    
    # Clean up
    kill $API_PID
    
    echo "✅ All tests passed!"
}

# Function to clean up Docker
clean_docker() {
    echo "🧹 Cleaning up Docker containers and images..."
    
    # Stop and remove container
    docker stop ecommerce-scraper-api 2>/dev/null || true
    docker rm ecommerce-scraper-api 2>/dev/null || true
    
    # Remove image
    docker rmi ecommerce-scraper-api:latest 2>/dev/null || true
    
    echo "✅ Cleanup completed!"
}

# Function to show deployment info
show_info() {
    echo "📋 Deployment Information"
    echo "========================"
    echo "API Title: E-commerce Product Scraper API"
    echo "Version: 1.0.0"
    echo "Port: 8000"
    echo "Health Check: /health"
    echo "Documentation: /docs"
    echo "OpenAPI Spec: /openapi.json"
    echo ""
    echo "🔗 Endpoints:"
    echo "  GET /search - Search products"
    echo "  GET /search/{platform} - Platform-specific search"
    echo "  GET /platforms - List supported platforms"
    echo "  GET /health - Health check"
    echo ""
    echo "📊 Rate Limits:"
    echo "  Default: 100 requests/hour per IP"
    echo "  Burst: 10 requests/minute"
    echo ""
    echo "🚀 For RapidAPI deployment:"
    echo "  1. Upload this code to your hosting platform"
    echo "  2. Set environment variables from .env.example"
    echo "  3. Configure the API endpoint in RapidAPI"
    echo "  4. Set up rate limiting and pricing tiers"
}

# Main script logic
case "${1:-help}" in
    local)
        run_local
        ;;
    docker)
        run_docker
        ;;
    build)
        build_docker
        ;;
    test)
        run_tests
        ;;
    clean)
        clean_docker
        ;;
    info)
        show_info
        ;;
    help|*)
        usage
        ;;
esac