# Deployment Checklist ✅

Use this checklist to deploy your price tracker to production.

## Pre-Deployment

- [x] Code changes completed
- [x] Lazada API production service ready (`lazada_api_production/`)
- [ ] Render account created (https://render.com)
- [ ] Vercel account created (https://vercel.com)
- [x] Supabase database set up
- [x] Google OAuth credentials configured

---

## Step 1: Deploy Lazada Scraper to Render

- [ ] Go to https://dashboard.render.com
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub repository
- [ ] Configure service:
  - [ ] Name: `lazada-scraper-api`
  - [ ] Region: Singapore (or closest to users)
  - [ ] Root Directory: `lazada_api_production`
  - [ ] Runtime: Python 3
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
  - [ ] Instance Type: Free (or Starter for $7/month)
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (5-10 minutes)
- [ ] Copy the service URL: `https://______________.onrender.com`
- [ ] Test the service: Visit `https://your-url.onrender.com/health`
- [ ] Test search: Visit `https://your-url.onrender.com/search?q=laptop&per_page=5`

**Render URL:** `_________________________________` ← Write it here!

---

## Step 2: Update Local Environment

- [ ] Open `backend/.env`
- [ ] Update `LAZADA_API_URL` with your Render URL
- [ ] Save the file
- [ ] Test locally (optional):
  ```bash
  cd backend
  python test_api_scraper.py
  ```

---

## Step 3: Deploy Backend to Vercel

- [ ] Go to https://vercel.com/dashboard
- [ ] Click "Add New..." → "Project"
- [ ] Import your GitHub repository
- [ ] Configure project:
  - [ ] Project Name: `price-tracker-lazada-uuyz`
  - [ ] Framework: Other
  - [ ] Root Directory: `backend`
- [ ] Add Environment Variables (Settings → Environment Variables):
  - [ ] `DATABASE_URL` = `your-supabase-database-url`
  - [ ] `SECRET_KEY` = `your-super-secret-key-change-this-in-production`
  - [ ] `GOOGLE_CLIENT_ID` = `your-google-client-id`
  - [ ] `GOOGLE_CLIENT_SECRET` = `your-google-client-secret`
  - [ ] `DEBUG` = `False`
  - [ ] `CORS_ORIGINS` = `["https://price-tracker-lazada.vercel.app","http://localhost:3000","http://localhost:5173"]`
  - [ ] `LAZADA_API_URL` = `https://your-render-url.onrender.com` ← Use your actual URL!
- [ ] Select "All Environments" for each variable
- [ ] Click "Deploy"
- [ ] Wait for deployment
- [ ] Test: Visit `https://price-tracker-lazada-uuyz.vercel.app/health`

**Backend URL:** `_________________________________` ← Write it here!

---

## Step 4: Deploy Frontend to Vercel

- [ ] Go to https://vercel.com/dashboard
- [ ] Click "Add New..." → "Project"
- [ ] Import your GitHub repository (same repo, different project)
- [ ] Configure project:
  - [ ] Project Name: `price-tracker-lazada`
  - [ ] Framework: Vite
  - [ ] Root Directory: `frontend`
  - [ ] Build Command: `npm run build`
  - [ ] Output Directory: `dist`
- [ ] Add Environment Variables:
  - [ ] `VITE_GOOGLE_CLIENT_ID` = `your-google-client-id`
  - [ ] `VITE_API_URL` = `https://price-tracker-lazada-uuyz.vercel.app`
- [ ] Select "All Environments" for each variable
- [ ] Click "Deploy"
- [ ] Wait for deployment
- [ ] Test: Visit `https://price-tracker-lazada.vercel.app`

**Frontend URL:** `_________________________________` ← Write it here!

---

## Step 5: Update Google OAuth

- [ ] Go to https://console.cloud.google.com
- [ ] Select your project
- [ ] Go to "APIs & Services" → "Credentials"
- [ ] Click on your OAuth 2.0 Client ID
- [ ] Under "Authorized JavaScript origins", add:
  - [ ] `https://price-tracker-lazada.vercel.app`
- [ ] Under "Authorized redirect URIs", add:
  - [ ] `https://price-tracker-lazada.vercel.app`
- [ ] Click "Save"

---

## Step 6: Test Everything

### Test Render Service
- [ ] Visit: `https://your-render-url.onrender.com/`
- [ ] Should see: `{"name": "Lazada Product Scraper API", "status": "healthy"}`
- [ ] Visit: `https://your-render-url.onrender.com/search?q=laptop&per_page=5`
- [ ] Should see: JSON with product results

### Test Backend
- [ ] Visit: `https://price-tracker-lazada-uuyz.vercel.app/health`
- [ ] Should see: `{"status": "healthy", "app_name": "E-commerce Price Tracker"}`
- [ ] Visit: `https://price-tracker-lazada-uuyz.vercel.app/docs`
- [ ] Should see: API documentation (if DEBUG=True)

### Test Frontend
- [ ] Visit: `https://price-tracker-lazada.vercel.app`
- [ ] Should see: Login page
- [ ] Click "Sign in with Google"
- [ ] Complete Google login
- [ ] Should redirect to dashboard

### Test Search Functionality
- [ ] After logging in, search for "laptop"
- [ ] Wait 6-10 seconds (or 30-60 seconds if Render is cold starting)
- [ ] Should see: Lazada products with prices and images
- [ ] Click on a product
- [ ] Should open: Lazada product page in new tab

---

## Troubleshooting

### Issue: Search returns "LAZADA_API_URL environment variable is not set"
- [ ] Go to Vercel → Backend project → Settings → Environment Variables
- [ ] Verify `LAZADA_API_URL` is set correctly
- [ ] Redeploy backend

### Issue: Search times out or returns no results
- [ ] Visit Render service URL to wake it up
- [ ] Wait 30-60 seconds for cold start
- [ ] Try search again
- [ ] Check Render logs for errors

### Issue: Google OAuth shows "invalid_client"
- [ ] Verify `GOOGLE_CLIENT_ID` matches in frontend and Google Console
- [ ] Verify authorized origins include frontend URL
- [ ] Redeploy frontend

### Issue: CORS errors in browser console
- [ ] Check `CORS_ORIGINS` in backend includes frontend URL
- [ ] Format must be JSON array: `["https://..."]`
- [ ] Redeploy backend

---

## Post-Deployment

- [ ] Test all features thoroughly
- [ ] Monitor Render logs for errors
- [ ] Monitor Vercel logs for errors
- [ ] Set up monitoring/alerts (optional)
- [ ] Consider upgrading Render to paid plan ($7/month) to eliminate cold starts

---

## Performance Optimization (Optional)

- [ ] Upgrade Render to Starter plan ($7/month) for no cold starts
- [ ] Add loading message for cold starts in frontend
- [ ] Set up keep-alive service to ping Render every 10 minutes
- [ ] Enable Vercel Analytics
- [ ] Add error tracking (Sentry, etc.)

---

## Success Criteria

✅ All services are deployed and running
✅ Health checks pass for all services
✅ Google OAuth login works
✅ Product search returns results
✅ Images display correctly
✅ Prices are formatted properly
✅ No errors in browser console
✅ No errors in Vercel logs
✅ No errors in Render logs

---

## Completion

- [ ] All steps completed
- [ ] All tests passed
- [ ] App is live and working
- [ ] Documentation updated
- [ ] Team notified (if applicable)

**Deployment Date:** _______________

**Deployed By:** _______________

**Notes:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## 🎉 Congratulations!

Your E-commerce Price Tracker is now live in production!

**URLs:**
- Frontend: https://price-tracker-lazada.vercel.app
- Backend: https://price-tracker-lazada-uuyz.vercel.app
- Scraper: https://your-render-url.onrender.com

Share it with your users and start tracking prices! 🚀
