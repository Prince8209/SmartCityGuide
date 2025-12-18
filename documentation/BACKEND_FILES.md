# Backend Files Reference

This document details every file in the `backend` directory.

## Core Application

| File | Path | Description |
| :--- | :--- | :--- |
| **`main.py`** | `backend/app/main.py` | **Entry Point**. Initializes Flask, configures database/CORS/secrets, registers API blueprints, and runs the server. |
| **`config.py`** | `backend/app/database/config.py` | Sets up `SQLAlchemy` instance. Defines `init_db(app)` to connect DB and create tables. |

## Data Models (`backend/app/models/`)
These classes map directly to database tables.

| Class | File | Table | Purpose |
| :--- | :--- | :--- | :--- |
| **`City`** | `city.py` | `cities` | **Core Content**. Stores city info (name, image, budget, description, region, trip_types). |
| **`User`** | `user.py` | `users` | Stores user credentials (email, hashed_password) and profile info. |
| **`Attraction`** | `attraction.py` | `attractions` | Tourist spots linked to a City. Contains entry fee, opening hours, coordinates. |
| **`Booking`** | `booking.py` | `bookings` | Records user trip bookings, dates, costs, and contact details. |
| **`Review`** | `review.py` | `reviews` | User reviews and ratings for cities. |
| **`Favorite`** | `favorite.py` | `favorites` | (Optional) Cities marked as favorite by users. |

## API Routes (`backend/app/api/`)
These files handle HTTP requests from the frontend.

| Module | URL Prefix | Description |
| :--- | :--- | :--- |
| **`auth.py`** | `/api/auth` | **Login/Signup**. Generates JWT tokens. Contains `@token_required` decorator for securing other routes. |
| **`cities.py`** | `/api/cities` | **Search & Listing**. GET cities with filters (search, region, budget). GET `trip-types`, `regions`. POST (Admin) to create cities. |
| **`bookings.py`**| `/api/bookings`| **Transactions**. POST to create a booking (calculates cost). GET to list bookings (Admin). |
| **`reviews.py`** | `/api/reviews` | **Social**. GET reviews for a city. POST to add a review (User only). |
| **`upload.py`** | `/api/upload` | **File Handling**. Handles image uploads (local storage or ImageKit integration). |
