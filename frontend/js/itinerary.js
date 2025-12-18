/**
 * Itinerary Page Logic
 * Handles dynamic itinerary generation based on user preferences
 */

// Debug helper
function logDebug(msg) {
    console.log(msg);
    let debugDiv = document.getElementById('debug-log');
    if (!debugDiv) {
        debugDiv = document.createElement('div');
        debugDiv.id = 'debug-log';
        debugDiv.style.position = 'fixed';
        debugDiv.style.bottom = '0';
        debugDiv.style.right = '0';
        debugDiv.style.background = 'rgba(0,0,0,0.8)';
        debugDiv.style.color = 'lime';
        debugDiv.style.padding = '10px';
        debugDiv.style.zIndex = '9999';
        debugDiv.style.maxHeight = '200px';
        debugDiv.style.overflow = 'auto';
        document.body.appendChild(debugDiv);
    }
    debugDiv.innerHTML += `<div>${msg}</div>`;
}

document.addEventListener('DOMContentLoaded', async () => {
    logDebug('DOM Loaded');
    await loadFormOptions();
    setupEventListeners();
});

// Load dropdown options
async function loadFormOptions() {
    try {
        logDebug('Loading options...');
        const selects = document.querySelectorAll('select');

        // Load Cities (First Select)
        const citiesResponse = await api.getCities({ limit: 1000 });
        const citySelect = selects[0];

        if (citiesResponse.success && citySelect) {
            citySelect.innerHTML = citiesResponse.cities
                .sort((a, b) => a.name.localeCompare(b.name))
                .map(city => `<option value="${city.id}">${city.name}</option>`)
                .join('');
            logDebug(`Loaded ${citiesResponse.cities.length} cities`);
        }

        // Load Trip Categories (Second Select)
        const categoriesResponse = await api.getAttractionCategories();
        const categorySelect = selects[1];

        if (categoriesResponse.success && categorySelect) {
            categorySelect.innerHTML = '<option value="">All Categories</option>' +
                categoriesResponse.categories
                    .map(category => `<option value="${category}">${category}</option>`)
                    .join('');
            logDebug(`Loaded ${categoriesResponse.categories.length} categories`);
        }

    } catch (error) {
        console.error('Error loading options:', error);
        logDebug('Error loading options: ' + error.message);
    }
}

// Setup Event Listeners
function setupEventListeners() {
    const generateBtn = document.querySelector('.btn-city');
    if (generateBtn) {
        generateBtn.onclick = generateItinerary;
        logDebug('Event listener attached to Generate button');
    } else {
        logDebug('Generate button not found!');
    }
}

// Generate Itinerary
async function generateItinerary() {
    logDebug('Generate button clicked');
    const selects = document.querySelectorAll('select');
    const citySelect = selects[0];
    const durationInput = document.querySelector('input[type="number"]');
    const categorySelect = selects[1];
    const styleSelect = selects[2];

    // Target the second column (Timeline) inside the grid
    const container = document.querySelector('.section .container > div > div:last-child');

    if (!citySelect || !durationInput || !categorySelect || !styleSelect || !container) {
        logDebug('Missing elements');
        return;
    }

    const cityId = citySelect.value;
    const duration = parseInt(durationInput.value);
    const category = categorySelect.value;
    const style = styleSelect.value;

    logDebug(`Generating for City: ${cityId}, Duration: ${duration}, Category: ${category}, Style: ${style}`);

    // Show loading
    const generateBtn = document.querySelector('.btn-city');
    const originalBtnText = generateBtn.innerHTML;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    generateBtn.disabled = true;

    try {
        // Fetch city details with attractions
        const response = await api.getCityById(cityId);

        if (!response.success) throw new Error('Failed to fetch city details');

        const city = response.city;
        const attractions = city.attractions || [];
        logDebug(`Fetched city: ${city.name}, Attractions: ${attractions.length}`);

        // Filter attractions by category if selected
        const filteredAttractions = category
            ? attractions.filter(a => a.category === category)
            : attractions;

        logDebug(`Filtered attractions: ${filteredAttractions.length}`);

        // Generate itinerary
        const itinerary = planItinerary(filteredAttractions, duration, style);
        logDebug(`Generated plan with ${itinerary.length} days`);

        // Render Itinerary
        renderItinerary(container, itinerary, city.name);
        logDebug('Rendered itinerary');

    } catch (error) {
        console.error('Error generating itinerary:', error);
        logDebug('Error: ' + error.message);
        alert('Failed to generate itinerary. Please try again.');
    } finally {
        generateBtn.innerHTML = originalBtnText;
        generateBtn.disabled = false;
    }
}

