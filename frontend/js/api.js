/**
 * API Client
 * Handles all HTTP requests to backend
 */
class APIClient {
    constructor() {
        this.baseURL = API_CONFIG.BASE_URL;
    }

    getToken() {
        return localStorage.getItem('token');
    }

    setToken(token) {
        localStorage.setItem('token', token);
    }

    removeToken() {
        localStorage.removeItem('token');
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const token = this.getToken();

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
            console.log('Attaching token:', token.substring(0, 10) + '...');
        } else {
            console.warn('No token found in localStorage');
        }

        try {
            const response = await fetch(url, { ...options, headers });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Cities
    async getCities(filters = {}) {
        const params = new URLSearchParams(filters).toString();
        const endpoint = params ? `${API_CONFIG.ENDPOINTS.CITIES}?${params}` : API_CONFIG.ENDPOINTS.CITIES;
        return await this.request(endpoint);
    }

    async getCityById(id) {
        return await this.request(API_CONFIG.ENDPOINTS.CITY_BY_ID(id));
    }

    async createCity(cityData) {
        return await this.request(API_CONFIG.ENDPOINTS.CITIES, {
            method: 'POST',
            body: JSON.stringify(cityData)
        });
    }

    async getRegions() {
        return await this.request(API_CONFIG.ENDPOINTS.REGIONS);
    }

    async getTripTypes() {
        return await this.request(API_CONFIG.ENDPOINTS.TRIP_TYPES);
    }

    async getAttractionCategories() {
        return await this.request(API_CONFIG.ENDPOINTS.ATTRACTION_CATEGORIES);
    }

    // Auth
    async login(credentials) {
        const response = await this.request(API_CONFIG.ENDPOINTS.LOGIN, {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
        if (response.success && response.token) {
            this.setToken(response.token);
            localStorage.setItem('user', JSON.stringify(response.user));
        }
        return response;
    }

    async signup(userData) {
        const response = await this.request(API_CONFIG.ENDPOINTS.SIGNUP, {
            method: 'POST',
            body: JSON.stringify(userData)
        });
        if (response.success && response.token) {
            this.setToken(response.token);
            localStorage.setItem('user', JSON.stringify(response.user));
        }
        return response;
    }

    logout() {
        this.removeToken();
        localStorage.removeItem('user');
    }

    // Bookings
    async createBooking(bookingData) {
        return await this.request(API_CONFIG.ENDPOINTS.BOOKINGS, {
            method: 'POST',
            body: JSON.stringify(bookingData)
        });
    }

    async getBookings() {
        return await this.request(API_CONFIG.ENDPOINTS.BOOKINGS);
    }

    // Reviews
    async getReviews(cityId) {
        return await this.request(`${API_CONFIG.ENDPOINTS.REVIEWS}/${cityId}`);
    }

    async addReview(reviewData) {
        return await this.request(API_CONFIG.ENDPOINTS.REVIEWS, {
            method: 'POST',
            body: JSON.stringify(reviewData)
        });
    }

    // Upload
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        const url = `${this.baseURL}${API_CONFIG.ENDPOINTS.UPLOAD}`;
        const token = this.getToken(); // Add token if needed, though upload endpoint didn't have @token_required

        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: headers, // Content-Type is auto-set by fetch when body is FormData
                body: formData
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Upload failed');
            }
            return data;
        } catch (error) {
            console.error('Upload Error:', error);
            throw error;
        }
    }
}

// Create global instance
const api = new APIClient();
