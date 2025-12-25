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
    // Real-time validation helpers
    const validators = {
        name: (value) => {
            if (!value || value.trim().length < 3) {
                return 'Name must be at least 3 characters long';
            }
            if (value.length > 50) {
                return 'Name must not exceed 50 characters';
            }
            if (!/^[a-zA-Z\s]+$/.test(value)) {
                return 'Name should only contain letters and spaces';
            }
            return null;
        },
        email: (value) => {
            if (!value) {
                return 'Email is required';
            }
            const emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
            if (!emailRegex.test(value)) {
                return 'Please enter a valid email address';
            }
            return null;
        },
        phone: (value) => {
            if (!value) {
                return 'Phone number is required';
            }
            // Remove any spaces or dashes
            const cleanPhone = value.replace(/[\s-]/g, '');
            if (!/^[6-9]\d{9}$/.test(cleanPhone)) {
                return 'Please enter a valid 10-digit Indian mobile number (starting with 6-9)';
            }
            return null;
        },
        password: (value) => {
            if (!value) {
                return 'Password is required';
            }
            if (value.length < 8) {
                return 'Password must be at least 8 characters long';
            }
            if (!/[a-z]/.test(value)) {
                return 'Password must contain at least one lowercase letter';
            }
            if (!/[A-Z]/.test(value)) {
                return 'Password must contain at least one uppercase letter';
            }
            if (!/\d/.test(value)) {
                return 'Password must contain at least one number';
            }
            return null;
        },
        confirmPassword: (value, password) => {
            if (!value) {
                return 'Please confirm your password';
            }
            if (value !== password) {
                return 'Passwords do not match';
            }
            return null;
        }
    };

    // Show error message
    const showError = (inputId, message) => {
        const errorElement = document.getElementById(inputId + 'Error');
        const inputElement = document.getElementById(inputId);
        if (errorElement && message) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            if (inputElement) {
                inputElement.style.borderColor = '#f56565';
            }
        }
    };

    // Clear error message
    const clearError = (inputId) => {
        const errorElement = document.getElementById(inputId + 'Error');
        const inputElement = document.getElementById(inputId);
        if (errorElement) {
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        }
        if (inputElement) {
            inputElement.style.borderColor = '#48bb78';
        }
    };

    // Add real-time validation
    const nameInput = document.getElementById('signupName');
    const emailInput = document.getElementById('signupEmail');
    const phoneInput = document.getElementById('signupPhone');
    const passwordInput = document.getElementById('signupPassword');
    const confirmPasswordInput = document.getElementById('confirmPassword');

    if (nameInput) {
        nameInput.addEventListener('blur', () => {
            const error = validators.name(nameInput.value);
            error ? showError('signupName', error) : clearError('signupName');
        });
        nameInput.addEventListener('input', () => {
            if (nameInput.value.length >= 3) {
                clearError('signupName');
            }
        });
    }

    if (emailInput) {
        emailInput.addEventListener('blur', () => {
            const error = validators.email(emailInput.value);
            error ? showError('signupEmail', error) : clearError('signupEmail');
        });
        emailInput.addEventListener('input', () => {
            const error = validators.email(emailInput.value);
            if (!error) clearError('signupEmail');
        });
    }

    if (phoneInput) {
        phoneInput.addEventListener('blur', () => {
            const error = validators.phone(phoneInput.value);
            error ? showError('signupPhone', error) : clearError('signupPhone');
        });
        phoneInput.addEventListener('input', (e) => {
            // Only allow numbers
            e.target.value = e.target.value.replace(/\D/g, '');
            if (e.target.value.length === 10) {
                const error = validators.phone(e.target.value);
                error ? showError('signupPhone', error) : clearError('signupPhone');
            }
        });
    }

    if (passwordInput) {
        passwordInput.addEventListener('blur', () => {
            const error = validators.password(passwordInput.value);
            error ? showError('signupPassword', error) : clearError('signupPassword');
        });
    }

    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('blur', () => {
            const error = validators.confirmPassword(confirmPasswordInput.value, passwordInput.value);
            error ? showError('confirmPassword', error) : clearError('confirmPassword');
        });
        confirmPasswordInput.addEventListener('input', () => {
            if (confirmPasswordInput.value === passwordInput.value) {
                clearError('confirmPassword');
            }
        });
    }

    // Form submission
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const agreeTermsInput = document.getElementById('agreeTerms');
        const submitBtn = signupForm.querySelector('button[type="submit"]');

        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const phone = phoneInput.value.replace(/[\s-]/g, '');
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const agreeTerms = agreeTermsInput.checked;

        // Clear all previous errors
        ['signupName', 'signupEmail', 'signupPhone', 'signupPassword', 'confirmPassword'].forEach(clearError);

        // Validate all fields
        let hasError = false;

        const nameError = validators.name(name);
        if (nameError) {
            showError('signupName', nameError);
            hasError = true;
        }

        const emailError = validators.email(email);
        if (emailError) {
            showError('signupEmail', emailError);
            hasError = true;
        }

        const phoneError = validators.phone(phone);
        if (phoneError) {
            showError('signupPhone', phoneError);
            hasError = true;
        }

        const passwordError = validators.password(password);
        if (passwordError) {
            showError('signupPassword', passwordError);
            hasError = true;
        }

        const confirmPasswordError = validators.confirmPassword(confirmPassword, password);
        if (confirmPasswordError) {
            showError('confirmPassword', confirmPasswordError);
            hasError = true;
        }

        if (!agreeTerms) {
            alert('Please agree to Terms & Conditions');
            hasError = true;
        }

        if (hasError) {
            return;
        }

        // Show loading state
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Account...';
        submitBtn.disabled = true;

        try {
            const response = await api.signup({
                username: name.toLowerCase().replace(/\s+/g, ''), // Create username from name
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
