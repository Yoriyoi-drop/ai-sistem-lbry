# ✅ AUTH FLOW TESTING - QUICK CHECKLIST

## 🚀 Quick Start

### Option 1: Automatic (Recommended)
```bash
./TEST_AUTH.sh
```

### Option 2: Manual
```bash
cd apps/dashboard
npm install
npm run dev
```

Then open: **http://localhost:5173**

---

## 📋 Testing Checklist

### ✅ Registration Flow
- [ ] Navigate to `/register` page
- [ ] Fill form with valid data
- [ ] Click "Sign Up"
- [ ] Verify redirect to `/dashboard`
- [ ] Check user info in header

### ✅ Login Flow
- [ ] Navigate to `/login` page
- [ ] Enter valid credentials
- [ ] Click "Sign In"
- [ ] Verify redirect to `/dashboard`
- [ ] Check token in localStorage

### ✅ Logout Flow
- [ ] Click "Logout" button
- [ ] Verify redirect to `/login`
- [ ] Check token removed from localStorage

### ✅ Protected Routes
- [ ] Try accessing `/dashboard` while logged OUT
- [ ] Verify redirect to `/login`
- [ ] Login, then access `/dashboard`
- [ ] Verify dashboard loads

### ✅ Forgot Password
- [ ] Click "Forgot password?" link
- [ ] Enter email address
- [ ] Click "Send Reset Link"
- [ ] Verify success message

---

## 🔍 Quick Debug Commands

### Check Auth Status
```javascript
// Open browser console (F12)
localStorage.getItem('access_token')  // Should show token if logged in
localStorage.getItem('user')          // Should show user data
```

### Clear Auth Data
```javascript
localStorage.clear()  // Logout and clear all data
location.reload()     // Refresh page
```

### Check Network
- Open DevTools → Network → XHR
- Look for `/api/v1/auth/*` requests
- Status 200/201 = Success
- Status 401 = Unauthorized
- Status 500 = Server Error

---

## ⚡ Expected Results

### After Registration
✅ User created  
✅ Logged in automatically  
✅ Dashboard visible  
✅ User info in header  

### After Login
✅ Token stored  
✅ Redirected to dashboard  
✅ Protected routes accessible  

### After Logout
✅ Token cleared  
✅ Redirected to login  
✅ Protected routes blocked  

---

## 🐛 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| `npm: command not found` | Install Node.js |
| `Cannot GET /` | Run `npm run dev` |
| `Network Error` | Backend not running (need FastAPI) |
| `401 Unauthorized` | Clear localStorage and login again |
| Port 5173 in use | Kill process: `lsof -ti:5173 \| xargs kill` |

---

## 📊 Test Data

Use these credentials for testing:

```
Email: test@example.com
Password: SecurePassword123!
Username: testuser
Full Name: Test User
```

---

## ✅ Success Criteria

Auth flow is working if ALL these pass:
- ✅ Can register new account
- ✅ Can login with credentials  
- ✅ Can logout successfully
- ✅ Dashboard loads after login
- ✅ Protected routes work
- ✅ User info displays in header
- ✅ No console errors

---

## 📝 Notes

- Frontend runs on: **http://localhost:5173**
- API (if running): **http://localhost:8000**
- Hot reload enabled (auto-refresh on code changes)

---

**Ready to test!** 🎉

Run: `./TEST_AUTH.sh` or `cd apps/dashboard && npm run dev`
