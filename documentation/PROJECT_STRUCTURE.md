# Project Structure

This document outlines the file organization of the Smart City Guide project.

## Directory Tree

```
e:\SmartCityGuide
├── backend/            # Python Flask API & MySQL Database logic
│   ├── app/            # Application source code
│   │   ├── api/        # API route handlers
│   │   ├── models/     # Database ORM models
│   │   ├── database/   # Database connection config
│   │   └── main.py     # Application entry point
│   ├── .env            # Environment variables (secrets)
│   ├── requirements.txt# Python dependencies
│   └── ...
└── frontend/           # HTML/CSS/JS Client Application
    ├── js/             # Application logic (Authentication, API calls, Page scripts)
    ├── pages/          # HTML Templates for specific routes
    ├── css/            # Stylesheets
    ├── assets/         # Images, fonts, and media
    └── index.html      # Main entry point (Landing Page)
```

## Key Directories

- **`backend/app/api/`**: Contains the route handlers (controllers) that define the endpoints the frontend calls.
- **`backend/app/models/`**: Defines the data structure (Schema) matching the Database tables.
- **`frontend/js/`**: Contains all client-side logic. `api.js` is the core bridge to the backend.
- **`frontend/pages/`**: Contains the HTML files for the application's different views.
