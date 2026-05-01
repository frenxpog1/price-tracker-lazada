# E-commerce Product Scraper API

A fast, reliable API for scraping product information from major e-commerce platforms including Lazada, Shopee, and Temu. Perfect for price comparison, market research, and product discovery.

## 🚀 Features

- **Multi-Platform Support**: Search across Lazada, Shopee, and Temu
- **Real-Time Data**: Get current prices, availability, and product details
- **Pagination & Sorting**: Navigate through results with flexible sorting options
- **Rate Limiting**: Built-in protection against abuse
- **Fast Performance**: Optimized for speed with intelligent caching
- **OpenAPI Documentation**: Interactive API docs with examples
- **Error Handling**: Comprehensive error responses with helpful messages

## 📋 API Endpoints

### Search Products
```
GET /search?q={query}&page={page}&per_page={limit}&sort_by={sort}
```

**Parameters:**
- `q` (required): Search query (2-100 characters)
- `page` (optional): Page number (default: 1, max: 50)
- `per_page` (optional): Results per page (default: 20, max: 100)
- `sort_by` (optional): Sort order (`best_match`, `price_asc`, `price_desc`)
- `platform` (optional): Filter by platform (`lazada`, `shopee`, `temu`)

### Platform-Specific Search
```
GET /search/{platform}?q={query}
```

### Get Supported Platforms
```
GET /platforms
```

### Health Check
```
GET /health
```

## 📊 Response Format

```json
{
  "query": "iphone 15",
  "total_results": 1250,
  "page": 1,
  "per_page": 20,
  "results": [
    {
      "platform": "lazada",
      "product_name": "Apple iPhone 15 Pro Max 256GB",
      "current_price": 75990.00,
      "currency": "PHP",
      "product_url": "https://www.lazada.com.ph/products/...",
      "image_url": "https://ph-live-02.slatic.net/p/...",
      "availability": true,
      "scraped_at": "2024-01-01T12:00:00Z"
    }
  ],
  "platforms_searched": ["lazada"],
  "platforms_failed": [],
  "search_time_seconds": 2.45
}
```

## 🔧 Installation & Deployment

### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd rapidapi_version

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Deployment
```bash
# Build the image
docker build -t ecommerce-scraper-api .

# Run the container
docker run -p 8000:8000 ecommerce-scraper-api
```

### RapidAPI Deployment
1. Upload the code to your hosting platform
2. Set environment variables if needed
3. Configure the API endpoint in RapidAPI
4. Set up rate limiting and pricing tiers

## 📈 Rate Limits

- **Free Tier**: 100 requests per hour
- **Basic Tier**: 1,000 requests per hour
- **Pro Tier**: 10,000 requests per hour
- **Enterprise**: Custom limits

## 🛡️ Error Handling

The API returns structured error responses:

```json
{
  "error": "Rate limit exceeded",
  "code": "HTTP_429",
  "details": "Maximum 100 requests per hour"
}
```

**Common Error Codes:**
- `400`: Bad request (invalid parameters)
- `429`: Rate limit exceeded
- `500`: Internal server error
- `503`: Service unavailable (scraper issues)

## 🔍 Supported Platforms

| Platform | Status | Features |
|----------|--------|----------|
| Lazada | ✅ Active | Search, Pagination, Sorting, Images |
| Shopee | ✅ Active | Search, Pagination, Sorting, Images |
| Temu | ✅ Active | Search, Pagination, Sorting, Images |

## 📝 Usage Examples

### Python
```python
import requests

# Search for products
response = requests.get(
    "https://your-api-domain.com/search",
    params={
        "q": "laptop gaming",
        "page": 1,
        "per_page": 10,
        "sort_by": "price_asc"
    }
)

data = response.json()
for product in data["results"]:
    print(f"{product['product_name']}: ₱{product['current_price']}")
```

### JavaScript
```javascript
// Search for products
const response = await fetch(
    'https://your-api-domain.com/search?q=smartphone&per_page=5'
);
const data = await response.json();

data.results.forEach(product => {
    console.log(`${product.product_name}: ${product.current_price} ${product.currency}`);
});
```

### cURL
```bash
# Basic search
curl "https://your-api-domain.com/search?q=headphones&per_page=5"

# Platform-specific search with sorting
curl "https://your-api-domain.com/search/lazada?q=tablet&sort_by=price_asc"
```

## 🚀 Performance

- **Average Response Time**: 2-5 seconds
- **Concurrent Requests**: Up to 10 simultaneous requests
- **Uptime**: 99.9% availability
- **Data Freshness**: Real-time scraping

## 📞 Support

- **Documentation**: `/docs` endpoint for interactive API docs
- **Health Check**: `/health` endpoint for monitoring
- **Status Page**: Monitor API status and performance

## 📄 License

MIT License - see LICENSE file for details.

## 🔄 Changelog

### v1.0.0
- ✅ Lazada integration with full search, pagination, sorting, and images
- ✅ Shopee integration with full search, pagination, sorting, and images  
- ✅ Temu integration with full search, pagination, sorting, and images
- ✅ Rate limiting and error handling
- ✅ OpenAPI documentation
- ✅ Multi-platform search across all three platforms
- ✅ Platform-specific search endpoints

### Coming Soon
- Advanced filtering options (price range, ratings, etc.)
- Webhook notifications for price changes
- Bulk search endpoints
- Product tracking and alerts