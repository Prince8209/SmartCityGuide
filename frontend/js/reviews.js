/**
 * Reviews Logic
 * Handles loading, displaying, and submitting reviews
 */

// State
let currentReviewCityId = null;

// DOM Elements
const reviewsModal = document.getElementById('reviewsModal');
const reviewsList = document.getElementById('reviewsList');
const reviewForm = document.getElementById('reviewForm');
const reviewsTitle = document.getElementById('reviewsTitle');

// Open Reviews Modal
async function openReviewsModal(cityId, cityName) {
    currentReviewCityId = cityId;
    reviewsTitle.textContent = `Reviews for ${cityName}`;
    
    // Reset UI
    reviewsModal.style.display = 'flex';
    reviewsList.innerHTML = '<div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i> Loading reviews...</div>';
    if (reviewForm) reviewForm.reset();

    // Load reviews
    await loadReviews(cityId);
}

// Close Reviews Modal
function closeReviewsModal() {
    reviewsModal.style.display = 'none';
}

// Load Reviews
async function loadReviews(cityId) {
    try {
        const response = await api.getReviews(cityId);
        
        if (response.success) {
            renderReviews(response.reviews);
        } else {
            reviewsList.innerHTML = '<p class="no-reviews">Failed to load reviews.</p>';
        }
    } catch (error) {
        console.error('Error loading reviews:', error);
        reviewsList.innerHTML = '<p class="no-reviews">Could not connect to server.</p>';
    }
}

// Render Reviews
function renderReviews(reviews) {
    if (!reviews || reviews.length === 0) {
        reviewsList.innerHTML = `
            <div class="no-reviews">
                <i class="far fa-comment-dots"></i>
                <p>No reviews yet. Be the first to write one!</p>
            </div>
        `;
        return;
    }

    reviewsList.innerHTML = reviews.map(review => `
        <div class="review-card">
            <div class="review-header">
                <span class="review-author"><i class="fas fa-user-circle"></i> ${review.user_name}</span>
                <span class="review-date">${new Date(review.created_at).toLocaleDateString()}</span>
            </div>
            <div class="review-rating">
                ${renderStars(review.rating)}
            </div>
            <p class="review-comment">${review.comment}</p>
        </div>
    `).join('');
}

// Render Stars Helper
function renderStars(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= rating) {
            stars += '<i class="fas fa-star"></i>';
        } else {
            stars += '<i class="far fa-star"></i>';
        }
    }
    return stars;
}

// Handle Review Submit
async function handleReviewSubmit(event) {
    event.preventDefault();
    
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
        alert('Please login to write a review');
        window.location.href = 'login.html';
        return;
    }

    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Posting...';

    const rating = document.querySelector('input[name="rating"]:checked')?.value;
    const comment = document.getElementById('reviewComment').value;

    if (!rating) {
        alert('Please select a rating');
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
        return;
    }

    try {
        const response = await api.addReview({
            city_id: currentReviewCityId,
            rating: parseInt(rating),
            comment: comment
        });

        if (response.success) {
            // Reload reviews
            await loadReviews(currentReviewCityId);
            reviewForm.reset();
            alert('Review posted successfully!');
        } else {
            alert(response.error || 'Failed to post review');
        }
    } catch (error) {
        console.error('Review error:', error);
        alert(`Error (v2): ${error.message || 'An error occurred. Please try again.'}`);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
}

// Close modal on outside click
window.onclick = function(event) {
    if (event.target == reviewsModal) {
        closeReviewsModal();
    }
    // Also handle booking modal here if needed, or keep separate
    const bookingModal = document.getElementById('bookingModal');
    if (bookingModal && event.target == bookingModal) {
        bookingModal.style.display = 'none';
    }
}
