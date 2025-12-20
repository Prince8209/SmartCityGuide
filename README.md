# 🏙️ Smart City Guide

A comprehensive travel guide platform designed to help users explore, plan, and book trips to incredible Indian cities. This full-stack application features a dynamic itinerary planner, user authentication, and a robust booking system.

<div align="center">
  <img src="frontend/assets/images/cities/delhi.jpg" alt="Smart City Guide" width="100%" style="border-radius: 10px; height: 300px; object-fit: cover;">
</div>

---

## 🌟 Key Features

- **Explore Destinations**: Browsable catalog of **60+ Indian cities** with filters for Region, Trip Type, and Budget.
- **Smart Itinerary Planner**: Generate personalized day-by-day travel plans based on your interests (Adventure, Heritage, Relaxed).
- **Budget Tracker**: Track trip expenses and get personalized budget recommendations based on travel style.
- **User Profile**: Manage your account details, bio, and travel preferences.
- **Secure Authentication**: User Signup and Login system powered by JSON Web Tokens (JWT).
- **Booking System**: Complete flow for booking trips, calculating costs, and managing reservations.
- **Admin Dashboard**: Dedicated panel for managing cities, users, and bookings.
- **Reviews & Ratings**: Share experiences and read reviews from other travelers.

---

## 🏗️ Technology Stack

### Backend
- **Framework**: Python Flask 3.0
- **Database**: MySQL 8.0 with SQLAlchemy ORM
- **Authentication**: PyJWT (JSON Web Tokens)
- **API**: RESTful architecture

### Frontend
- **Design**: Custom CSS (Responsive & Modern)
- **Logic**: Vanilla JavaScript (ES6+)
- **Icons**: Font Awesome 6
- **Architecture**: Modular component-based JS files

---

## 📚 Documentation

Detailed documentation for developers is available in the [`documentation/`](documentation/) directory:

*   **[📂 Project Structure](documentation/PROJECT_STRUCTURE.md)**: Overview of the folder layout.
*   **[⚙️ Backend Guide](documentation/BACKEND_FILES.md)**: Detailed breakdown of Models and API Routes.
*   **[🎨 Frontend Guide](documentation/FRONTEND_FILES.md)**: Explanation of JavaScript logic and Pages.
*   **[🔄 Workflows](documentation/WORKFLOWS.md)**: Step-by-step Technical Workflows (Signup, Booking, etc.).
*   **[📦 External Libraries](documentation/EXTERNAL_LIBRARIES.md)**: List of dependencies and their purpose.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server

### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure .env file (see .env.example)

# Run the server
python -m app.main
```
Server will start at `http://localhost:5000`

### 2. Frontend Setup
Simply serve the `frontend` folder using any static file server, or open `frontend/index.html` directly in your browser.

---

## 🔗 Key API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/cities` | List all cities (supports filters) |
| `POST` | `/api/auth/login` | Authenticate user |
| `POST` | `/api/bookings` | Create a new trip booking |
| `GET` | `/api/reviews/{id}` | Get reviews for a city |

---

## 📝 License

This project is licensed under the MIT License.

---
<div align="center">
  <sub>Built with ❤️ by Prince</sub>
</div>
