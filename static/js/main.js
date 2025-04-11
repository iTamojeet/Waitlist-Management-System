document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Animation for elements when they enter viewport
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const animateOnScroll = function() {
        animatedElements.forEach(element => {
            const elementPosition = element.getBoundingClientRect();
            const windowHeight = window.innerHeight;
            
            if (elementPosition.top < windowHeight * 0.9) {
                element.classList.add('fade-in');
            }
        });
    };
    
    // Run once on page load
    animateOnScroll();
    
    // And on scroll
    window.addEventListener('scroll', animateOnScroll);
    
    // Countdown timer for launch (example: 30 days from now)
    const countdownElement = document.getElementById('countdown-timer');
    if (countdownElement) {
        const launchDate = new Date();
        launchDate.setDate(launchDate.getDate() + 30);
        
        const updateCountdown = function() {
            const now = new Date();
            const timeDifference = launchDate - now;
            
            // If launch date has passed
            if (timeDifference < 0) {
                countdownElement.textContent = "Launching soon!";
                return;
            }
            
            const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
            const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);
            
            countdownElement.textContent = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        };
        
        // Update timer every second
        updateCountdown();
        setInterval(updateCountdown, 1000);
    }
    
    // Initialize tooltips if using Bootstrap 5
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Social sharing functions
    window.shareOnSocial = function(platform) {
        const url = window.location.origin;
        const text = "Join the waitlist for this exciting new product! 🚀";
        
        let shareUrl;
        
        switch(platform) {
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
                break;
            case 'facebook':
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
                break;
            case 'linkedin':
                shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
                break;
            default:
                return;
        }
        
        window.open(shareUrl, '_blank', 'width=600,height=400');
    }
    
    // Track waitlist interactions for analytics
    const waitlistForm = document.getElementById('waitlist-form');
    if (waitlistForm) {
        // Track form focus
        const formInputs = waitlistForm.querySelectorAll('input, select');
        formInputs.forEach(input => {
            input.addEventListener('focus', function() {
                console.log('Form interaction:', this.name);
                // In a real app, you might send this to an analytics service
            });
        });
        
        // Track form submission attempts
        waitlistForm.addEventListener('submit', function() {
            console.log('Form submitted');
            // In a real app, you might send this to an analytics service
        });
    }
    
    // Add confetti effect when someone joins (on success page)
    if (window.location.pathname.includes('/success')) {
        // Simple confetti effect
        const confettiCount = 200;
        const container = document.querySelector('body');
        
        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            
            // Random position, color and size
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.animationDelay = Math.random() * 5 + 's';
            confetti.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 50%)`;
            
            container.appendChild(confetti);
            
            // Remove after animation
            setTimeout(() => {
                confetti.remove();
            }, 6000);
        }
    }
});