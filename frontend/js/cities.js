/**
 * Cities Page Script
 * Handles loading cities, filtering, and search
 */

// State
let currentFilters = {
    search: '',
    region: '',
    trip_type: '',
    budget_max: '',
    page: 1,
    limit: 6
};
let userFavorites = [];

// DOM Elements
const elements = {
    grid: document.getElementById('citiesGrid'),
    search: document.getElementById('searchInput'),
    region: document.getElementById('regionFilter'),
    tripType: document.getElementById('tripTypeFilter'),
    budget: document.getElementById('budgetFilter'),
    clearBtn: document.getElementById('clearFilters'),
    count: document.getElementById('resultsCount'),
    loadMoreBtn: document.getElementById('loadMoreBtn')
};

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize page
async function init() {
    try {
        // Load filter options
        await Promise.all([
            loadRegions(),
            loadTripTypes()
        ]);

        // Load favorites if user is logged in
        if (localStorage.getItem('token')) {
            await loadFavorites();
        }

        // Check URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('search')) {
            currentFilters.search = urlParams.get('search');
            if (elements.search) elements.search.value = currentFilters.search;
        }

        // Initial load
        await loadCities();

        // Event Listeners
        setupEventListeners();

    } catch (error) {
        console.error('Initialization error:', error);
        showError('Failed to initialize page. Please make sure the backend server is running.');
    }
}

// Load Favorites
async function loadFavorites() {
    try {
        const response = await api.getFavorites();
        if (response.success) {
            userFavorites = response.favorites; // Array of city IDs
        }
    } catch (error) {
        console.error('Error loading favorites:', error);
    }
}

// Toggle Favorite
window.toggleFavorite = async function (cityId, btn) {
    const icon = btn.querySelector('i');
    const isAdding = !btn.classList.contains('active');

    // Debug
    console.log(`Toggling favorite: ${isAdding ? 'Adding' : 'Removing'} city ${cityId}`);

    // Optimistic UI Update
    btn.classList.toggle('active');
    if (isAdding) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        icon.style.color = '#e53e3e';
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        icon.style.color = '#cbd5e0';
    }

    try {
        let response;
        if (isAdding) {
            response = await api.addFavorite(cityId);
        } else {
            response = await api.removeFavorite(cityId);
        }

        if (!response.success) {
            throw new Error(response.message || response.error || 'Request failed');
        }

        // Update local state
        if (isAdding) {
            userFavorites.push(cityId);
        } else {
            userFavorites = userFavorites.filter(id => id !== cityId);
        }

    } catch (error) {
        console.error('Favorite update failed:', error);
        alert(`Failed to save favorite: ${error.message}`);

        // Revert UI
        btn.classList.toggle('active');
        if (isAdding) {
            icon.classList.remove('fas');
            icon.classList.add('far');
            icon.style.color = '#cbd5e0';
        } else {
            icon.classList.remove('far');
            icon.classList.add('fas');
            icon.style.color = '#e53e3e';
        }
    }
};

// Load Regions for dropdown
async function loadRegions() {
    try {
        const response = await api.getRegions();
        if (response.success && elements.region) {
            response.regions.forEach(region => {
                if (region) {
                    const option = document.createElement('option');
                    option.value = region;
                    option.textContent = region;
                    elements.region.appendChild(option);
                }
            });
        }
    } catch (error) {
        console.error('Error loading regions:', error);
    }
}

// Load Trip Types for dropdown
async function loadTripTypes() {
    try {
        const response = await api.getTripTypes();
        if (response.success && elements.tripType) {
            response.trip_types.forEach(type => {
                if (type) {
                    const option = document.createElement('option');
                    option.value = type;
                    option.textContent = type;
                    elements.tripType.appendChild(option);
                }
            });
        }
    } catch (error) {
        console.error('Error loading trip types:', error);
    }
}

// Load Cities with current filters
async function loadCities(append = false) {
    if (!elements.grid) return;

    // Show loading state if initial load
    if (!append) {
        elements.grid.innerHTML = '<div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i> Loading amazing cities...</div>';
    }

    if (elements.loadMoreBtn) {
        elements.loadMoreBtn.classList.add('loading');
        elements.loadMoreBtn.disabled = true;
        elements.loadMoreBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    }

    if (elements.count) elements.count.textContent = 'Searching...';

    try {
        const response = await api.getCities(currentFilters);

        if (response.success) {
            if (append) {
                renderCities(response.cities, true);
            } else {
                renderCities(response.cities, false);
            }

            if (elements.count) {
                elements.count.textContent = `Found ${response.count} destination${response.count !== 1 ? 's' : ''}`;
            }

            // Handle Load More Button
            if (elements.loadMoreBtn) {
                if (response.has_next) {
                    elements.loadMoreBtn.style.display = 'inline-flex';
                    elements.loadMoreBtn.disabled = false;
                    elements.loadMoreBtn.classList.remove('loading');
                    elements.loadMoreBtn.innerHTML = 'Load More <i class="fas fa-chevron-down"></i>';
                } else {
                    elements.loadMoreBtn.style.display = 'none';
                }
            }

        } else {
            showError('Failed to load cities.');
        }
    } catch (error) {
        console.error('Error loading cities:', error);
        showError('Could not connect to server. Please ensure backend is running on http://localhost:5000');
    }
}

