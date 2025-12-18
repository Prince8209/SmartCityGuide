# Frontend Files Reference

This document details every file in the `frontend` directory.

## Networking & Logic (`frontend/js/`)

| File | Type | Description |
| :--- | :--- | :--- |
| **`api.js`** | **Core Service** | **The Network Layer**. A centralized `APIClient` class handling all `fetch` requests. Manages JWT tokens automatically. |
| **`auth.js`** | **Controller** | **Auth Logic**. Handles Login/Signup forms, validation, and password strength checking. |
| **`cities.js`** | **Controller** | **Cities Page**. Fetches cities, renders cards, handles Search/Filter inputs (Debounced search, Region/TripType dropdowns). |
| **`itinerary.js`**| **Controller** | **Itinerary Page**. The "AI" Planner. Generates a day-by-day plan based on selected City + Days + Style. Randomizes attractions. |
| **`booking.js`** | **Controller** | **Booking Modal**. Handles the booking form inside the modal, date calculations, and submission to API. |
| **`reviews.js`** | **Controller** | **Reviews Modal**. Fetches and displays reviews. Handles submitting a new review. |
| **`admin.js`** | **Controller** | **Admin Dashboard**. Protected (checks `is_admin` flag). Loads stats, lists cities (CRUD), bookings, and users. |
| **`home.js`** | **Controller** | **Homepage**. Dynamic content for the landing page (e.g., featured cities). |
| **`script.js`** | **Utility** | **Global UI**. Navbar toggling, global event listeners, and common UI utilities. |
| **`config.js`** | **Config** | API Base URL configuration. |

## HTML Pages (`frontend/` & `frontend/pages/`)

| File | Location | Description |
| :--- | :--- | :--- |
| **`index.html`** | Root | **Landing Page**. Hero section, features overview, call to action. |
| **`cities.html`** | `pages/` | **Explore**. Grid of city cards with a sidebar for filters (Search, Region, Trip Type, Budget). |
| **`itinerary.html`**| `pages/` | **Planner**. Interface to select preferences and generate a custom trip timeline. |
| **`login.html`** | `pages/` | Login form. |
| **`signup.html`** | `pages/` | Registration form. |
| **`admin.html`** | `pages/` | **Dashboard**. Table views for managing Cities, Bookings, and Users. |
| **`contact.html`** | `pages/` | Contact form and info. |
| **`features.html`** | `pages/` | Static page listing site features. |
