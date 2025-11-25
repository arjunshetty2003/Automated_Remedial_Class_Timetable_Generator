# Troubleshooting Guide

## Issue: "Failed to fetch" errors in browser

### ✅ Solution: CORS Fixed
The CORS (Cross-Origin Resource Sharing) issue has been resolved.

**What was done:**
1. Added CORS middleware to backend (`backend/app/main.py`)
2. Configured to allow requests from `http://localhost:3000`
3. Restarted backend server

**To verify it's working:**
```bash
# Check CORS headers
curl -I -X OPTIONS http://localhost:8000/students \
  -H "Origin: http://localhost:3000" | grep access-control
```

Expected output:
```
access-control-allow-credentials: true
access-control-allow-origin: http://localhost:3000
```

## Quick Fix Steps

### 1. Refresh Browser
Simply refresh your browser at http://localhost:3000

### 2. Clear Browser Cache
- Chrome/Edge: Ctrl+Shift+Delete (Cmd+Shift+Delete on Mac)
- Firefox: Ctrl+Shift+Delete
- Safari: Cmd+Option+E

### 3. Hard Reload
- Chrome/Firefox: Ctrl+Shift+R (Cmd+Shift+R on Mac)
- Safari: Cmd+Option+R

## Verify Services Are Running

### Check Backend
```bash
# Should show uvicorn process
ps aux | grep "uvicorn app.main" | grep -v grep

# Should return student data
curl http://localhost:8000/students
```

### Check Frontend
```bash
# Should show next dev process
ps aux | grep "next dev" | grep -v grep
```

## Restart Services (if needed)

### Restart Backend
```bash
# Stop backend
ps aux | grep "uvicorn app.main" | grep -v grep | awk '{print $2}' | xargs kill

# Start backend
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
```

### Restart Frontend
```bash
# Stop frontend
ps aux | grep "next dev" | grep -v grep | awk '{print $2}' | xargs kill

# Start frontend
cd frontend
npm run dev &
```

## Common Issues

### Issue: Port 8000 already in use
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Issue: Port 3000 already in use
```bash
# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Issue: Database connection error
Check that DATABASE_URL in `backend/.env` is correct:
```bash
cat backend/.env | grep DATABASE_URL
```

### Issue: Frontend shows blank page
Check browser console (F12) for errors and verify:
1. Backend is running on port 8000
2. No CORS errors
3. API calls are succeeding

## Current System Status

**Backend:** ✅ Running with CORS enabled  
**Frontend:** ✅ Running on port 3000  
**Database:** ✅ Connected (71 timetables, 8 students, 6 teachers)

## Test Endpoints

```bash
# Test students endpoint
curl http://localhost:8000/students | python3 -m json.tool

# Test teachers endpoint  
curl http://localhost:8000/teachers | python3 -m json.tool

# Test timetables endpoint
curl http://localhost:8000/timetables | python3 -m json.tool

# Test health endpoint
curl http://localhost:8000/health
```

## Browser Developer Console

Open browser console (F12) and check:
- **Console tab**: Should have no red errors
- **Network tab**: API calls should return 200 status
- **Application tab**: Check if cookies/storage is working

## Success Indicators

When everything is working, you should see:

### Dashboard Page
- 5 stat cards with numbers
- Quick action buttons
- System overview panel

### Students Page
- Table with 8 students
- "Add Student" button
- Subject marks visible

### Teachers Page
- Table with 6 teachers
- Subject badges (color-coded)
- "Add Teacher" button

### Marks Page
- 32 mark entries
- Color-coded performance
- Warning for failing students

### Timetables Page
- 71 regular timetable entries
- Filter buttons working
- Complete schedule details

## Still Having Issues?

1. Check this file: `SYSTEM_STATUS.md` for current status
2. Review `DEPLOYMENT_SUMMARY.md` for setup details
3. Check backend logs: `tail -f /tmp/backend.log`
4. Check frontend in browser console (F12)

## Contact Information

For more help, check:
- Backend docs: http://localhost:8000/docs
- Frontend guide: `frontend/README_FRONTEND.md`
- System overview: `SYSTEM_OVERVIEW.md`
