# 🔗 How to Update Your Render URL

After deploying your Lazada scraper to Render, you'll get a URL like:
```
https://lazada-scraper-xyz.onrender.com
```

You need to add this URL to **3 places**. Here's how:

---

## 1️⃣ Local Development (.env file)

**File:** `backend/.env`

**Find this line:**
```env
LAZADA_API_URL=https://your-render-service.onrender.com
```

**Replace with your actual URL:**
```env
LAZADA_API_URL=https://lazada-scraper-xyz.onrender.com
```

**How to do it:**
```bash
# Open the file
cd backend
nano .env  # or use your favorite editor

# Update the line
# Save and close
```

---

## 2️⃣ Vercel Backend (Environment Variables)

**Where:** Vercel Dashboard → Backend Project → Settings → Environment Variables

**Steps:**

1. Go to https://vercel.com/dashboard
2. Click on your **backend** project: `price-tracker-lazada-uuyz`
3. Click **Settings** (top menu)
4. Click **Environment Variables** (left sidebar)
5. Find `LAZADA_API_URL` or click **Add New**
6. Enter:
   - **Key**: `LAZADA_API_URL`
   - **Value**: `https://lazada-scraper-xyz.onrender.com` (your actual URL)
   - **Environments**: Select all (Production, Preview, Development)
7. Click **Save**

**Visual:**
```
┌─────────────────────────────────────────────────────────┐
│  Environment Variables                                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Key:   LAZADA_API_URL                                 │
│  Value: https://lazada-scraper-xyz.onrender.com        │
│                                                         │
│  Environments:                                          │
│  ☑ Production                                           │
│  ☑ Preview                                              │
│  ☑ Development                                          │
│                                                         │
│  [Save]                                                 │
└─────────────────────────────────────────────────────────┘
```

---

## 3️⃣ Documentation (Optional)

**File:** `VERCEL_ENV_VARIABLES.md`

**Find this line:**
```markdown
LAZADA_API_URL=https://your-render-service.onrender.com
```

**Replace with your actual URL:**
```markdown
LAZADA_API_URL=https://lazada-scraper-xyz.onrender.com
```

This is optional but helps keep your documentation accurate.

---

## ✅ Verification Checklist

After updating all 3 places:

- [ ] Updated `backend/.env` with Render URL
- [ ] Added `LAZADA_API_URL` to Vercel environment variables
- [ ] Selected all environments (Production, Preview, Development)
- [ ] Clicked Save in Vercel
- [ ] (Optional) Updated `VERCEL_ENV_VARIABLES.md`

---

## 🧪 Test Your Setup

### Test Locally (Optional)

```bash
cd backend
python test_api_scraper.py
```

Expected output:
```
============================================================
Testing Lazada API Scraper
============================================================
✅ LAZADA_API_URL is set: https://lazada-scraper-xyz.onrender.com
✅ Successfully imported LazadaAPIScraper

Testing search for 'laptop'...
------------------------------------------------------------
✅ Search successful!
   Total results: 1234
   Products returned: 5

Sample products:

1. Laptop ASUS VivoBook...
   Price: PHP 25999
   URL: https://www.lazada.com.ph/...
   Image: https://...

============================================================
✅ All tests passed! Your setup is ready for deployment.
============================================================
```

### Test on Vercel

After redeploying:

1. Visit: `https://price-tracker-lazada-uuyz.vercel.app/health`
2. Should see: `{"status":"healthy",...}`
3. Visit: `https://price-tracker-lazada.vercel.app`
4. Login and search for "laptop"
5. Should see results in 6-10 seconds

---

## 🚨 Common Mistakes

### ❌ Wrong: Using placeholder URL
```env
LAZADA_API_URL=https://your-render-service.onrender.com
```

### ✅ Right: Using actual Render URL
```env
LAZADA_API_URL=https://lazada-scraper-xyz.onrender.com
```

### ❌ Wrong: Adding to frontend project
The `LAZADA_API_URL` should be added to the **backend** project, not frontend.

### ✅ Right: Adding to backend project
Vercel → `price-tracker-lazada-uuyz` (backend) → Settings → Environment Variables

### ❌ Wrong: Not selecting all environments
Only selecting "Production" means it won't work in Preview or Development.

### ✅ Right: Selecting all environments
☑ Production ☑ Preview ☑ Development

---

## 🔄 After Updating

### If you updated local .env:
```bash
# Restart your local backend server
cd backend
# Stop the server (Ctrl+C)
# Start it again
uvicorn app.main:app --reload
```

### If you updated Vercel:
1. Go to **Deployments** tab
2. Click **"..."** on latest deployment
3. Click **"Redeploy"**
4. Wait 1-2 minutes

---

## 📋 Quick Copy-Paste Template

Once you have your Render URL, use this template:

```bash
# For backend/.env
LAZADA_API_URL=https://YOUR-ACTUAL-URL.onrender.com

# For Vercel (copy this value)
https://YOUR-ACTUAL-URL.onrender.com
```

**Replace `YOUR-ACTUAL-URL` with your actual Render service name!**

---

## 🎯 Example

Let's say your Render URL is:
```
https://lazada-scraper-api-abc123.onrender.com
```

Then you would:

1. **Local .env:**
```env
LAZADA_API_URL=https://lazada-scraper-api-abc123.onrender.com
```

2. **Vercel:**
- Key: `LAZADA_API_URL`
- Value: `https://lazada-scraper-api-abc123.onrender.com`

3. **Test:**
```bash
python test_api_scraper.py
```

---

## ✅ Success Criteria

You know it's working when:

- ✅ `python test_api_scraper.py` passes all tests
- ✅ Vercel backend health check returns healthy
- ✅ Frontend search returns Lazada products
- ✅ No errors in browser console
- ✅ No errors in Vercel logs

---

## 🆘 Troubleshooting

### Error: "LAZADA_API_URL environment variable is not set"

**Cause:** Variable not added to Vercel or not redeployed

**Solution:**
1. Check Vercel → Backend → Settings → Environment Variables
2. Verify `LAZADA_API_URL` exists
3. Redeploy the backend

### Error: "Cannot connect to Lazada API"

**Cause:** Render service URL is wrong or service is down

**Solution:**
1. Visit your Render URL in browser: `https://your-url.onrender.com/health`
2. Should see: `{"status":"healthy",...}`
3. If not, check Render dashboard for errors

### Error: Search times out

**Cause:** Render free tier is cold starting

**Solution:**
1. Wait 30-60 seconds
2. Try again
3. Consider upgrading Render to paid plan ($7/month)

---

## 📞 Need Help?

If you're stuck:
1. Double-check all 3 places have the correct URL
2. Make sure URL starts with `https://`
3. Make sure URL ends with `.onrender.com` (no trailing slash)
4. Run `python test_api_scraper.py` to diagnose
5. Check Render logs for errors
6. Check Vercel logs for errors

---

**Next:** After updating the URL, continue with [QUICK_START.md](QUICK_START.md) Step 3 (Redeploy Backend)
