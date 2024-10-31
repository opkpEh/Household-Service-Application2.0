document.addEventListener('DOMContentLoaded', function() {
    const professionalRadio = document.getElementById('professional');
    const customerRadio = document.getElementById('customer');
    const professionalDetails = document.getElementById('professional-details');
    const professionalFields = professionalDetails.querySelectorAll('input, select, textarea');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const signupForm = document.querySelector('.signup-form');

    const passwordMessage = document.createElement('span');
    passwordMessage.className = 'password-message';
    confirmPasswordInput.parentNode.appendChild(passwordMessage);

    function toggleProfessionalFields(isProfessional) {
        professionalDetails.style.display = isProfessional ? 'block' : 'none';
        professionalFields.forEach(field => {
            field.required = isProfessional;
        });
    }

    // function to validate password match
    function validatePasswords() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (!confirmPassword) {
            passwordMessage.style.display = 'none';
            return false;
        }

        if (password === confirmPassword) {
            passwordMessage.textContent = '✓ Passwords match';
            passwordMessage.className = 'password-message success';
            passwordMessage.style.display = 'block';
            return true;
        } else {
            passwordMessage.textContent = '✗ Passwords do not match';
            passwordMessage.className = 'password-message error';
            passwordMessage.style.display = 'block';
            return false;
        }
    }

    function validatePasswordStrength(password) {
        const strongPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
        return strongPassword.test(password);
    }

    passwordInput.addEventListener('input', function() {
        if (!validatePasswordStrength(this.value)) {
            this.setCustomValidity('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number');
        } else {
            this.setCustomValidity('');
        }
        validatePasswords();
    });

    confirmPasswordInput.addEventListener('input', validatePasswords);

    signupForm.addEventListener('submit', function(event) {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        // check if password matches
        if (password !== confirmPassword) {
            event.preventDefault();
            confirmPasswordInput.focus();
            passwordMessage.textContent = '✗ Passwords must match to submit';
            passwordMessage.className = 'password-message error';
            passwordMessage.style.display = 'block';
        }

        // check if password is good
        if (!validatePasswordStrength(password)) {
            event.preventDefault();
            passwordInput.focus();
        }
    });

    // Professional/Customer radio button event listeners
    professionalRadio.addEventListener('change', () => toggleProfessionalFields(true));
    customerRadio.addEventListener('change', () => toggleProfessionalFields(false));
});