# Deployment Guide

## 🚀 Quick Deploy Options

### Option 1: Local Testing (Fastest)

```bash
cd lazada_api_production
pip install -r requirements.txt
python3 main.py
```

Open http://localhost:8000/docs to test

### Option 2: Heroku (Free Tier Available)

1. **Install Heroku CLI**
```bash
brew install heroku/brew/heroku  # Mac
# or download from heroku.com
```

2. **Create Heroku app**
```bash
heroku login
heroku create your-lazada-api
```

3. **Add buildpacks** (for Chrome)
```bash
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add --index 3 https://github.com/heroku/heroku-buildpack-chromedriver
```

4. **Create Procfile**
```bash
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
```

5. **Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

6. **Open your API**
```bash
heroku open
```

### Option 3: Railway.app (Recommended - Easy & Fast)

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select this folder
4. Railway auto-detects Python and deploys
5. Add environment variable: `PORT=8000`
6. Get your public URL

### Option 4: Render.com (Free Tier)

1. Go to [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub repo
4. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python3 main.py`
5. Deploy!

### Option 5: Fly.io (Global Edge Network)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch app
flyctl launch

# Deploy
flyctl deploy
```

### Option 6: DigitalOcean App Platform

1. Go to DigitalOcean
2. Create new App
3. Connect GitHub
4. Select Python
5. Deploy

### Option 7: AWS Lambda (Serverless)

Use Mangum adapter:
```python
from mangum import Mangum
handler = Mangum(app)
```

Deploy with AWS SAM or Serverless Framework

## 🔧 Environment Variables

No environment variables required! API works out of the box.

Optional:
- `PORT` - Port to run on (default: 8000)
- `LOG_LEVEL` - Logging level (default: INFO)

## 📊 Performance Tuning

### For High Traffic:

1. **Add Redis Caching**
```python
import redis
cache = redis.Redis(host='localhost', port=6379)
```

2. **Use Gunicorn** (multiple workers)
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. **Add Rate Limiting**
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
```

## 🐳 Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install Chrome
RUN apt-get update && apt-get install -y \\
    wget gnupg unzip && \\
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \\
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \\
    apt-get update && apt-get install -y google-chrome-stable && \\
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "main.py"]
```

**Build and run:**
```bash
docker build -t lazada-api .
docker run -p 8000:8000 lazada-api
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    restart: always
```

## 🌐 RapidAPI Marketplace

1. **Deploy to any cloud** (get public URL)
2. **Go to RapidAPI Hub**
3. **Add New API**
4. **Configure:**
   - Base URL: Your deployed URL
   - Endpoints: Import from OpenAPI spec
   - Pricing: Set your rates
5. **Publish!**

## 🔒 Security (Production)

### Add API Key Authentication:

```python
from fastapi.security import APIKeyHeader
from fastapi import Security, HTTPException

API_KEY = "your-secret-key"
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.get("/search", dependencies=[Depends(verify_api_key)])
async def search_products(...):
    ...
```

### Add Rate Limiting:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/search")
@limiter.limit("10/minute")
async def search_products(request: Request, ...):
    ...
```

## 📈 Monitoring

### Add Logging:

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Add Health Checks:

Already included at `/health` endpoint

### Add Metrics:

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## 🐛 Troubleshooting

**Chrome not found:**
```bash
# Ubuntu/Debian
sudo apt-get install google-chrome-stable

# Mac
brew install --cask google-chrome
```

**Port already in use:**
```bash
# Change port in main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Slow first request:**
- Normal (Chrome initialization)
- Consider keeping Chrome instance alive
- Use connection pooling

## 💰 Pricing Suggestions (RapidAPI)

- **Free Tier**: 100 requests/month
- **Basic**: $9.99/month - 1,000 requests
- **Pro**: $49.99/month - 10,000 requests
- **Ultra**: $199.99/month - 100,000 requests

## 📞 Support

Check logs for errors:
```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# Docker
docker logs container-name
```

---

**Ready to deploy!** Choose your platform and follow the steps above. 🚀
