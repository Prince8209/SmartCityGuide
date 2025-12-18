/**
 * Global Script
 * Handles shared functionality like navigation, auth state, etc.
 */

document.addEventListener('DOMContentLoaded', () => {
    checkLoginState();
    setupMobileMenu();
});

// Check if user is logged in and update UI
function checkLoginState() {
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');

    console.log('Checking login state...');
    console.log('Token exists:', !!token);
    console.log('User data exists:', !!userStr);

    if (token && userStr) {
        try {
            const user = JSON.parse(userStr);
            console.log('Parsed user:', user);
            updateNavForLoggedInUser(user);
        } catch (e) {
            console.error('Error parsing user data:', e);
            logout();
        }
    }
}

// Update Navigation for Logged In User
function updateNavForLoggedInUser(user) {
    const navButtons = document.querySelector('.nav-buttons');
    if (navButtons) {
        const isInPages = window.location.pathname.includes('/pages/');
        const adminPath = isInPages ? 'admin.html' : 'pages/admin.html';

        let adminButtonHtml = '';
        if (user.is_admin) {
            adminButtonHtml = `
                <a href="${adminPath}" style="background: #4a5568; color: white; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem; transition: background 0.3s ease;" onmouseover="this.style.background='#2d3748'" onmouseout="this.style.background='#4a5568'">
                    <i class="fas fa-user-shield"></i> Admin
                </a>
             `;
        }

        navButtons.innerHTML = `
            <div class="user-menu" style="display: flex; align-items: center; gap: 1rem;">
                ${adminButtonHtml}
                <span style="color: #2d3748; font-weight: 600; display: flex; align-items: center;">
                    <i class="fas fa-user-circle" style="margin-right: 0.5rem; color: #667eea; font-size: 1.2rem;"></i>
                    ${user.username || user.full_name || 'User'}
                </span>
                <button onclick="logout()" class="btn-login" style="background: #e53e3e; color: white; border: none; padding: 0.5rem 1rem; border-radius: 8px; cursor: pointer;">
                    <i class="fas fa-sign-out-alt"></i>
                </button>
            </div>
        `;
    }
}

// Logout Function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = window.location.pathname.includes('pages') ? '../index.html' : 'index.html';
}

// Mobile Menu Toggle
function setupMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = menuToggle.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
}
