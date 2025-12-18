/**
 * API Configuration
 * Backend endpoint URLs
 */
const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:5000/api',
    ENDPOINTS: {
        // Cities
        CITIES: '/cities',
        CITY_BY_ID: (id) => `/cities/${id}`,
        REGIONS: '/cities/regions',
        TRIP_TYPES: '/cities/trip-types',
        ATTRACTION_CATEGORIES: '/cities/attraction-categories',

        // Auth
        LOGIN: '/auth/login',
        SIGNUP: '/auth/signup',

        // Bookings
        BOOKINGS: '/bookings',

        // Reviews
        REVIEWS: '/reviews',

        // Upload
        UPLOAD: '/upload/local'
    }
};
