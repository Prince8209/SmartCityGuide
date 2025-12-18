/**
 * Booking Logic
 * Handles booking modal, cost calculation, and API submission
 */

// State
let currentBookingCity = '';
let currentDailyBudget = 0;

// DOM Elements
const bookingModal = document.getElementById('bookingModal');
const bookingForm = document.getElementById('bookingForm');
const bookingFormContainer = document.getElementById('bookingFormContainer');
const bookingSuccess = document.getElementById('bookingSuccess');

// Inputs
const checkInInput = document.getElementById('checkInDate');
const checkOutInput = document.getElementById('checkOutDate');
const travelersInput = document.getElementById('numTravelers');
const totalCostDisplay = document.getElementById('totalCostDisplay');
const costBreakdown = document.getElementById('costBreakdown');

// Open Modal
function openBookingModal(cityName, dailyBudget) {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
        alert('Please login to book a trip!');
        window.location.href = 'login.html';
        return;
    }

    currentBookingCity = cityName;
    currentDailyBudget = dailyBudget;

    // Reset UI
    bookingForm.reset();
    bookingFormContainer.style.display = 'block';
    bookingSuccess.style.display = 'none';
    
    // Set hidden fields
    document.getElementById('bookingCityName').value = cityName;
    document.getElementById('bookingDailyBudget').value = dailyBudget;

    // Pre-fill user info if available
    if (user) {
        document.getElementById('customerName').value = user.full_name || '';
        document.getElementById('customerEmail').value = user.email || '';
    }

    // Set default dates (Tomorrow -> 3 days later)
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    const threeDaysLater = new Date(tomorrow);
    threeDaysLater.setDate(threeDaysLater.getDate() + 3);

    checkInInput.valueAsDate = tomorrow;
    checkOutInput.valueAsDate = threeDaysLater;
    
    // Set min dates
    checkInInput.min = new Date().toISOString().split('T')[0];
    checkOutInput.min = tomorrow.toISOString().split('T')[0];

    // Initial calculation
    calculateTotal();

    // Show modal
    bookingModal.style.display = 'flex';
}

// Close Modal
function closeBookingModal() {
    bookingModal.style.display = 'none';
}

// Calculate Total Cost
function calculateTotal() {
    const checkIn = new Date(checkInInput.value);
    const checkOut = new Date(checkOutInput.value);
    const travelers = parseInt(travelersInput.value) || 1;

    if (checkIn && checkOut && checkOut > checkIn) {
        const diffTime = Math.abs(checkOut - checkIn);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
        
        const total = diffDays * travelers * currentDailyBudget;

        totalCostDisplay.textContent = `₹${total.toLocaleString()}`;
        costBreakdown.innerHTML = `
            <small>
                ${diffDays} days × ${travelers} travelers × ₹${currentDailyBudget}/day
            </small>
        `;
    } else {
        totalCostDisplay.textContent = '₹0';
        costBreakdown.innerHTML = '<small style="color: red;">Invalid dates</small>';
    }
}

// Handle Form Submit
async function handleBookingSubmit(event) {
    event.preventDefault();

    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

    try {
        const formData = {
            city_name: currentBookingCity,
            customer_name: document.getElementById('customerName').value,
            customer_email: document.getElementById('customerEmail').value,
            customer_phone: document.getElementById('customerPhone').value,
            check_in_date: checkInInput.value,
            check_out_date: checkOutInput.value,
            num_travelers: parseInt(travelersInput.value),
            daily_budget: currentDailyBudget
        };

        const response = await api.createBooking(formData);

        if (response.success) {
            showSuccess(response.booking);
        } else {
            alert(response.error || 'Booking failed. Please try again.');
        }
    } catch (error) {
        console.error('Booking error:', error);
        alert('An error occurred. Please try again.');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
}

// Show Success View
function showSuccess(booking) {
    bookingFormContainer.style.display = 'none';
    bookingSuccess.style.display = 'block';

    // Fill details
    document.getElementById('bookingReference').textContent = booking.booking_reference;
    document.getElementById('bookingCity').textContent = booking.city_name;
    document.getElementById('bookingDates').textContent = `${booking.check_in_date} to ${booking.check_out_date}`;
    document.getElementById('bookingTravelers').textContent = booking.num_travelers;
    document.getElementById('bookingTotal').textContent = `₹${booking.total_cost}`;

    // Setup PDF download
    document.getElementById('downloadPdfBtn').onclick = () => downloadPDF(booking);
}

// Download PDF
function downloadPDF(booking) {
    if (!window.jspdf) {
        alert('PDF generation library not loaded.');
        return;
    }

    const doc = new window.jspdf.jsPDF();
    
    // Header
    doc.setFontSize(22);
    doc.setTextColor(102, 126, 234); // Brand color
    doc.text("Smart City Guide", 20, 20);
    
    doc.setFontSize(16);
    doc.setTextColor(0, 0, 0);
    doc.text("Booking Confirmation", 20, 35);

    // Details
    doc.setFontSize(12);
    doc.setLineHeightFactor(1.5);
    
    let y = 50;
    const addLine = (label, value) => {
        doc.setFont(undefined, 'bold');
        doc.text(`${label}:`, 20, y);
        doc.setFont(undefined, 'normal');
        doc.text(String(value), 70, y);
        y += 10;
    };

    addLine("Reference", booking.booking_reference);
    addLine("City", booking.city_name);
    addLine("Customer", booking.customer_name);
    addLine("Check-in", booking.check_in_date);
    addLine("Check-out", booking.check_out_date);
    addLine("Travelers", booking.num_travelers);
    addLine("Total Cost", `Rs. ${booking.total_cost}`);
    
    // Footer
    doc.setFontSize(10);
    doc.setTextColor(100);
    doc.text("Thank you for booking with Smart City Guide!", 20, y + 10);

    doc.save(`Booking_${booking.booking_reference}.pdf`);
}

// Event Listeners for Calculation
checkInInput.addEventListener('change', calculateTotal);
checkOutInput.addEventListener('change', calculateTotal);
travelersInput.addEventListener('input', calculateTotal);

// Close modal on outside click
window.onclick = function(event) {
    if (event.target == bookingModal) {
        closeBookingModal();
    }
}