// Helper to shuffle array
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Simple planning algorithm
function planItinerary(attractions, days, style) {
    const plan = [];
    const itemsPerDay = style === 'Relaxed' ? 2 : (style === 'Adventure-packed' ? 4 : 3);

    // Shuffle attractions for variety
    const availableAttractions = shuffleArray([...attractions]);

    for (let i = 0; i < days; i++) {
        const dayAttractions = [];
        for (let j = 0; j < itemsPerDay; j++) {
            if (availableAttractions.length > 0) {
                dayAttractions.push(availableAttractions.shift());
            }
        }

        // If no attractions left, maybe add a "Free Time" or "Local Exploration" placeholder
        if (dayAttractions.length === 0) {
            dayAttractions.push({
                name: 'Local Exploration',
                description: 'Explore the local markets and streets at your own pace.',
                opening_hours: 'Flexible',
                category: 'Leisure'
            });
        }

        plan.push({
            day: i + 1,
            title: getDayTitle(i, days),
            items: dayAttractions
        });
    }
    return plan;
}

function getDayTitle(dayIndex, totalDays) {
    if (dayIndex === 0) return 'Arrival & First Impressions';
    if (dayIndex === totalDays - 1) return 'Departure & Last Minute Shopping';
    return 'City Exploration';
}

// Render the itinerary HTML
function renderItinerary(container, plan, cityName) {
    const timelineHTML = `
        <h3 style="margin-bottom: 1.5rem; color: #2d3748;"><i class="fas fa-calendar-alt"></i> Your Itinerary for ${cityName}</h3>
        ${plan.map(day => `
            <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 1.5rem; animation: fadeIn 0.5s ease-out;">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div style="width: 50px; height: 50px; background: linear-gradient(135deg, ${getDayColor(day.day)} 0%, ${getDayColor(day.day, true)} 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; margin-right: 1rem;">
                        DAY ${day.day}
                    </div>
                    <div>
                        <h4 style="margin-bottom: 0.25rem; color: #2d3748;">${day.title}</h4>
                        <p style="color: #718096; font-size: 0.9rem;">${day.items.length} Activities</p>
                    </div>
                </div>

                <div style="border-left: 3px solid #e2e8f0; padding-left: 1.5rem; margin-left: 1.5rem;">
                    ${day.items.map((item, index) => `
                        <div style="margin-bottom: 1.5rem;">
                            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                <i class="fas ${getCategoryIcon(item.category)}" style="color: ${getDayColor(day.day)}; margin-right: 0.5rem;"></i>
                                <strong style="color: #2d3748;">${getTimeSlot(index)} - ${item.name}</strong>
                            </div>
                            <p style="color: #718096; font-size: 0.95rem; margin-left: 1.8rem;">${item.description || 'Experience the beauty of this location.'}</p>
                            ${item.entry_fee ? `<p style="color: #718096; font-size: 0.85rem; margin-left: 1.8rem; margin-top: 0.2rem;"><i class="fas fa-ticket-alt"></i> Entry: ₹${item.entry_fee}</p>` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('')}
        
        <div style="text-align: center; margin-top: 2rem;">
            <button onclick="window.print()" style="padding: 1rem 2rem; background: white; border: 2px dashed #667eea; color: #667eea; border-radius: 12px; font-weight: 600; cursor: pointer; font-size: 1rem;">
                <i class="fas fa-print"></i> Print Itinerary
            </button>
        </div>
    `;

    container.innerHTML = timelineHTML;
}

function getDayColor(day, isGradientEnd = false) {
    const colors = [
        ['#667eea', '#764ba2'], // Blue/Purple
        ['#4facfe', '#00f2fe'], // Light Blue
        ['#f093fb', '#f5576c'], // Pink/Red
        ['#43e97b', '#38f9d7'], // Green
        ['#fa709a', '#fee140'], // Orange/Yellow
    ];
    const index = (day - 1) % colors.length;
    return colors[index][isGradientEnd ? 1 : 0];
}

function getCategoryIcon(category) {
    const map = {
        'Heritage': 'fa-landmark',
        'Nature': 'fa-tree',
        'Religious': 'fa-praying-hands',
        'Adventure': 'fa-hiking',
        'Food': 'fa-utensils',
        'Shopping': 'fa-shopping-bag',
        'Beach': 'fa-umbrella-beach',
        'Leisure': 'fa-coffee'
    };
    return map[category] || 'fa-map-marker-alt';
}

function getTimeSlot(index) {
    const slots = ['9:00 AM', '11:30 AM', '2:00 PM', '4:30 PM', '7:00 PM'];
    return slots[index] || 'Flexible';
}