// Render city cards
function renderCities(cities, append = false) {
    if (!elements.grid) return;

    if (!append && cities.length === 0) {
        elements.grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 3rem;">
                <i class="fas fa-search" style="font-size: 3rem; color: #cbd5e0; margin-bottom: 1rem;"></i>
                <h3>No cities found</h3>
                <p style="color: #718096;">Try adjusting your filters or search terms</p>
            </div>
        `;
        if (elements.loadMoreBtn) elements.loadMoreBtn.style.display = 'none';
        return;
    }

    const html = cities.map(city => {
        const imagePath = city.image_url && city.image_url.startsWith('http')
            ? city.image_url
            : (city.image_url ? `../assets/images/cities/${city.image_url}` : '../assets/images/cities/default.jpg');

        const isFavorite = userFavorites.includes(city.id);
        const favClass = isFavorite ? 'active' : '';
        const favIconClass = isFavorite ? 'fas' : 'far';
        const favIconColor = isFavorite ? '#e53e3e' : '#cbd5e0';

        return `
        <div class="city-card" id="${city.name.toLowerCase()}">
            <div class="city-image" style="background-image: url('${imagePath}')">
                <div class="city-badge">${city.badge || city.category}</div>
                <button class="btn-favorite ${favClass}" onclick="toggleFavorite(${city.id}, this)">
                    <i class="${favIconClass} fa-heart" style="color: ${favIconColor}"></i>
                </button>
            </div>
            <div class="city-content">
                <h3 class="city-name">${city.name}</h3>
                <p class="city-desc">${city.description ? city.description.substring(0, 100) + '...' : ''}</p>
                <div class="city-info">
                    <span class="city-stat"><i class="fas fa-clock"></i> ${city.recommended_days}</span>
                    <span class="city-stat"><i class="fas fa-rupee-sign"></i> ₹${city.avg_budget_per_day}/day</span>
                    <span class="city-stat"><i class="fas fa-sun"></i> ${city.best_season || 'Year-round'}</span>
                </div>
                <div class="city-attractions">
                    ${renderAttractions(city.attractions)}
                </div>
                <div class="city-actions" style="display: flex; gap: 0.5rem;">
                    <button class="btn-city" onclick="window.location.href='city-detail.html?id=${city.id}'" style="flex: 1; background: #2d3748; border: none;">
                         <i class="fas fa-binoculars"></i> Explore
                    </button>
                    <button class="btn-city" onclick="openBookingModal('${city.name}', ${city.avg_budget_per_day})" style="flex: 1;">
                        <i class="fas fa-map-marked-alt"></i> Book
                    </button>
                    <button class="btn-city btn-reviews" onclick="openReviewsModal(${city.id}, '${city.name}')" style="flex: 1; background: #fff; color: var(--primary); border: 1px solid var(--primary);">
                        <i class="fas fa-star"></i> Reviews
                    </button>
                </div>
            </div>
        </div>
    `;
    }).join('');

    if (append) {
        elements.grid.insertAdjacentHTML('beforeend', html);
    } else {
        elements.grid.innerHTML = html;
    }
}

// Helper to render attractions tags
function renderAttractions(attractions) {
    if (!attractions || !Array.isArray(attractions)) return '';
    return attractions.slice(0, 4).map(attr =>
        `<span class="attraction-tag">${attr}</span>`
    ).join('');
}

// Show error message
function showError(message) {
    if (elements.grid) {
        elements.grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: #e53e3e;">
                <i class="fas fa-exclamation-circle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <p>${message}</p>
            </div>
        `;
    }
}

// Setup Event Listeners
function setupEventListeners() {
    // Search
    if (elements.search) {
        elements.search.addEventListener('input', debounce((e) => {
            currentFilters.search = e.target.value.trim();
            currentFilters.page = 1; // Reset to page 1
            loadCities();
        }, 500));
    }

    // Region Filter
    if (elements.region) {
        elements.region.addEventListener('change', (e) => {
            currentFilters.region = e.target.value;
            currentFilters.page = 1;
            loadCities();
        });
    }

    // Trip Type Filter
    if (elements.tripType) {
        elements.tripType.addEventListener('change', (e) => {
            currentFilters.trip_type = e.target.value;
            currentFilters.page = 1;
            loadCities();
        });
    }

    // Budget Filter
    if (elements.budget) {
        elements.budget.addEventListener('change', (e) => {
            currentFilters.budget_max = e.target.value;
            currentFilters.page = 1;
            loadCities();
        });
    }

    // Clear Filters
    if (elements.clearBtn) {
        elements.clearBtn.addEventListener('click', () => {
            currentFilters = {
                search: '',
                region: '',
                trip_type: '',
                budget_max: '',
                page: 1,
                limit: 6
            };

            // Reset UI
            if (elements.search) elements.search.value = '';
            if (elements.region) elements.region.value = '';
            if (elements.tripType) elements.tripType.value = '';
            if (elements.budget) elements.budget.value = '';

            loadCities();
        });
    }

    // Load More Button
    if (elements.loadMoreBtn) {
        elements.loadMoreBtn.addEventListener('click', () => {
            currentFilters.page++;
            loadCities(true); // Load more (append)
        });
    }
}

// Start when DOM is ready
document.addEventListener('DOMContentLoaded', init);
