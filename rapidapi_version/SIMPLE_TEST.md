# 🎯 Simple 2-Step Test

## Step 1: Start API (Terminal)

```bash
cd rapidapi_version
pip3 install -r requirements.txt
python3 run_api.py
```

**Wait for this message:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The test dashboard will automatically open in your browser!

---

## Step 2: Test in Dashboard (Browser)

The dashboard will open automatically. If not, open `test_dashboard.html` manually.

### What to do:

1. **Check API Status** (top bar)
   - Should show "✅ Online" in green
   - If red, API isn't running

2. **Click "🔍 Test All Platforms"**
   - Uses default search "phone"
   - Tests all 3 platforms at once
   - Takes 20-40 seconds

3. **Check Results**
   - Products should appear below
   - Each with image, name, price
   - Platform badges (lazada/shopee/temu)

4. **Check Platform Cards**
   - All three should turn green
   - Show result counts and times

---

## ✅ Success = Ready to Deploy!

If you see:
- ✅ API Status: Online (green)
- ✅ Products displayed with images
- ✅ All platform cards green
- ✅ No errors in activity log

**You're ready to deploy to RapidAPI!** 🚀

---

## ❌ If Something Fails

### API Status shows "Offline"
```bash
# Make sure API is running
python3 run_api.py
```

### No products appear
- Try different search term
- Check activity log for errors
- Wait longer (first run is slow)

### Platform card shows "Failed"
- Check terminal for error messages
- That platform might be temporarily down
- Try again in a few minutes

---

## 🎨 Dashboard Features

- **Quick Test**: Test all platforms at once
- **Individual Tests**: Test each platform separately  
- **Live Results**: See products as they're found
- **Activity Log**: Real-time status updates
- **Statistics**: Track success/failure rates

---

## 💡 Pro Tip

Test with different queries to make sure everything works:
- "phone" - Electronics
- "laptop" - Computers
- "shoes" - Fashion
- "bag" - Accessories

If all queries work, your API is solid! ✅
