document.addEventListener('DOMContentLoaded', function() {
    const waitlistForm = document.getElementById('waitlist-form');
    
    if (waitlistForm) {
        waitlistForm.addEventListener('submit', function(event) {
            // Prevent form submission to validate first
            event.preventDefault();
            
            // Get form inputs
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            
            // Reset previous error messages
            clearErrors();
            
            // Validate inputs
            let isValid = true;
            
            // Validate name (at least 2 characters)
            if (!nameInput.value || nameInput.value.trim().length < 2) {
                displayError(nameInput, 'Please enter your name (at least 2 characters)');
                isValid = false;
            }
            
            // Validate email (basic regex pattern)
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailInput.value || !emailPattern.test(emailInput.value)) {
                displayError(emailInput, 'Please enter a valid email address');
                isValid = false;
            }
            
            // If all validation passes, submit the form
            if (isValid) {
                // Show loading state
                const submitButton = waitlistForm.querySelector('button[type="submit"]');
                const originalButtonText = submitButton.innerHTML;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...';
                submitButton.disabled = true;
                
                // Submit the form
                waitlistForm.submit();
            }
        });
    }
    
    // Function to display error message
    function displayError(inputElement, message) {
        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;
        
        // Add error class to input
        inputElement.classList.add('is-invalid');
        
        // Add error message after input
        inputElement.parentNode.appendChild(errorDiv);
    }
    
    // Function to clear all error messages
    function clearErrors() {
        // Remove all error messages
        document.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
        
        // Remove error class from all inputs
        document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
    }
    
    // Real-time validation for email field
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            // Clear previous error for this field
            this.classList.remove('is-invalid');
            const existingError = this.parentNode.querySelector('.invalid-feedback');
            if (existingError) {
                existingError.remove();
            }
            
            // Validate email format
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (this.value && !emailPattern.test(this.value)) {
                displayError(this, 'Please enter a valid email address');
            }
        });
    }
});