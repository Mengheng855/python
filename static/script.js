// Cart Management
let cart = [];
let cartCount = 0;

function updateCartBadge() {
    const badge = document.querySelector('.cart-badge');
    if (badge) {
        badge.textContent = cartCount;
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    
    // Add to cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Update cart count
            cartCount++;
            updateCartBadge();
            
            // Visual feedback
            const icon = this.querySelector('i');
            const originalClass = icon.className;
            
            icon.className = 'bi bi-check2';
            this.classList.add('added');
            
            setTimeout(() => {
                icon.className = originalClass;
                this.classList.remove('added');
            }, 1500);
        });
    });
    
    // Wishlist functionality
    const wishlistButtons = document.querySelectorAll('.wishlist-btn-premium');
    
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const icon = this.querySelector('i');
            
            if (this.classList.contains('active')) {
                this.classList.remove('active');
                icon.className = 'bi bi-heart';
            } else {
                this.classList.add('active');
                icon.className = 'bi bi-heart-fill';
            }
        });
    });
    
    // Newsletter form
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const input = this.querySelector('input[type="email"]');
            const button = this.querySelector('.btn-subscribe');
            const originalText = button.textContent;
            
            if (input.value) {
                button.textContent = 'Subscribed!';
                button.style.backgroundColor = '#10b981';
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.style.backgroundColor = '';
                    input.value = '';
                }, 2000);
            }
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                const target = document.querySelector(href);
                
                if (target) {
                    const navbarHeight = document.querySelector('.navbar').offsetHeight;
                    const targetPosition = target.offsetTop - navbarHeight - 20;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.05)';
        } else {
            navbar.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
    
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe product cards and category cards
    const animatedElements = document.querySelectorAll('.product-card-premium, .category-card-large, .category-card-small, .service-card');
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
    
    // Mobile menu close on link click
    const navLinks = document.querySelectorAll('.nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                    toggle: false
                });
                bsCollapse.hide();
            }
        });
    });
});

// Console log for debugging
console.log('[v0] Electronics store initialized');