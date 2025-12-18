/**
 * Homepage Database Integration
 * Loads featured cities from MySQL database
 */

// Load featured cities from database
async function loadFeaturedCities() {
    try {
        console.log('🔄 Attempting to load cities from database...');

        // Get cities from database (limit to 3 for featured section)
        const response = await api.getCities({ budget_max: 2500 });

        console.log('📡 API Response:', response);

        if (response.success && response.cities.length > 0) {
            const cities = response.cities.slice(0, 3);

            // Find the featured cities container - it's the first grid in the section
            const sections = document.querySelectorAll('.section');
            let container = null;

            // The featured cities section is the first section after hero
            for (let section of sections) {
                const sectionHeader = section.querySelector('.section-header');
                if (sectionHeader && sectionHeader.textContent.includes('Featured Destinations')) {
                    container = section.querySelector('div[style*="grid"]');
                    break;
                }
            }

            if (container) {
                console.log('✅ Found container, replacing with database cities');
                container.innerHTML = cities.map(city => `
                    <div class="city-card">
                        <div class="city-image" style="background-image: url('${city.image_url || 'assets/images/cities/default.jpg'}')">
                            <div class="city-badge">${city.badge || city.category}</div>
                        </div>
                        <div class="city-content">
                            <h3 class="city-name">${city.name}</h3>
                            <p class="city-desc">${city.description ? city.description.substring(0, 100) + '...' : ''}</p>
                            <div class="city-info">
                                <span class="city-stat"><i class="fas fa-clock"></i> ${city.recommended_days}</span>
                                <span class="city-stat"><i class="fas fa-rupee-sign"></i> ₹${city.avg_budget_per_day}/day</span>
                                <span class="city-stat"><i class="fas fa-sun"></i> ${city.best_season || 'Year-round'}</span>
                            </div>
                            <button class="btn-city" onclick="window.location.href='pages/cities.html#${city.name.toLowerCase()}'">
                                <i class="fas fa-map-marked-alt"></i> Explore ${city.name}
                            </button>
                        </div>
                    </div>
                `).join('');

                console.log(`✓ Successfully loaded ${cities.length} featured cities from database`);
            } else {
                console.warn('⚠️ Container not found');
            }
        } else {
            console.warn('⚠️ No cities returned from API');
        }
    } catch (error) {
        console.error('❌ Error loading featured cities:', error);
        console.log('💡 Make sure backend server is running on http://localhost:5000');
        console.log('💡 Using hardcoded cities as fallback');
    }
}

// Update stats with real database count
async function updateStats() {
    try {
        const response = await api.getCities();
        if (response.success) {
            const cityCountElement = document.querySelector('.stat-number[data-target="50"]');
            if (cityCountElement) {
                cityCountElement.setAttribute('data-target', response.count);
                cityCountElement.textContent = response.count;
            }
        }
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Search cities function
function searchCities() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput && searchInput.value.trim()) {
        window.location.href = `pages/cities.html?search=${encodeURIComponent(searchInput.value.trim())}`;
    } else {
        window.location.href = 'pages/cities.html';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadFeaturedCities();
    updateStats();

    // Add enter key support for search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchCities();
            }
        });
    }
});
