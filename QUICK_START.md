# Quick Start - Get Search Working on Vercel

## What Changed?

Your backend now calls an **external Lazada scraper API** (hosted on Render) instead of running Selenium directly in Vercel. This is necessary because Vercel's serverless functions don't support browser automation.

## Architecture

```
User → Frontend (Vercel) → Backend API (Vercel) → Lazada Scraper (Render) → Lazada.com.ph
```

## Quick Deployment Steps

### 1. Deploy Lazada Scraper to Render (5 minutes)

1. Go to https://dashboard.render.com
2. Create **New Web Service**
3. Connect your GitHub repo
4. Settings:
   - Root Directory: `lazada_api_production`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy and copy the URL (e.g., `https://lazada-scraper-xyz.onrender.com`)

### 2. Add Environment Variable to Vercel Backend (2 minutes)

1. Go to https://vercel.com/dashboard
2. Select your **backend** project (`price-tracker-lazada-uuyz`)
3. Go to **Settings** → **Environment Variables**
4. Add new variable:
   - **Key**: `LAZADA_API_URL`
   - **Value**: `https://your-render-url.onrender.com` (from step 1)
   - **Environments**: Select all (Production, Preview, Development)
5. Click **Save**

### 3. Redeploy Backend (1 minute)

1. Go to **Deployments** tab
2. Click **"..."** on the latest deployment
3. Click **"Redeploy"**
4. Wait for deployment to complete

### 4. Test It! (30 seconds)

1. Visit your frontend: `https://price-tracker-lazada.vercel.app`
2. Login with Google
3. Search for "laptop"
4. Wait 6-10 seconds (first search may take 30-60 seconds if Render service was sleeping)
5. See results! 🎉

## Important Notes

⚠️ **First Search Delay**: Render's free tier spins down after 15 minutes of inactivity. The first search after inactivity will take 30-60 seconds while the service wakes up. Subsequent searches are fast (6-10 seconds).

💡 **Solution**: Upgrade Render to paid plan ($7/month) for no cold starts, or add a loading message to set user expectations.

## Files Changed

- ✅ `backend/app/scrapers/lazada_api_scraper.py` - New API-based scraper
- ✅ `backend/app/scrapers/scraper_factory.py` - Updated to use API scraper
- ✅ `backend/app/config.py` - Added `LAZADA_API_URL` setting
- ✅ `backend/requirements.txt` - Removed Selenium/Playwright (not needed)
- ✅ `backend/.env` - Added `LAZADA_API_URL`
- ✅ `VERCEL_ENV_VARIABLES.md` - Updated with new variable
- ✅ `DEPLOYMENT_GUIDE.md` - Complete deployment guide

## Troubleshooting

### Search returns error "LAZADA_API_URL environment variable is not set"
→ Add the environment variable in Vercel (Step 2 above)

### Search times out or returns no results
→ Render service is cold starting. Wait 30-60 seconds and try again.
→ Visit `https://your-render-url.onrender.com/health` to wake it up.

### Still not working?
→ Check Render logs: https://dashboard.render.com → Your service → Logs
→ Check Vercel logs: https://vercel.com/dashboard → Your project → Deployments → Logs

## Next Steps

1. Deploy to Render ✓
2. Add `LAZADA_API_URL` to Vercel ✓
3. Redeploy backend ✓
4. Test search ✓
5. (Optional) Add better loading UI for cold starts
6. (Optional) Upgrade Render to paid plan for better performance

That's it! Your search should now work on Vercel. 🚀
