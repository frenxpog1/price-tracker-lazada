# Vercel Environment Variables Setup Guide

## Backend Project: price-tracker-lazada-uuyz

Copy and paste these environment variables into your **backend** Vercel project:

### Environment Variables (Key = Value)

```
DATABASE_URL=postgresql://postgres:1fRAjzOpSx7nteA7@db.jnruinihotolqgmcwyhs.supabase.co:5432/postgres
```

```
SECRET_KEY=your-super-secret-key-change-this-in-production
```

```
GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com
```

```
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET_HERE
```

```
DEBUG=False
```

```
CORS_ORIGINS=["https://price-tracker-lazada.vercel.app","http://localhost:3000","http://localhost:5173"]
```

```
LAZADA_API_URL=https://price-tracker-lazada.onrender.com
```

---

## Frontend Project: price-tracker-lazada

Copy and paste these environment variables into your **frontend** Vercel project:

### Environment Variables (Key = Value)

```
VITE_GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com
```

```
VITE_API_URL=https://price-tracker-lazada-uuyz.vercel.app
```

---

## How to Add Environment Variables in Vercel:

1. Go to https://vercel.com/dashboard
2. Select your project (backend or frontend)
3. Go to **Settings** → **Environment Variables**
4. For each variable above:
   - Click **Add New**
   - Enter the **Key** (e.g., `DATABASE_URL`)
   - Enter the **Value** (e.g., `postgresql://postgres:...`)
   - Select all environments: **Production**, **Preview**, **Development**
   - Click **Save**
5. After adding all variables, go to **Deployments** tab
6. Click **Redeploy** on the latest deployment

---

## Summary Table

### Backend Environment Variables (7 total)
| Key | Value |
|-----|-------|
| DATABASE_URL | postgresql://postgres:1fRAjzOpSx7nteA7@db.jnruinihotolqgmcwyhs.supabase.co:5432/postgres |
| SECRET_KEY | your-super-secret-key-change-this-in-production |
| GOOGLE_CLIENT_ID | YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com |
| GOOGLE_CLIENT_SECRET | YOUR_GOOGLE_CLIENT_SECRET_HERE |
| DEBUG | False |
| CORS_ORIGINS | ["https://price-tracker-lazada.vercel.app","http://localhost:3000","http://localhost:5173"] |
| LAZADA_API_URL | https://price-tracker-lazada.onrender.com |

### Frontend Environment Variables (2 total)
| Key | Value |
|-----|-------|
| VITE_GOOGLE_CLIENT_ID | YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com |
| VITE_API_URL | https://price-tracker-lazada-uuyz.vercel.app |

---

## Testing After Setup

1. **Backend Health Check**: Visit https://price-tracker-lazada-uuyz.vercel.app/health
   - Should return: `{"status":"healthy","app_name":"E-commerce Price Tracker","version":"1.0.0"}`

2. **Frontend**: Visit https://price-tracker-lazada.vercel.app
   - Should show your login page
   - Google OAuth button should work

3. **Test Google OAuth**: Click "Sign in with Google"
   - Should redirect to Google login
   - After login, should redirect back to your app

---

## Troubleshooting

If Google OAuth still shows "invalid_client" error:
1. Verify the `GOOGLE_CLIENT_ID` matches in both frontend and Google Cloud Console
2. Verify `https://price-tracker-lazada.vercel.app` is in the authorized origins in Google Cloud Console
3. Check that both projects have been redeployed after adding environment variables
