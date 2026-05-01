# Google OAuth Setup Guide

## Overview
This guide will help you set up Google OAuth authentication for your Price Tracker application.

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: "Price Tracker" (or any name you prefer)
4. Click "Create"

## Step 2: Enable Google+ API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click on it and click "Enable"

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: Price Tracker
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue"
   - Scopes: Click "Save and Continue" (no additional scopes needed)
   - Test users: Add your email for testing
   - Click "Save and Continue"

4. Create OAuth Client ID:
   - Application type: **Web application**
   - Name: Price Tracker Web Client
   - Authorized JavaScript origins:
     - `http://localhost:3000`
     - `http://localhost:5173` (for Vite dev server)
   - Authorized redirect URIs:
     - `http://localhost:3000`
     - `http://localhost:5173`
   - Click "Create"

5. **Copy your Client ID** - it will look like:
   ```
   123456789-abcdefghijklmnop.apps.googleusercontent.com
   ```

## Step 4: Configure Frontend

1. Create a `.env` file in the `frontend/` directory:
   ```bash
   cd frontend
   cp .env.example .env
   ```

2. Edit `frontend/.env` and add your Google Client ID:
   ```env
   VITE_API_URL=http://localhost:8000
   VITE_GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
   ```

3. Replace `YOUR_CLIENT_ID_HERE` with the Client ID you copied

## Step 5: Restart the Application

1. Stop the frontend (Ctrl+C)
2. Restart it:
   ```bash
   cd frontend
   npm run dev
   ```

## Step 6: Test Google Sign-In

1. Go to http://localhost:3000
2. Click the "Sign in with Google" button
3. Select your Google account
4. You should be redirected to the dashboard

## Production Deployment

When deploying to production:

1. Add your production domain to Google Cloud Console:
   - Go to Credentials → Edit your OAuth client
   - Add Authorized JavaScript origins:
     - `https://yourdomain.com`
   - Add Authorized redirect URIs:
     - `https://yourdomain.com`

2. Update your production `.env` file with the same Client ID

3. Publish your OAuth consent screen:
   - Go to "OAuth consent screen"
   - Click "Publish App"
   - Submit for verification if needed

## Security Notes

- ⚠️ **Never commit your `.env` file to Git**
- ⚠️ The `.env` file is already in `.gitignore`
- ⚠️ Keep your Client ID secure (though it's not as sensitive as a secret)
- ⚠️ For production, consider adding a Client Secret for backend verification

## Troubleshooting

### "redirect_uri_mismatch" error
- Make sure your redirect URI in Google Console matches exactly
- Include the port number (e.g., `:3000`)
- Check for trailing slashes

### "idpiframe_initialization_failed" error
- Clear browser cookies
- Make sure third-party cookies are enabled
- Try in incognito mode

### Google button not showing
- Check browser console for errors
- Verify VITE_GOOGLE_CLIENT_ID is set correctly
- Restart the dev server after changing .env

## Support

For more information, see:
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [React OAuth Google Library](https://www.npmjs.com/package/@react-oauth/google)
