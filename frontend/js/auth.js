/**
 * Authentication Logic
 * Handles login and signup form submissions
 */

// Login Form Handler
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const emailInput = document.getElementById('loginEmail');
        const passwordInput = document.getElementById('loginPassword');
        const submitBtn = loginForm.querySelector('button[type="submit"]');

        const email = emailInput.value;
        const password = passwordInput.value;

        if (!email || !password) {
            alert('Please fill in all fields');
            return;
        }

        // Show loading state
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
        submitBtn.disabled = true;

        try {
            const response = await api.login({ email, password });

            if (response.success) {
                // Save to localStorage
                localStorage.setItem('token', response.token);
                localStorage.setItem('user', JSON.stringify(response.user));

                // Success UI
                submitBtn.innerHTML = '<i class="fas fa-check"></i> Success!';
                submitBtn.style.background = '#48bb78';

                // Redirect after short delay
                setTimeout(() => {
                    window.location.href = '../index.html';
                }, 1000);
            } else {
                throw new Error(response.error || 'Login failed');
            }
        } catch (error) {
            console.error('Login error:', error);
            alert(error.message || 'Login failed. Please check your credentials.');

            // Reset button
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
        }
    });
}

// Signup Form Handler
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const nameInput = document.getElementById('signupName');
        const emailInput = document.getElementById('signupEmail');
        const phoneInput = document.getElementById('signupPhone');
        const passwordInput = document.getElementById('signupPassword');
        const confirmPasswordInput = document.getElementById('confirmPassword');
        const agreeTermsInput = document.getElementById('agreeTerms');
        const submitBtn = signupForm.querySelector('button[type="submit"]');

        const name = nameInput.value;
        const email = emailInput.value;
        const phone = phoneInput.value;
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const agreeTerms = agreeTermsInput.checked;

        // Validation
        if (!name || !email || !phone || !password || !confirmPassword) {
            alert('Please fill in all fields');
            return;
        }

        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }

        if (password.length < 8) {
            alert('Password must be at least 8 characters long');
            return;
        }

        if (!agreeTerms) {
            alert('Please agree to Terms & Conditions');
            return;
        }

        // Show loading state
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Account...';
        submitBtn.disabled = true;

        try {
            const response = await api.signup({
                username: name, // Using name as username for simplicity or split if needed
                email: email,
                password: password,
                full_name: name,
                phone: phone
            });

            if (response.success) {
                // Success
                submitBtn.innerHTML = '<i class="fas fa-check"></i> Account Created!';
                submitBtn.style.background = '#48bb78';

                // Redirect to login
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 1500);
            } else {
                throw new Error(response.error || 'Signup failed');
            }
        } catch (error) {
            console.error('Signup error:', error);
            alert(error.message || 'Signup failed. Please try again.');

            // Reset button
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
        }
    });
}

// Password Toggle Helper
function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);
    const icon = button.querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

// Password Strength Checker (only on signup page)
const signupPasswordInput = document.getElementById('signupPassword');
if (signupPasswordInput) {
    signupPasswordInput.addEventListener('input', (e) => {
        const password = e.target.value;
        const strengthBar = document.getElementById('strengthBar');
        const strengthText = document.getElementById('strengthText');

        if (!strengthBar || !strengthText) return;

        let strength = 0;
        if (password.length >= 8) strength += 25;
        if (/[a-z]/.test(password)) strength += 25;
        if (/[A-Z]/.test(password)) strength += 25;
        if (/[0-9]/.test(password)) strength += 25;

        strengthBar.style.width = strength + '%';

        if (strength <= 25) {
            strengthBar.style.background = '#f56565';
            strengthText.textContent = 'Password strength: Weak';
            strengthText.style.color = '#f56565';
        } else if (strength <= 50) {
            strengthBar.style.background = '#ed8936';
            strengthText.textContent = 'Password strength: Fair';
            strengthText.style.color = '#ed8936';
        } else if (strength <= 75) {
            strengthBar.style.background = '#48bb78';
            strengthText.textContent = 'Password strength: Good';
            strengthText.style.color = '#48bb78';
        } else {
            strengthBar.style.background = '#38a169';
            strengthText.textContent = 'Password strength: Strong';
            strengthText.style.color = '#38a169';
        }
    });
}
