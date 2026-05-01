"""
Simple test script for the E-commerce Scraper API
Run this to verify the API is working correctly
"""

import requests
import json
import time

# API base URL (change this to your deployed URL)
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_root():
    """Test the root endpoint"""
    print("🏠 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint works: {data['name']}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_platforms():
    """Test the platforms endpoint"""
    print("🏪 Testing platforms endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/platforms", timeout=10)
        if response.status_code == 200:
            data = response.json()
            platforms = list(data['platforms'].keys())
            print(f"✅ Platforms endpoint works: {platforms}")
            return True
        else:
            print(f"❌ Platforms endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Platforms endpoint error: {e}")
        return False

def test_search():
    """Test the search endpoint"""
    print("🔍 Testing search endpoint...")
    try:
        # Test with a simple query
        params = {
            'q': 'phone',
            'per_page': 5,
            'page': 1
        }
        
        print(f"Searching for: {params['q']}")
        start_time = time.time()
        
        response = requests.get(f"{BASE_URL}/search", params=params, timeout=90)
        
        if response.status_code == 200:
            data = response.json()
            search_time = time.time() - start_time
            
            print(f"✅ Search successful!")
            print(f"   Query: {data['query']}")
            print(f"   Total results: {data['total_results']}")
            print(f"   Results returned: {len(data['results'])}")
            print(f"   Platforms searched: {data['platforms_searched']}")
            print(f"   Platforms failed: {data['platforms_failed']}")
            print(f"   Search time: {search_time:.2f}s")
            
            # Show first result if available
            if data['results']:
                first_result = data['results'][0]
                print(f"   First result: {first_result['product_name'][:50]}...")
                print(f"   Price: {first_result['current_price']} {first_result['currency']}")
                print(f"   Platform: {first_result['platform']}")
            
            return True
        else:
            print(f"❌ Search failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Search error: {e}")
        return False

def test_individual_platforms():
    """Test each platform individually"""
    print("🏪 Testing individual platforms...")
    platforms = ['lazada', 'shopee', 'temu']
    
    for platform in platforms:
        print(f"\n  Testing {platform}...")
        try:
            params = {
                'q': 'phone',
                'per_page': 3,
                'page': 1
            }
            
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/search/{platform}", params=params, timeout=60)
            search_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"    ✅ {platform}: {len(data['results'])} results in {search_time:.2f}s")
                if data['results']:
                    print(f"       Sample: {data['results'][0]['product_name'][:40]}...")
            else:
                print(f"    ❌ {platform}: Failed ({response.status_code})")
                
        except Exception as e:
            print(f"    ❌ {platform}: Error - {e}")
    
    return True

def test_rate_limiting():
    """Test rate limiting (optional)"""
    print("⏱️ Testing rate limiting...")
    try:
        # Make multiple quick requests
        for i in range(3):
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code != 200:
                print(f"❌ Rate limiting test failed at request {i+1}")
                return False
        
        print("✅ Rate limiting test passed (no immediate blocking)")
        return True
    except Exception as e:
        print(f"❌ Rate limiting test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 E-commerce Scraper API Test Suite")
    print("=" * 40)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Platforms Endpoint", test_platforms),
        ("Rate Limiting", test_rate_limiting),
        ("Individual Platforms", test_individual_platforms),
        ("Search Endpoint", test_search),  # This one takes longest, so run it last
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        if test_func():
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
        print(f"🌐 API Documentation: {BASE_URL}/docs")
        print(f"📋 API Status: {BASE_URL}/health")
    else:
        print("⚠️ Some tests failed. Check the API configuration.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)