# Quick Login Guide for Temu/Shopee

## Why Manual Login Once?

Google and other platforms have strong bot detection that blocks automated logins. The solution: **log in manually once**, save cookies, then the scraper works automatically forever.

## Steps (Takes 2 minutes):

### 1. Run the login script:
```bash
cd rapidapi_version
/usr/bin/python3 simple_login_temu.py
```

### 2. In the browser that opens:
- Click "Sign in" or "Register"
- Click "Continue with Google"
- Log in with your Google account
- After logging in, search for "phone" to test
- Go back to terminal and press ENTER

### 3. Done! Cookies saved forever

The scraper will now work automatically without any login needed.

## For Shopee (same process):
```bash
/usr/bin/python3 simple_login_shopee.py
```

## Testing:
```bash
/usr/bin/python3 test_temu_with_saved_cookies.py
```

## Troubleshooting:

**Q: Cookies expired?**
A: Just run the login script again (once every few weeks)

**Q: Can't automate Google login?**
A: Correct - Google blocks bots. Manual login once is the industry standard.

**Q: Is this secure?**
A: Yes - cookies are saved locally, never shared. Same as staying logged in on your browser.
