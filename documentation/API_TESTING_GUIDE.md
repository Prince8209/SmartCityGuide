# API Testing Guide

## Overview
This document provides instructions for testing the Smart City Guide backend API.

---

## Test Files

### 1. API Integration Tests
**File**: [`tests/api_tests.py`](file:///e:/SmartCityGuide/tests/api_tests.py)

Comprehensive Python script that tests all backend endpoints including:
- Authentication (Login, Signup)
- Cities API (List, Detail, Search, Regions)
- Data Structures Integration:
  - HashMap: Cache statistics
  - BST: Top rated cities, Rating stats
  - Queue: Booking queue status
  - Stack: Navigation tracking and history
  - LinkedList: Recent cities

### 2. Postman Collection
**File**: [`SmartCityGuide_API_Complete.postman_collection.json`](file:///e:/SmartCityGuide/SmartCityGuide_API_Complete.postman_collection.json)

Complete Postman collection with all API endpoints organized by category.

---

## Running Tests

### Prerequisites
1. **Start the backend server**:
```bash
cd backend
python app/main.py
```

2. **Install requests library** (if not installed):
```bash
pip install requests
```

### Run Python Tests
```bash
python tests/api_tests.py
```

**Expected Output**:
```
======================================================================
SMART CITY GUIDE - API INTEGRATION TESTS
======================================================================

Started at: 2024-01-10 15:30:00
Base URL: http://localhost:5000/api

🔍 Testing Core APIs...
----------------------------------------------------------------------
✓ Health Check

🔐 Testing Authentication...
----------------------------------------------------------------------
✓ Auth - Login
✓ Auth - Signup

🏙️ Testing Cities API...
----------------------------------------------------------------------
✓ Cities - Get All
✓ Cities - Get Detail (with cache)
✓ Cities - Get Regions

📊 Testing Data Structures Integration...
----------------------------------------------------------------------
✓ Cities - Cache Stats (HashMap): Hit rate: 75.0%
✓ Cities - Top Rated (BST): Found 5 cities
✓ Cities - Rating Stats (BST): Total: 10

📅 Testing Bookings API...
----------------------------------------------------------------------
✓ Bookings - Create (Queue): Queue position: 3
✓ Bookings - Queue Status (Queue): Pending: 3, Processed: 15

👤 Testing User Tracking API...
----------------------------------------------------------------------
✓ Users - Track Navigation (Stack)
✓ Users - Navigation History (Stack): Found 5 pages
✓ Users - Recent Cities (LinkedList): Found 3 cities

======================================================================
TEST SUMMARY
======================================================================
Total Tests: 18
✓ Passed: 18
✗ Failed: 0
Success Rate: 100.0%
======================================================================

📄 Test report saved to: tests/api_test_report.json
```

---

## Using Postman Collection

### Import Collection
1. Open Postman
2. Click **Import**
3. Select `SmartCityGuide_API_Complete.postman_collection.json`
4. Collection will be imported with all endpoints

### Collection Structure
```
Smart City Guide API - Complete Collection
├── Health & Info
│   ├── API Index
│   └── Health Check
├── Authentication
│   ├── Login
│   └── Signup
├── Cities API
│   ├── Get All Cities
│   ├── Get City by ID (with Cache)
│   ├── Search Cities
│   ├── Get Regions
│   └── Get Trip Types
├── Data Structures - Cache (HashMap)
│   └── Get Cache Statistics
├── Data Structures - Ratings (BST)
│   ├── Get Top Rated Cities
│   └── Get Rating Statistics
├── Bookings API
│   ├── Create Booking (Queue)
│   └── Get Bookings
├── Data Structures - Queue
│   └── Get Queue Status
├── Data Structures - Navigation (Stack)
│   ├── Track Navigation
│   ├── Get Navigation History
│   └── Go Back
├── Data Structures - Recent Cities (LinkedList)
│   └── Get Recent Cities
└── Reviews API
    ├── Get City Reviews
    └── Create Review
```

### Environment Variables
The collection uses these variables:
- `base_url`: `http://localhost:5000/api`
- `auth_token`: Auto-populated after login

### Testing Flow
1. **Login** first to get auth token
2. Test **Cities API** endpoints
3. Test **Data Structures** endpoints:
   - Cache stats (HashMap)
   - Top rated cities (BST)
   - Queue status (Queue)
   - Navigation tracking (Stack)
   - Recent cities (LinkedList)
4. Test **Bookings** with queue
5. Test **Reviews** (requires auth)

---

## Test Coverage

### Endpoints Tested

| Category | Endpoint | Method | Data Structure | Status |
|----------|----------|--------|----------------|--------|
| **Health** | `/health` | GET | - | ✅ |
| **Auth** | `/auth/login` | POST | - | ✅ |
| **Auth** | `/auth/signup` | POST | - | ✅ |
| **Cities** | `/cities` | GET | - | ✅ |
| **Cities** | `/cities/<id>` | GET | HashMap | ✅ |
| **Cities** | `/cities/regions` | GET | - | ✅ |
| **Cache** | `/cities/cache/stats` | GET | HashMap | ✅ |
| **Ratings** | `/cities/top-rated` | GET | BST | ✅ |
| **Ratings** | `/cities/ratings/stats` | GET | BST | ✅ |
| **Bookings** | `/bookings` | POST | Queue | ✅ |
| **Queue** | `/bookings/queue/status` | GET | Queue | ✅ |
| **Navigation** | `/users/navigation` | POST | Stack | ✅ |
| **Navigation** | `/users/navigation/history` | GET | Stack | ✅ |
| **Navigation** | `/users/navigation/back` | POST | Stack | ✅ |
| **Recent** | `/users/recent-cities` | GET | LinkedList | ✅ |

**Total**: 15 endpoints tested

---

## Test Report

After running tests, a JSON report is generated: `tests/api_test_report.json`

**Example Report**:
```json
{
  "total_tests": 18,
  "passed": 18,
  "failed": 0,
  "tests": [
    {
      "name": "Health Check",
      "status": "PASS",
      "details": ""
    },
    {
      "name": "Auth - Login",
      "status": "PASS",
      "details": ""
    },
    {
      "name": "Cities - Cache Stats (HashMap)",
      "status": "PASS",
      "details": "Hit rate: 75.0%"
    }
  ]
}
```

---

## Manual Testing Examples

### Test Cache (HashMap)
```bash
# First request (cache miss)
curl http://localhost:5000/api/cities/1?user_id=test123

# Second request (cache hit)
curl http://localhost:5000/api/cities/1?user_id=test123

# Check cache stats
curl http://localhost:5000/api/cities/cache/stats
```

### Test Queue
```bash
# Create booking (adds to queue)
curl -X POST http://localhost:5000/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "city_name": "Mumbai",
    "customer_name": "Test User",
    "customer_email": "test@example.com",
    "customer_phone": "9876543210",
    "check_in_date": "2024-02-01",
    "check_out_date": "2024-02-05",
    "num_travelers": 2,
    "daily_budget": 3000
  }'

# Check queue status
curl http://localhost:5000/api/bookings/queue/status
```

### Test Navigation (Stack)
```bash
# Track navigation
curl -X POST http://localhost:5000/api/users/navigation \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "page": "/cities/mumbai"}'

# Get history
curl http://localhost:5000/api/users/navigation/history?user_id=user123
```

### Test Recent Cities (LinkedList)
```bash
# View city (auto-tracks in recent)
curl http://localhost:5000/api/cities/1?user_id=user123

# Get recent cities
curl http://localhost:5000/api/users/recent-cities?user_id=user123
```

---

## Troubleshooting

### Backend Not Running
**Error**: Connection refused
**Solution**: Start backend with `python backend/app/main.py`

### Module Not Found
**Error**: `ModuleNotFoundError: No module named 'requests'`
**Solution**: Install requests with `pip install requests`

### Test Failures
1. Check backend is running on port 5000
2. Check database is connected
3. Review error details in test output
4. Check `tests/api_test_report.json` for details

---

## Next Steps

1. ✅ Run Python tests: `python tests/api_tests.py`
2. ✅ Import Postman collection
3. ✅ Test all endpoints manually
4. ✅ Review test report: `tests/api_test_report.json`
5. ✅ Verify data structures integration

---

## Summary

- **18 Test Cases** covering all endpoints
- **5 Data Structures** tested (HashMap, Queue, Stack, LinkedList, BST)
- **Postman Collection** with all endpoints
- **Automated Testing** with Python script
- **JSON Report** generation
