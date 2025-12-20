/**
 * Admin Dashboard Logic
 * Handles admin functionality and UI updates
 */

const AdminPanel = {
    currentAttractions: [],

    init() {
        this.checkAdminAuth();
        this.loadStats();
        this.loadCities();
        this.loadBookings();
        this.loadUsers();
        this.setupEventListeners();
    },

    // Check if user is admin
    checkAdminAuth() {
        const userStr = localStorage.getItem('user');
        if (!userStr) {
            window.location.href = 'login.html';
            return;
        }

        try {
            const user = JSON.parse(userStr);
            if (!user.is_admin) {
                alert('Access Denied: Admin privileges required.');
                window.location.href = '../index.html';
            }
        } catch (e) {
            console.error('Auth check error:', e);
            window.location.href = 'login.html';
        }
    },

    // Load Dashboard Statistics (Mock)
    async loadStats() {
        const statsContainer = document.getElementById('statsContainer');
        if (!statsContainer) return;

        try {
            const response = await api.getStats();
            if (response.success && response.stats) {
                const s = response.stats;
                const stats = [
                    { title: 'Total Cities', value: s.cities, icon: 'fa-city', color: '#667eea' },
                    { title: 'Total Users', value: s.users, icon: 'fa-users', color: '#48bb78' },
                    { title: 'Active Bookings', value: s.bookings, icon: 'fa-ticket-alt', color: '#ed8936' },
                    { title: 'Total Reviews', value: s.reviews, icon: 'fa-star', color: '#ecc94b' }
                ];

                statsContainer.innerHTML = stats.map(stat => `
                    <div class="stat-card">
                        <i class="fas ${stat.icon}" style="color: ${stat.color}"></i>
                        <div class="stat-content">
                            <h3>${stat.value}</h3>
                            <p>${stat.title}</p>
                        </div>
                    </div>
                `).join('');
            }
        } catch (error) {
            console.error('Error loading stats:', error);
            statsContainer.innerHTML = '<p class="error">Failed to load statistics</p>';
        }
    },

    // Fetch and Display Cities
    async loadCities() {
        const citiesTable = document.getElementById('citiesTable');
        if (!citiesTable) return;

        try {
            // Fetch all cities (limit 1000 to ensure we get everything for admin)
            const response = await api.getCities({ limit: 1000 });

            if (response.success && response.cities) {
                const cities = response.cities;

                if (cities.length === 0) {
                    citiesTable.innerHTML = '<p class="loading">No cities found.</p>';
                    return;
                }

                let html = `
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th>Image</th>
                                <th>Name</th>
                                <th>State</th>
                                <th>Region</th>
                                <th>Budget</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                html += cities.map(city => {
                    // Path resolution logic
                    const imagePath = city.image_url && city.image_url.startsWith('http')
                        ? city.image_url
                        : (city.image_url ? `../assets/images/cities/${city.image_url}` : '../assets/images/cities/default.jpg');

                    return `
                    <tr>
                        <td>
                            <img src="${imagePath}" alt="${city.name}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;">
                        </td>
                        <td>
                            <div style="font-weight: 600;">${city.name}</div>
                            <small style="color: #718096;">${city.category || 'General'}</small>
                        </td>
                        <td>${city.state}</td>
                        <td>${city.region || '-'}</td>
                        <td>₹${city.avg_budget_per_day}/day</td>
                        <td>
                            <button class="btn-edit" onclick="AdminPanel.editCity(${city.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn-delete" onclick="AdminPanel.deleteCity(${city.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                `;
                }).join('');

                html += '</tbody></table>';
                citiesTable.innerHTML = html;
            } else {
                throw new Error('Failed to fetch cities');
            }
        } catch (error) {
            console.error('Error loading cities:', error);
            citiesTable.innerHTML = `
                <div class="loading" style="color: #e53e3e;">
                    <i class="fas fa-exclamation-circle"></i> Error loading cities.
                    <br>
                    <button onclick="AdminPanel.loadCities()" style="margin-top: 1rem; padding: 0.5rem 1rem; cursor: pointer;">Retry</button>
                </div>
            `;
        }
    },

    // Fetch and Display Bookings
    async loadBookings() {
        const bookingsContainer = document.getElementById('bookingsTable');
        if (!bookingsContainer) return;

        try {
            const response = await api.getBookings();

            if (response.success && response.bookings) {
                const bookings = response.bookings;

                if (bookings.length === 0) {
                    bookingsContainer.innerHTML = '<p class="loading">No bookings found.</p>';
                    return;
                }

                let html = `
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th>Reference</th>
                                <th>Customer</th>
                                <th>City</th>
                                <th>Dates</th>
                                <th>Travelers</th>
                                <th>Cost</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                html += bookings.map(booking => {
                    const checkIn = new Date(booking.check_in_date).toLocaleDateString();
                    const checkOut = new Date(booking.check_out_date).toLocaleDateString();

                    return `
                    <tr>
                        <td>
                            <span style="font-family: monospace; font-weight: 600; color: #667eea;">${booking.booking_reference}</span>
                            <br>
                            <small style="color: #a0aec0;">${new Date(booking.created_at).toLocaleDateString()}</small>
                        </td>
                        <td>
                            <div style="font-weight: 600;">${booking.customer_name}</div>
                            <small style="color: #718096;">${booking.customer_email}</small><br>
                            <small style="color: #718096;">${booking.customer_phone}</small>
                        </td>
                        <td>${booking.city_name}</td>
                        <td>
                            <div>${checkIn}</div>
                            <div style="color: #718096; font-size: 0.8em;">to</div>
                            <div>${checkOut}</div>
                        </td>
                        <td style="text-align: center;">${booking.num_travelers}</td>
                        <td style="font-weight: 600;">₹${booking.total_cost}</td>
                        <td>
                            <span style="background: #ebf8ff; color: #4299e1; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 600;">
                                Confirmed
                            </span>
                        </td>
                    </tr>
                `;
                }).join('');

                html += '</tbody></table>';
                bookingsContainer.innerHTML = html;
            } else {
                throw new Error('Failed to fetch bookings');
            }
        } catch (error) {
            console.error('Error loading bookings:', error);
            bookingsContainer.innerHTML = `
                <div class="loading" style="color: #e53e3e;">
                    <i class="fas fa-exclamation-circle"></i> Error loading bookings.
                    <br>
                    <button onclick="AdminPanel.loadBookings()" style="margin-top: 1rem; padding: 0.5rem 1rem; cursor: pointer;">Retry</button>
                </div>
            `;
        }
    },

    // Load Users
    async loadUsers() {
        const usersTable = document.getElementById('usersTable');
        if (!usersTable) return;

        try {
            const response = await api.getUsers();
            if (response.success && response.users) {
                const users = response.users;

                let html = `
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th>User</th>
                                <th>Role</th>
                                <th>Joined</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                html += users.map(user => `
                    <tr>
                        <td>
                            <div style="font-weight: 600;">${user.full_name || user.username}</div>
                            <small style="color: #718096;">${user.email}</small>
                        </td>
                        <td>
                            <span style="background: ${user.is_admin ? '#ebf8ff' : '#f7fafc'}; color: ${user.is_admin ? '#4299e1' : '#718096'}; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 600;">
                                ${user.is_admin ? 'Admin' : 'User'}
                            </span>
                        </td>
                        <td>
                            ${new Date(user.created_at).toLocaleDateString()}
                        </td>
                        <td>
                            <button class="btn-edit" title="Edit User" disabled style="opacity: 0.5; cursor: not-allowed;"><i class="fas fa-edit"></i></button>
                        </td>
                    </tr>
                `).join('');

                html += '</tbody></table>';
                usersTable.innerHTML = html;
            }
        } catch (error) {
            console.error('Error loading users:', error);
            usersTable.innerHTML = '<p class="error">Failed to load users</p>';
        }
    },

    // Modal Functions
    showAddCityForm() {
        const modal = document.getElementById('cityFormModal');
        const form = document.getElementById('cityForm');
        const title = document.getElementById('cityFormTitle');

        if (modal && form && title) {
            form.reset();
            this.currentAttractions = [];
            this.renderAttractions();
            title.textContent = 'Add New City';
            modal.style.display = 'flex';
        }
    },

    addAttraction() {
        const nameInput = document.getElementById('attrName');
        const categoryInput = document.getElementById('attrCategory');
        const descInput = document.getElementById('attrDesc');

        const name = nameInput.value;
        const category = categoryInput.value;
        const desc = descInput.value;

        if (!name || !category) {
            alert('Please enter at least an Attraction Name and Category.');
            return;
        }

        this.currentAttractions.push({
            name,
            category,
            description: desc
        });

        // Clear inputs
        nameInput.value = '';
        categoryInput.value = '';
        descInput.value = '';

        this.renderAttractions();
    },

    renderAttractions() {
        const listContainer = document.getElementById('attractionsList');
        if (!listContainer) return;

        if (this.currentAttractions.length === 0) {
            listContainer.innerHTML = '<p style="color: #a0aec0; text-align: center; font-style: italic;">No attractions added yet.</p>';
            return;
        }

        listContainer.innerHTML = this.currentAttractions.map((attr, index) => `
            <div style="background: white; padding: 0.8rem; border: 1px solid #e2e8f0; border-radius: 4px; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 600;">${attr.name}</div>
                    <small style="color: #718096;">${attr.category}</small>
                </div>
                <button onclick="AdminPanel.removeAttraction(${index})" style="background: none; border: none; color: #e53e3e; cursor: pointer;">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `).join('');
    },

    removeAttraction(index) {
        this.currentAttractions.splice(index, 1);
        this.renderAttractions();
    },

    closeModal() {
        const modal = document.getElementById('cityFormModal');
        if (modal) {
            modal.style.display = 'none';
        }
    },

    async editCity(id) {
        try {
            const response = await api.getCityById(id);
            if (response.success && response.city) {
                const city = response.city;

                // Show modal
                this.showAddCityForm();
                document.getElementById('cityFormTitle').textContent = 'Edit City';

                // Populate fields
                document.getElementById('cityName').value = city.name;
                document.getElementById('cityState').value = city.state;
                document.getElementById('cityDescription').value = city.description;
                document.getElementById('cityRegion').value = city.region || '';
                document.getElementById('cityBudget').value = city.avg_budget_per_day;
                document.getElementById('cityCategory').value = city.category || '';

                // Populate attractions
                this.currentAttractions = city.attractions || [];
                this.renderAttractions();

                // Set editing flag
                document.getElementById('cityForm').dataset.editId = id;
            }
        } catch (error) {
            console.error('Error fetching city details:', error);
            alert('Failed to load city details');
        }
    },

    async deleteCity(id) {
        if (confirm('Are you sure you want to delete this city? This action cannot be undone.')) {
            try {
                const response = await api.deleteCity(id);
                if (response.success) {
                    alert('City deleted successfully');
                    this.loadCities();
                    this.loadStats(); // Update stats
                } else {
                    throw new Error(response.error || 'Failed to delete city');
                }
            } catch (error) {
                console.error('Error deleting city:', error);
                alert('Error: ' + error.message);
            }
        }
    },

    setupEventListeners() {
        // Modal close outside click
        const modal = document.getElementById('cityFormModal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        }

        // Form submit
        const form = document.getElementById('cityForm');
        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                const submitBtn = form.querySelector('button[type="submit"]');
                const originalBtnText = submitBtn.innerText;
                const uploadStatus = document.getElementById('uploadStatus');

                try {
                    submitBtn.disabled = true;
                    submitBtn.innerText = 'Processing...';

                    // 1. Collect Form Data
                    const name = document.getElementById('cityName').value;
                    const cityData = {
                        name: name,
                        state: document.getElementById('cityState').value,
                        description: document.getElementById('cityDescription').value,
                        region: document.getElementById('cityRegion').value,
                        avg_budget_per_day: document.getElementById('cityBudget').value,
                        category: document.getElementById('cityCategory').value,
                        category: document.getElementById('cityCategory').value,
                        trip_types: [document.getElementById('cityCategory').value], // Basic extraction
                        attractions: this.currentAttractions
                    };

                    // 2. Upload City Image if selected
                    const cityFileInput = document.getElementById('cityImageFile');
                    let cityImageUrl = 'placeholder.jpg';

                    if (cityFileInput.files.length > 0) {
                        try {
                            const uploadResp = await api.uploadFile(cityFileInput.files[0]);
                            if (uploadResp.success) {
                                cityImageUrl = uploadResp.filename;
                            }
                        } catch (e) {
                            console.error('City image upload failed:', e);
                            alert('Failed to upload city image. Using placeholder.');
                        }
                    }

                    cityData.image_url = cityImageUrl;

                    // 3. Send Data to API
                    // 3. Send Data to API
                    let response;
                    const editId = form.dataset.editId;

                    if (editId) {
                        response = await api.updateCity(editId, cityData);
                    } else {
                        response = await api.createCity(cityData);
                    }

                    if (response.success) {
                        alert(`City ${editId ? 'updated' : 'created'} successfully!`);
                        this.closeModal();
                        this.loadCities(); // Refresh list
                        this.loadStats(); // Update stats
                        delete form.dataset.editId; // Clear edit mode
                    } else {
                        throw new Error(response.message || 'Failed to save city');
                    }

                    // Upload
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error: ' + error.message);
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.innerText = originalBtnText;
                }
            });
        }
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    AdminPanel.init();
});
