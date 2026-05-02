# 🎨 Visual Deployment Guide

A visual, step-by-step guide to deploying your price tracker.

---

## 🏗️ Current Setup

```
┌─────────────────────────────────────────────────────────┐
│  YOUR COMPUTER                                          │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Code Repository (GitHub)                         │ │
│  │  ├── frontend/          (React app)               │ │
│  │  ├── backend/           (FastAPI)                 │ │
│  │  └── lazada_api_production/  (Scraper)           │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Target Architecture

```
┌──────────────────┐
│   👤 USER        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   🌐 FRONTEND    │─────▶│   ⚙️ BACKEND     │─────▶│   🤖 SCRAPER     │
│   (Vercel)       │      │   (Vercel)       │      │   (Render)       │
└──────────────────┘      └────────┬─────────┘      └──────────────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │   💾 DATABASE    │
                          │   (Supabase)     │
                          └──────────────────┘
```

---

## 📋 Step-by-Step Visual Guide

### Step 1: Deploy Scraper to Render 🤖

```
┌─────────────────────────────────────────────────────────────┐
│  RENDER DASHBOARD (https://dashboard.render.com)           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [+ New] ▼                                                  │
│    ├─ Web Service          ← Click this                    │
│    ├─ Static Site                                           │
│    └─ ...                                                   │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Connect Repository                                   │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  🔗 GitHub: your-repo                           │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │                                                       │ │
│  │  Name: lazada-scraper-api                            │ │
│  │  Region: Singapore                                   │ │
│  │  Root Directory: lazada_api_production               │ │
│  │  Build Command: pip install -r requirements.txt     │ │
│  │  Start Command: uvicorn main:app --host 0.0.0.0 ... │ │
│  │                                                       │ │
│  │  [Create Web Service]                                │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

⏱️  Wait 5-10 minutes for deployment...

✅ Success! Your URL: https://lazada-scraper-xyz.onrender.com
```

---

### Step 2: Add Environment Variable to Vercel ⚙️

```
┌─────────────────────────────────────────────────────────────┐
│  VERCEL DASHBOARD (https://vercel.com/dashboard)           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Projects                                                   │
│  ├─ price-tracker-lazada          (Frontend)               │
│  └─ price-tracker-lazada-uuyz     (Backend) ← Click this   │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Settings                                             │ │
│  │  ├─ General                                           │ │
│  │  ├─ Domains                                           │ │
│  │  ├─ Environment Variables      ← Click this          │ │
│  │  └─ ...                                               │ │
│  │                                                       │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  Add New Variable                               │ │ │
│  │  │                                                 │ │ │
│  │  │  Key:   LAZADA_API_URL                         │ │ │
│  │  │  Value: https://lazada-scraper-xyz.onrender.com│ │ │
│  │  │                                                 │ │ │
│  │  │  Environments:                                  │ │ │
│  │  │  ☑ Production                                   │ │ │
│  │  │  ☑ Preview                                      │ │ │
│  │  │  ☑ Development                                  │ │ │
│  │  │                                                 │ │ │
│  │  │  [Save]                                         │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

✅ Environment variable added!
```

---

### Step 3: Redeploy Backend ⚙️

```
┌─────────────────────────────────────────────────────────────┐
│  VERCEL - Backend Project                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Deployments                        ← Click this tab        │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Latest Deployment                                    │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  ✅ Production                                  │ │ │
│  │  │  main branch                                    │ │ │
│  │  │  2 minutes ago                                  │ │ │
│  │  │                                                 │ │ │
│  │  │  [⋮] ← Click                                    │ │ │
│  │  │    ├─ Visit                                     │ │ │
│  │  │    ├─ Redeploy      ← Click this                │ │ │
│  │  │    └─ ...                                       │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  ⚙️  Building...                                      │ │
│  │  ⏱️  This will take 1-2 minutes                       │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

⏱️  Wait 1-2 minutes...

✅ Deployment successful!
```

---

### Step 4: Test Everything ✅

#### 4.1 Test Scraper Service

```
🌐 Browser: https://lazada-scraper-xyz.onrender.com/health

┌─────────────────────────────────────────────────────────────┐
│  {                                                          │
│    "status": "healthy",                                     │
│    "platform": "lazada",                                    │
│    "timestamp": 1234567890                                  │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘

✅ Scraper is working!
```

#### 4.2 Test Backend API

```
🌐 Browser: https://price-tracker-lazada-uuyz.vercel.app/health

┌─────────────────────────────────────────────────────────────┐
│  {                                                          │
│    "status": "healthy",                                     │
│    "app_name": "E-commerce Price Tracker",                  │
│    "version": "1.0.0"                                       │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘

✅ Backend is working!
```

#### 4.3 Test Frontend

```
🌐 Browser: https://price-tracker-lazada.vercel.app

┌─────────────────────────────────────────────────────────────┐
│  E-commerce Price Tracker                                   │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                                                       │ │
│  │  Welcome Back!                                        │ │
│  │                                                       │ │
│  │  [🔐 Sign in with Google]                            │ │
│  │                                                       │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

✅ Frontend is working!
```

#### 4.4 Test Search

```
1. Click "Sign in with Google"
2. Complete Google login
3. You're now on the dashboard

┌─────────────────────────────────────────────────────────────┐
│  Dashboard                                                  │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  🔍 Search products...                                │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  Type: "laptop"                                             │
│  ⏱️  Searching... (6-10 seconds)                            │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  💻 Laptop ASUS VivoBook                              │ │
│  │  ₱ 25,999                                             │ │
│  │  [Track Price]                                        │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  💻 Lenovo IdeaPad                                    │ │
│  │  ₱ 22,500                                             │ │
│  │  [Track Price]                                        │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

✅ Search is working!
```

---

## 🎉 Success!

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              🎊 DEPLOYMENT SUCCESSFUL! 🎊                   │
│                                                             │
│  Your app is now live at:                                  │
│  🌐 https://price-tracker-lazada.vercel.app                │
│                                                             │
│  All systems operational:                                  │
│  ✅ Frontend (Vercel)                                       │
│  ✅ Backend (Vercel)                                        │
│  ✅ Scraper (Render)                                        │
│  ✅ Database (Supabase)                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting Visual Guide

### Problem: Search returns no results

```
┌─────────────────────────────────────────────────────────────┐
│  Diagnosis Steps:                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣  Check Scraper                                          │
│     🌐 Visit: https://your-scraper.onrender.com/health     │
│     ✅ Working? → Go to step 2                              │
│     ❌ Not working? → Check Render logs                     │
│                                                             │
│  2️⃣  Check Backend                                          │
│     🌐 Visit: https://your-backend.vercel.app/health       │
│     ✅ Working? → Go to step 3                              │
│     ❌ Not working? → Check Vercel logs                     │
│                                                             │
│  3️⃣  Check Environment Variable                             │
│     Vercel → Settings → Environment Variables              │
│     ✅ LAZADA_API_URL is set? → Go to step 4               │
│     ❌ Not set? → Add it and redeploy                       │
│                                                             │
│  4️⃣  Check Render Service                                   │
│     ⏱️  First search after 15 min? → Wait 30-60 seconds    │
│     🔄 Try again                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Deployment Status Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│  Component Status                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🌐 Frontend (Vercel)                                       │
│     Status: ⚪ Not deployed yet                             │
│     URL: https://price-tracker-lazada.vercel.app           │
│                                                             │
│  ⚙️  Backend (Vercel)                                       │
│     Status: ⚪ Not deployed yet                             │
│     URL: https://price-tracker-lazada-uuyz.vercel.app      │
│                                                             │
│  🤖 Scraper (Render)                                        │
│     Status: ⚪ Not deployed yet                             │
│     URL: https://______________.onrender.com                │
│                                                             │
│  💾 Database (Supabase)                                     │
│     Status: ✅ Already set up                               │
│     URL: db.jnruinihotolqgmcwyhs.supabase.co               │
│                                                             │
└─────────────────────────────────────────────────────────────┘

After deployment, all should show: ✅
```

---

## 🎯 Quick Reference

| What | Where | Time |
|------|-------|------|
| Deploy Scraper | https://dashboard.render.com | 10 min |
| Add Env Var | Vercel → Backend → Settings | 2 min |
| Redeploy | Vercel → Backend → Deployments | 2 min |
| Test | Browser | 5 min |

---

## 📞 Need Help?

```
┌─────────────────────────────────────────────────────────────┐
│  Documentation Files:                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📄 QUICK_START.md           - 4-step quick guide           │
│  📄 DEPLOYMENT_GUIDE.md      - Detailed instructions        │
│  📄 DEPLOYMENT_CHECKLIST.md  - Interactive checklist        │
│  📄 ARCHITECTURE.md          - System architecture          │
│  📄 VISUAL_GUIDE.md          - This file                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**Ready to deploy? Start with DEPLOYMENT_CHECKLIST.md!** ✅
