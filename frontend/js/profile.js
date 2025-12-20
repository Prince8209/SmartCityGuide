/**
 * Profile Page Logic
 * Handles loading user data, bookings, and favorites
 */

document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadProfile();
    loadUserBookings();
    loadUserFavorites();
});

// Check Auth
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
    }
}

// Load Profile Info
function loadProfile() {
    const userStr = localStorage.getItem('user');
    if (userStr) {
        const user = JSON.parse(userStr);
        document.getElementById('userName').textContent = user.username || user.full_name || 'User';
        document.getElementById('userEmail').textContent = user.email || '';
    }
}

// Switch Tabs
window.switchTab = function (tabName) {
    // Buttons
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');

    // Content
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
};

// Load Bookings
async function loadUserBookings() {
    const container = document.getElementById('bookingsList');

    try {
        const response = await api.getBookings(); // Now returns user specific bookings

        if (response.success && response.bookings.length > 0) {
            container.innerHTML = response.bookings.map(booking => `
                <div class="booking-card">
                    <div>
                        <h3 style="margin-bottom: 0.5rem;">${booking.city_name}</h3>
                        <p style="color: #718096; font-size: 0.9rem;">
                            Ref: <strong>${booking.booking_reference}</strong>
                        </p>
                    </div>
                    <div>
                        <p><i class="fas fa-calendar"></i> ${new Date(booking.check_in_date).toLocaleDateString()} - ${new Date(booking.check_out_date).toLocaleDateString()}</p>
                        <p><i class="fas fa-users"></i> ${booking.num_travelers} Travelers</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="font-weight: 700; font-size: 1.2rem; color: #2d3748;">₹${booking.total_cost.toLocaleString()}</p>
                        <span class="booking-status">Confirmed</span>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = `
                <div style="text-align: center; padding: 3rem; color: #cbd5e0;">
                    <i class="fas fa-ticket-alt" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                    <p>No bookings found. Time to plan a trip!</p>
                    <button class="btn-city" onclick="window.location.href='cities.html'" style="margin-top: 1rem; width: auto; padding: 0.5rem 1.5rem;">Explore Cities</button>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading bookings:', error);
        container.innerHTML = '<p class="error">Failed to load bookings.</p>';
    }
}

// Load Favorites
async function loadUserFavorites() {
    const container = document.getElementById('favoritesList');

    try {
        // Get favorite IDs
        const favResponse = await api.getFavorites();
        if (!favResponse.success) throw new Error('Failed to fetch favorites');

        const favoriteIds = favResponse.favorites;

        if (favoriteIds.length === 0) {
            container.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: #cbd5e0;">
                    <i class="far fa-heart" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                    <p>No favorites yet. Save cities you love!</p>
                    <button class="btn-city" onclick="window.location.href='cities.html'" style="margin-top: 1rem; width: auto; padding: 0.5rem 1.5rem;">Browse Cities</button>
                </div>
            `;
            return;
        }

        // Fetch details for each favorite city
        // Note: Doing parallel requests or fetching all cities and filtering would be better
        // For now, let's fetch all cities and filter (more efficient than N requests)
        const cityResponse = await api.getCities({ limit: 1000 });

        if (cityResponse.success) {
            const favoriteCities = cityResponse.cities.filter(city => favoriteIds.includes(city.id));

            // Reuse renderCities from cities.js but targeting our container
            // Since renderCities relies on global 'elements.grid', we'll do manual rendering here 
            // to avoid conflict, but reusing the HTML structure

            container.innerHTML = favoriteCities.map(city => {
                const imagePath = city.image_url && city.image_url.startsWith('http')
                    ? city.image_url
                    : (city.image_url ? `../assets/images/cities/${city.image_url}` : '../assets/images/cities/default.jpg');

                return `
                <div class="city-card">
                    <div class="city-image" style="background-image: url('${imagePath}')">
                        <div class="city-badge">${city.badge || city.category}</div>
                        <button class="btn-favorite active" onclick="toggleFavorite(${city.id}, this)">
                            <i class="fas fa-heart" style="color: #e53e3e"></i>
                        </button>
                    </div>
                    <div class="city-content">
                        <h3 class="city-name">${city.name}</h3>
                        <p class="city-desc">${city.description ? city.description.substring(0, 80) + '...' : ''}</p>
                        <div class="city-actions">
                            <button class="btn-city" onclick="window.location.href='cities.html#${city.name.toLowerCase()}'">
                                <i class="fas fa-map-marked-alt"></i> View Details
                            </button>
                        </div>
                    </div>
                </div>
                `;
            }).join('');

        }

    } catch (error) {
        console.error('Error loading favorites:', error);
        container.innerHTML = `<div class="error-message" style="grid-column: 1/-1; text-align: center; color: #e53e3e; padding: 2rem;">
            <i class="fas fa-exclamation-triangle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
            <p>Failed to load favorites.</p>
            <p style="font-size: 0.9rem; margin-top: 0.5rem; background: #fff5f5; display: inline-block; padding: 0.5rem; border-radius: 4px;">Technical Details: ${error.message}</p>
        </div>`;
    }
}
