# 🧪 AUTH FLOW TESTING GUIDE

## Prerequisites

### 1. Backend Setup
```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Celery
cd apps/api
celery -A apps.api.src.tasks.celery_app worker -l info

# Terminal 3: Start FastAPI
cd apps/api
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
# Terminal 4: Start Vite Dev Server
cd apps/dashboard
npm install
npm run dev
```

---

## 🔐 Testing Auth Flow

### Step 1: Access Application
Open browser: `http://localhost:5173`

You should be redirected to `/login`

---

### Step 2: Test Registration

1. Click "Sign up" link
2. Fill registration form:
   ```
   Full Name: Test User
   Username: testuser
   Email: test@example.com
   Password: SecurePassword123!
   Confirm Password: SecurePassword123!
   ```
3. Click "Sign Up"
4. **Expected Result:**
   - ✅ User created successfully
   - ✅ Redirected to `/dashboard`
   - ✅ Token stored in localStorage
   - ✅ User info displayed in header

**Troubleshooting:**
- ❌ "Registration failed" → Check backend API is running
- ❌ "Passwords do not match" → Ensure passwords match
- ❌ "Password must be at least 8 characters" → Use stronger password

---

### Step 3: Test Logout

1. Click "Logout" button in header
2. **Expected Result:**
   - ✅ Redirected to `/login`
   - ✅ Token removed from localStorage
   - ✅ User logged out

---

### Step 4: Test Login

1. Fill login form:
   ```
   Email: test@example.com
   Password: SecurePassword123!
   ```
2. Click "Sign In"
3. **Expected Result:**
   - ✅ Login successful
   - ✅ Redirected to `/dashboard`
   - ✅ Dashboard shows stats
   - ✅ User info in header

**Troubleshooting:**
- ❌ "Login failed" → Check credentials
- ❌ "Invalid email or password" → Backend auth issue
- ❌ Network error → Check API is running

---

### Step 5: Test Protected Routes

1. While logged OUT, try to access: `http://localhost:5173/dashboard`
2. **Expected Result:**
   - ✅ Redirected to `/login`
   - ✅ Cannot access without auth

3. Login, then access: `http://localhost:5173/dashboard`
4. **Expected Result:**
   - ✅ Dashboard loads successfully
   - ✅ Stats cards visible
   - ✅ Sidebar navigation works

---

### Step 6: Test Forgot Password

1. On login page, click "Forgot password?"
2. Enter email: `test@example.com`
3. Click "Send Reset Link"
4. **Expected Result:**
   - ✅ Success message displayed
   - ✅ Email would be sent (check backend logs)
   - ✅ Can return to login

---

### Step 7: Test Token Refresh

1. Login successfully
2. Wait ~15 minutes (or manually expire token)
3. Make an API call (navigate between pages)
4. **Expected Result:**
   - ✅ Token auto-refreshed
   - ✅ No logout
   - ✅ Continues working

**Manual Test:**
```javascript
// Open browser console
localStorage.getItem('access_token') // Should show token
// Delete token
localStorage.removeItem('access_token')
// Refresh page - should redirect to login
```

---

## 🔍 Debugging

### Check Browser Console
```javascript
// Check if user is authenticated
localStorage.getItem('access_token')
localStorage.getItem('user')

// Clear all auth data
localStorage.clear()
```

### Check Network Tab
1. Open DevTools → Network
2. Filter: XHR/Fetch
3. Look for:
   - `/api/v1/auth/login` → Should return 200
   - `/api/v1/auth/register` → Should return 201
   - `/api/v1/auth/me` → Should return user data

### Common Issues

**Issue: "Network Error"**
- ✅ Check API is running on port 8000
- ✅ Check CORS is configured
- ✅ Check .env file has correct API_URL

**Issue: "401 Unauthorized"**
- ✅ Token expired - try logging in again
- ✅ Token invalid - clear localStorage
- ✅ Backend not configured properly

**Issue: "Cannot POST /api/v1/auth/login"**
- ✅ Backend routes not setup
- ✅ FastAPI not running
- ✅ Wrong API URL in .env

---

## ✅ Success Criteria

Auth flow is working if:

- ✅ Can register new user
- ✅ Can login with credentials
- ✅ Can logout successfully
- ✅ Protected routes require auth
- ✅ Dashboard loads after login
- ✅ User info shows in header
- ✅ Token stored in localStorage
- ✅ Token auto-refreshes
- ✅ Forgot password flow works
- ✅ Form validation works

---

## 📊 Mock Data for Testing

If backend is not ready, you can test with mock responses:

### Mock User
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "role": "admin",
  "is_active": true,
  "created_at": "2025-11-26T14:00:00Z"
}
```

### Mock Login Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "refresh_token_here",
  "token_type": "bearer",
  "user": { /* user object */ }
}
```

---

## 🚀 Next Steps After Testing

If auth flow works:
1. ✅ Test dashboard navigation
2. ✅ Test agents page
3. ✅ Test security page
4. ✅ Add more UI components
5. ✅ Write unit tests

---

**Last Updated:** 2025-11-26  
**Status:** Ready for Testing
