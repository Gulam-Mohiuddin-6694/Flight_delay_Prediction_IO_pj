# HOW TO SET API KEY PROPERLY - STEP BY STEP

## Current Status: API Key NOT Set
The diagnostic test shows your API key is not configured.

---

## OPTION 1: Set API Key in Windows (Temporary - for current session)

### Step 1: Open Command Prompt where you run the app

### Step 2: Set the API key
```cmd
set AVIATIONSTACK_API_KEY=your_actual_api_key_here
```

**IMPORTANT:** Replace `your_actual_api_key_here` with your real API key from aviationstack.com

### Step 3: Verify it's set
```cmd
echo %AVIATIONSTACK_API_KEY%
```
Should show your API key

### Step 4: Start the app in SAME command prompt
```cmd
python app.py
```

**NOTE:** This only works in the current command prompt session. If you close it, you need to set it again.

---

## OPTION 2: Set API Key Permanently in Windows

### Step 1: Open Command Prompt as Administrator

### Step 2: Set permanent environment variable
```cmd
setx AVIATIONSTACK_API_KEY "your_actual_api_key_here"
```

### Step 3: Close and reopen Command Prompt

### Step 4: Verify
```cmd
echo %AVIATIONSTACK_API_KEY%
```

### Step 5: Start app
```cmd
python app.py
```

---

## OPTION 3: Hardcode API Key (Quick Test - Not Recommended for Production)

### Edit the file: src/flight_lookup.py

Find this line (line 7):
```python
self.aviationstack_key = os.getenv('AVIATIONSTACK_API_KEY', 'demo_key')
```

Change to:
```python
self.aviationstack_key = 'your_actual_api_key_here'  # Replace with your key
```

Save and restart app.

---

## HOW TO GET API KEY

### Step 1: Go to AviationStack
https://aviationstack.com/

### Step 2: Click "Get Free API Key"

### Step 3: Sign up with email

### Step 4: Verify email

### Step 5: Go to Dashboard
https://aviationstack.com/dashboard

### Step 6: Copy your API Key
It looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

---

## TESTING AFTER SETUP

### Run diagnostic test:
```cmd
python test_api_connection.py
```

### Expected output if working:
```
API Key Found: a1b2c3d4e5...o5p6
Source: api
SUCCESS! Real-time flight data is working!
```

### Expected output if NOT working:
```
API Key NOT SET in environment
Source: demo
Demo mode is working fine for presentation!
```

---

## COMMON ISSUES

### Issue 1: "API Key NOT SET"
**Solution:** Make sure you set it in the SAME command prompt where you run the app

### Issue 2: "API returned status 401"
**Solution:** API key is invalid. Check if you copied it correctly

### Issue 3: "API returned status 403"  
**Solution:** Rate limit reached (100 requests/month on free tier)

### Issue 4: Still using demo data
**Solution:** 
1. Close app completely
2. Set API key
3. Verify with: `echo %AVIATIONSTACK_API_KEY%`
4. Restart app

---

## QUICK TEST COMMANDS

```cmd
# 1. Set API key (replace with your key)
set AVIATIONSTACK_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

# 2. Verify
echo %AVIATIONSTACK_API_KEY%

# 3. Test
python test_api_connection.py

# 4. If test passes, start app
python app.py
```

---

## FOR YOUR PROJECT SUBMISSION

### You have 2 options:

**Option A: Keep Demo Mode (Recommended)**
- Works perfectly for demonstration
- No API setup needed
- Shows 12 pre-configured flights
- Mention: "Supports real API integration"

**Option B: Enable Real API**
- Follow steps above
- Works with ANY flight worldwide
- Requires API key setup
- Free tier: 100 requests/month

---

## IMPORTANT NOTES

1. **Environment variables are session-specific**
   - If you set with `set`, it only works in that command prompt
   - Use `setx` for permanent setting

2. **Restart required**
   - After setting API key, restart the app
   - Close and reopen command prompt if using `setx`

3. **API key format**
   - Should be 32 characters
   - Only letters and numbers
   - No spaces or special characters

4. **Free tier limits**
   - 100 requests per month
   - Resets monthly
   - Enough for testing and demo

---

## VERIFICATION CHECKLIST

- [ ] Got API key from aviationstack.com
- [ ] Set environment variable with `set` or `setx`
- [ ] Verified with `echo %AVIATIONSTACK_API_KEY%`
- [ ] Ran `python test_api_connection.py`
- [ ] Saw "Source: api" in test results
- [ ] Restarted app with `python app.py`
- [ ] Tested with real flight number

---

**If you're still having issues, demo mode works perfectly for your project!** ✅
