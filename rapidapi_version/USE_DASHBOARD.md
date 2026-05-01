# 🎯 How to Use the Test Dashboard

## Quick Start (2 Steps)

### Step 1: Start the API
```bash
cd rapidapi_version
pip3 install -r requirements.txt
python3 run_api.py
```

Wait until you see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Open the Dashboard
Open `test_dashboard.html` in your browser:
- **Mac**: `open test_dashboard.html`
- **Windows**: Double-click the file
- **Linux**: `xdg-open test_dashboard.html`

Or just drag the file into your browser.

---

## 🎨 Dashboard Features

### 1. **API Status Bar** (Top)
- Shows if API is online/offline
- Tracks total tests run
- Shows success/failure count
- Updates automatically every 5 seconds

### 2. **Quick Test All Platforms**
- Test all three platforms at once
- Enter search query (e.g., "phone", "laptop", "shoes")
- Choose number of results per platform
- Select sort order
- Click "Test All Platforms"

### 3. **Individual Platform Tests**
- Test Lazada, Shopee, or Temu separately
- See real-time status for each platform
- View response time and result count
- Color-coded status (green=success, red=error, orange=testing)

### 4. **Results Display**
- Shows all products found
- Displays product images, names, and prices
- Platform badges for each product
- Hover over products for full details

### 5. **Activity Log**
- Real-time log of all actions
- Color-coded messages (blue=info, green=success, red=error)
- Timestamps for each event
- Scrollable history

---

## ✅ What Success Looks Like

### When Everything Works:

1. **API Status**: Shows "✅ Online" in green
2. **Platform Cards**: All turn green after testing
3. **Results**: Products appear with images and prices
4. **Logs**: Show "✅ test completed" messages

### Example Success Log:
```
[10:30:15] Starting quick test: "phone"
[10:30:23] ✅ Quick test completed in 8.45s
[10:30:23] Found 3271 total results, returned 9 products
[10:30:23] Platforms searched: lazada, shopee, temu
```

---

## ❌ Troubleshooting

### "API Not Running" Warning
**Problem**: Orange warning at top of page
**Solution**: Start the API with `python3 run_api.py`

### "API returned 500" Error
**Problem**: API is running but scrapers are failing
**Solution**: Check the API terminal for error messages

### No Products Displayed
**Problem**: Test completes but no products shown
**Solution**: 
- Try a different search query
- Check if the platform website is accessible
- Look at the activity log for details

### Slow Response Times
**Problem**: Tests take 30+ seconds
**Solution**: This is normal! Scrapers need to:
- Launch Chrome browser
- Load the website
- Wait for JavaScript
- Extract data

**Expected times:**
- Lazada: 5-10 seconds
- Shopee: 10-15 seconds
- Temu: 10-15 seconds

---

## 🧪 Testing Checklist

Use this checklist before deploying:

- [ ] API status shows "✅ Online"
- [ ] Quick test returns products from all platforms
- [ ] Lazada individual test succeeds
- [ ] Shopee individual test succeeds
- [ ] Temu individual test succeeds
- [ ] All products have images
- [ ] All products have prices
- [ ] All products have names
- [ ] No error messages in logs
- [ ] Response times are reasonable (< 30s per platform)

---

## 💡 Pro Tips

1. **Test with different queries**: Try "phone", "laptop", "shoes", "bag"
2. **Test sorting**: Try all three sort options
3. **Test pagination**: Change results per platform (1-10)
4. **Watch the logs**: They show exactly what's happening
5. **Test multiple times**: Make sure results are consistent

---

## 🚀 Ready to Deploy?

If all tests pass in the dashboard:

✅ Your API is working perfectly!
✅ All three scrapers are functional!
✅ You're ready to deploy to RapidAPI!

**Next steps:**
1. Deploy to your hosting platform (Heroku, AWS, etc.)
2. Update API_BASE_URL in the dashboard to your deployed URL
3. Test again with the deployed URL
4. List on RapidAPI marketplace!

---

## 📸 Screenshot Guide

### What You Should See:

**Top Status Bar:**
```
API Status: ✅ Online
Tests Run: 4
Successful: 4
Failed: 0
```

**Platform Cards (After Testing):**
```
🛒 Lazada          [Success]
Status: 3 products found
Results: 3
Time: 8.45s
```

**Results Section:**
- Grid of product cards
- Each with image, name, price
- Platform badge (lazada/shopee/temu)

**Activity Log:**
- Green success messages
- Blue info messages
- No red error messages

---

## 🆘 Need Help?

If something doesn't work:

1. Check the activity log in the dashboard
2. Check the terminal where API is running
3. Make sure you ran `pip3 install -r requirements.txt`
4. Make sure API is running on port 8000
5. Try restarting the API

**Common fixes:**
```bash
# Restart API
Ctrl+C (stop current API)
python3 run_api.py

# Reinstall dependencies
pip3 install -r requirements.txt

# Check if port 8000 is in use
lsof -i :8000
```
