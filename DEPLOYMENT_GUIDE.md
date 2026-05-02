# Deployment Guide - E-commerce Price Tracker

This guide will help you deploy your price tracker application to production using Vercel (frontend + backend) and Render (Lazada scraper service).

## Architecture Overview

```
┌─────────────────┐
│  Frontend       │
│  (Vercel)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Backend API    │─────▶│  Lazada Scraper  │
│  (Vercel)       │      │  (Render)        │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│  Database       │
│  (Supabase)     │
└─────────────────┘
```

## Prerequisites

- [x] Vercel account (https://vercel.com)
- [x] Render account (https://render.com)
- [x] Supabase database (already set up)
- [x] Google OAuth credentials (already set up)

---

## Step 1: Deploy Lazada Scraper to Render

### 1.1 Create New Web Service on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `lazada-scraper-api` (or your preferred name)
   - **Region**: Choose closest to your users (e.g., Singapore)
   - **Branch**: `main`
   - **Root Directory**: `lazada_api_production`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free (or paid for better performance)

5. Click **"Create Web Service"**

### 1.2 Wait for Deployment

- Render will build and deploy your service
- This takes 5-10 minutes for the first deployment
- Once deployed, you'll get a URL like: `https://lazada-scraper-api.onrender.com`

### 1.3 Test the Scraper API

Visit your Render URL in a browser:
```
https://your-service.onrender.com/
```

You should see:
```json
{
  "name": "Lazada Product Scraper API",
  "version": "1.0.0",
  "status": "healthy"
}
```

Test the search endpoint:
```
https://your-service.onrender.com/search?q=laptop&per_page=5
```

**Important Note**: The first request may take 30-60 seconds because Render's free tier spins down after inactivity. Subsequent requests will be faster.

---

## Step 2: Deploy Backend to Vercel

### 2.1 Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

Or use the Vercel dashboard (recommended for first deployment).

### 2.2 Deploy via Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure the project:
   - **Project Name**: `price-tracker-lazada-uuyz` (or your preferred name)
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)

### 2.3 Add Environment Variables

Go to **Settings** → **Environment Variables** and add these:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `your-supabase-database-url` |
| `SECRET_KEY` | `your-super-secret-key-change-this-in-production` |
| `GOOGLE_CLIENT_ID` | `your-google-client-id` |
| `GOOGLE_CLIENT_SECRET` | `your-google-client-secret` |
| `DEBUG` | `False` |
| `CORS_ORIGINS` | `["https://price-tracker-lazada.vercel.app","http://localhost:3000","http://localhost:5173"]` |
| `LAZADA_API_URL` | `https://your-render-service.onrender.com` ⚠️ **Replace with your actual Render URL** |

**Important**: Replace `https://your-render-service.onrender.com` with your actual Render service URL from Step 1.2.

Select **All Environments** (Production, Preview, Development) for each variable.

### 2.4 Deploy

Click **"Deploy"** and wait for the deployment to complete.

Your backend will be available at: `https://price-tracker-lazada-uuyz.vercel.app`

### 2.5 Test the Backend

Visit:
```
https://price-tracker-lazada-uuyz.vercel.app/health
```

You should see:
```json
{
  "status": "healthy",
  "app_name": "E-commerce Price Tracker",
  "version": "1.0.0"
}
```

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Create New Project

1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository (same repo, different project)
4. Configure the project:
   - **Project Name**: `price-tracker-lazada`
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 3.2 Add Environment Variables

Go to **Settings** → **Environment Variables** and add:

| Key | Value |
|-----|-------|
| `VITE_GOOGLE_CLIENT_ID` | `your-google-client-id` |
| `VITE_API_URL` | `https://price-tracker-lazada-uuyz.vercel.app` |

Select **All Environments** for each variable.

### 3.3 Deploy

Click **"Deploy"** and wait for the deployment to complete.

Your frontend will be available at: `https://price-tracker-lazada.vercel.app`

---

## Step 4: Update Google OAuth Settings

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Go to **APIs & Services** → **Credentials**
4. Click on your OAuth 2.0 Client ID
5. Under **Authorized JavaScript origins**, ensure these are added:
   - `https://price-tracker-lazada.vercel.app`
   - `http://localhost:5173` (for local development)
6. Under **Authorized redirect URIs**, ensure these are added:
   - `https://price-tracker-lazada.vercel.app`
   - `http://localhost:5173` (for local development)
7. Click **Save**

---

## Step 5: Test the Complete System

### 5.1 Test Frontend
Visit: `https://price-tracker-lazada.vercel.app`

You should see the login page.

### 5.2 Test Google OAuth
1. Click **"Sign in with Google"**
2. Complete the Google login flow
3. You should be redirected back to the dashboard

### 5.3 Test Product Search
1. After logging in, go to the dashboard
2. Search for a product (e.g., "laptop")
3. Wait 6-10 seconds for results
4. You should see Lazada products with prices and images

**Note**: The first search after Render service inactivity may take 30-60 seconds because the service needs to spin up.

---

## Troubleshooting

### Issue: "LAZADA_API_URL environment variable is not set"

**Solution**: 
1. Go to Vercel dashboard → Your backend project → Settings → Environment Variables
2. Add `LAZADA_API_URL` with your Render service URL
3. Redeploy the backend

### Issue: Search returns no results or times out

**Possible causes**:
1. **Render service is cold starting**: Wait 30-60 seconds and try again
2. **Wrong Render URL**: Check that `LAZADA_API_URL` in Vercel matches your Render service URL
3. **Render service failed**: Check Render logs at https://dashboard.render.com

**Solution**:
- Visit your Render service URL directly to wake it up: `https://your-service.onrender.com/health`
- Check Render logs for errors
- Verify the Render service is running (green status in dashboard)

### Issue: Google OAuth shows "invalid_client"

**Solution**:
1. Verify `GOOGLE_CLIENT_ID` matches in both frontend and Google Cloud Console
2. Verify authorized origins include your Vercel frontend URL
3. Redeploy both frontend and backend after changes

### Issue: CORS errors in browser console

**Solution**:
1. Check that `CORS_ORIGINS` in backend includes your frontend URL
2. Format must be a JSON array: `["https://price-tracker-lazada.vercel.app"]`
3. Redeploy backend after changes

---

## Performance Optimization

### Render Free Tier Limitations

The free tier on Render spins down after 15 minutes of inactivity. This means:
- First request after inactivity: 30-60 seconds (cold start)
- Subsequent requests: 6-10 seconds (normal)

### Solutions:

1. **Upgrade to Paid Plan** ($7/month): No cold starts, always running
2. **Keep-Alive Service**: Set up a cron job to ping your service every 10 minutes
3. **User Expectation**: Show a loading message: "Waking up scraper service..."

### Recommended: Add Loading State

Update your frontend to show a better loading message:

```typescript
// In your search component
if (loading) {
  return (
    <div>
      <p>Searching Lazada products...</p>
      <p className="text-sm text-gray-500">
        First search may take 30-60 seconds while service wakes up
      </p>
    </div>
  );
}
```

---

## Monitoring

### Check Service Health

- **Frontend**: `https://price-tracker-lazada.vercel.app`
- **Backend**: `https://price-tracker-lazada-uuyz.vercel.app/health`
- **Scraper**: `https://your-render-service.onrender.com/health`

### View Logs

- **Vercel**: Dashboard → Project → Deployments → Click deployment → Logs
- **Render**: Dashboard → Service → Logs tab

---

## Cost Summary

| Service | Plan | Cost |
|---------|------|------|
| Vercel (Frontend) | Hobby | Free |
| Vercel (Backend) | Hobby | Free |
| Render (Scraper) | Free | Free (with cold starts) |
| Render (Scraper) | Starter | $7/month (no cold starts) |
| Supabase | Free | Free (up to 500MB) |
| **Total** | | **$0 - $7/month** |

---

## Next Steps

1. ✅ Deploy Lazada scraper to Render
2. ✅ Get Render service URL
3. ✅ Deploy backend to Vercel with `LAZADA_API_URL`
4. ✅ Deploy frontend to Vercel
5. ✅ Update Google OAuth settings
6. ✅ Test the complete system
7. 🎉 Your app is live!

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Vercel and Render logs
3. Verify all environment variables are set correctly
4. Test each service individually (scraper → backend → frontend)

Good luck with your deployment! 🚀
