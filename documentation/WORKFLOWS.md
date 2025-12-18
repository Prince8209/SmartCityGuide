# Project Workflows

This document explains how different files interact to complete common user tasks.

## 1. User Sign Up Flow
1. **User** fills form on `signup.html`.
2. **`js/auth.js`** validates input fields (password match, length).
3. **`js/auth.js`** calls `api.signup(data)`.
4. **`js/api.js`** sends a **POST** request to `/api/auth/signup`.
5. **`backend/app/api/auth.py`** receives request:
   - checks if email exists in `User` table.
   - creates new `User` instance.
   - commits to database.
   - generates JWT token.
6. **`backend`** returns JSON with Token.
7. **`js/auth.js`** saves token to `localStorage` and redirects to `login.html`.

## 2. Booking a Trip Flow
1. **User** clicks "Book" on a card in `cities.html`.
2. **`js/cities.js`** triggers the modal opening (logic shared/imported).
3. **User** enters check-in/out dates and number of travelers.
4. **`js/booking.js`** calculates total cost logic live in the UI.
5. **User** confirms booking. `js/booking.js` calls `api.createBooking()`.
6. **`js/api.js`** sends **POST** request to `/api/bookings` with the auth token header.
7. **`backend/app/api/bookings.py`**:
   - validates dates and calculation.
   - creates `Booking` record in database.
8. **Success** message shown to user.

## 3. Admin Adding a City Flow
1. **Admin** logs in and navigates to `admin.html`.
2. **`js/admin.js`** verifies user `is_admin` from local storage (and API will verify token).
3. **Admin** clicks "Add City", fills details, and selects an image file.
4. **`js/admin.js`** 2-step process:
   - **Step A**: Call `api.uploadFile(file)`. `backend/app/api/upload.py` saves file and returns filename.
   - **Step B**: Call `api.createCity(data)` including the new filename.
5. **`backend/app/api/cities.py`**:
   - saves `City` record.
   - saves associated `Attraction` records if any.
6. **`js/admin.js`** refreshes the table to show the new city.
