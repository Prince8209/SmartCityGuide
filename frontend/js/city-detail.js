/**
 * City Detail Page Script
 */

async function initCityDetail() {
    const urlParams = new URLSearchParams(window.location.search);
    const cityId = urlParams.get('id');

    if (!cityId) {
        window.location.href = 'cities.html';
        return;
    }

    try {
        const response = await api.getCityById(cityId);

        if (response.success && response.city) {
            renderCityDetail(response.city);
            document.getElementById('loading').style.display = 'none';
            document.getElementById('cityContent').style.display = 'block';
        } else {
            showError('City not found');
        }

    } catch (error) {
        console.error('Error fetching city details:', error);
        showError('Failed to load city details');
    }
}

function renderCityDetail(city) {
    // Hero Section
    const hero = document.getElementById('cityHero');
    const imagePath = city.image_url && city.image_url.startsWith('http')
        ? city.image_url
        : (city.image_url ? `../assets/images/cities/${city.image_url}` : '../assets/images/cities/default.jpg');

    hero.style.backgroundImage = `url('${imagePath}')`;

    document.getElementById('cityName').textContent = city.name;
    document.getElementById('cityState').innerHTML = `<i class="fas fa-map-marker-alt"></i> ${city.state}`;
    document.getElementById('cityBadge').textContent = city.badge || city.category || 'Destination';

    // Info Cards
    document.getElementById('infoSeason').textContent = city.best_season || 'Year-round';
    document.getElementById('infoBudget').textContent = `₹${city.avg_budget_per_day}`;
    document.getElementById('infoDuration').textContent = city.recommended_days || '3 Days';
    document.getElementById('infoRating').textContent = city.rating ? `${city.rating}/5` : 'New';

    // Description
    document.getElementById('cityDescription').textContent = city.description;

    // Attractions
    const attractionsList = document.getElementById('attractionsList');
    if (city.attractions && city.attractions.length > 0) {
        const attractionsHtml = city.attractions.map(attr => `
            <div class="attraction-card">
                <img src="../assets/images/cities/default_attraction.jpg" alt="${attr}" class="attraction-img">
                <div class="attraction-content">
                    <span style="font-size: 0.8rem; color: #667eea; font-weight: 600; text-transform: uppercase;">Must Visit</span>
                    <h3 style="margin: 0.5rem 0; font-size: 1.25rem;">${attr}</h3>
                    <p style="color: #718096; line-height: 1.6;">A popular attraction in ${city.name} that attracts many tourists.</p>
                </div>
            </div>
        `).join('');
        attractionsList.innerHTML = attractionsHtml;
    } else {
        attractionsList.innerHTML = '<p style="color: #718096; font-style: italic;">No specific attractions listed yet.</p>';
    }

    // Booking Sidebar logic
    document.getElementById('bookCityName').textContent = city.name;
    document.getElementById('bookCost').textContent = `₹${city.avg_budget_per_day}`;

    document.getElementById('bookNowBtn').addEventListener('click', () => {
        // Re-use existing booking functionality or redirect
        // For now, simpler to alert or simple redirect since modal logic is complex
        // Ideally, we import openBookingModal from booking.js if available globally,
        // but booking.js is UI dependent. 
        alert('Booking feature coming to this page soon! Please go back to Cities page to book.');
        // TODO: Import booking modal logic here
    });
}

function showError(message) {
    document.getElementById('loading').innerHTML = `
        <div style="text-align: center; color: #e53e3e;">
            <i class="fas fa-exclamation-triangle" style="font-size: 3rem;"></i>
            <h2 style="margin-top: 1rem;">${message}</h2>
            <a href="cities.html" style="margin-top: 1rem; display: inline-block; color: #667eea; text-decoration: underline;">Return to Cities</a>
        </div>
    `;
}

// Initialize
document.addEventListener('DOMContentLoaded', initCityDetail);
