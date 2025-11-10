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
    
    // Favorites functionality using localStorage
    let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');

    function updateFavoritesCount() {
        const countElement = document.getElementById('favorites-count');
        if (countElement) {
            countElement.textContent = favorites.length;
        }
    }

    function updateFavoriteButtons() {
        const wishlistButtons = document.querySelectorAll('.wishlist-btn-premium');

        wishlistButtons.forEach(button => {
            const productCard = button.closest('.product-card-premium');
            if (productCard) {
                const productId = productCard.querySelector('.product-category-hidden').value;
                const icon = button.querySelector('i');

                if (favorites.includes(productId)) {
                    button.classList.add('active');
                    icon.className = 'bi bi-heart-fill';
                } else {
                    button.classList.remove('active');
                    icon.className = 'bi bi-heart';
                }
            }
        });
    }

    // Initialize favorite buttons and count on page load
    updateFavoriteButtons();
    updateFavoritesCount();

    // Favorites button click handler - now it's a link, so no modal needed
    // The link will navigate to /favorites page

    function showFavoritesModal() {
        // Remove existing modal if any
        const existingModal = document.getElementById('favorites-modal');
        if (existingModal) {
            existingModal.remove();
        }

        // Create modal
        const modal = document.createElement('div');
        modal.id = 'favorites-modal';
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">My Favorites (${favorites.length})</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${favorites.length === 0 ?
                            '<p class="text-center text-muted">No favorites yet. Click the heart icon on products to add them here!</p>' :
                            '<div class="row g-3" id="favorites-list"></div>'
                        }
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Populate favorites if any
        if (favorites.length > 0) {
            const favoritesList = modal.querySelector('#favorites-list');
            favorites.forEach(favId => {
                // Find the product card with this category
                const productCard = Array.from(document.querySelectorAll('.product-card-premium')).find(card => {
                    return card.querySelector('.product-category-hidden').value === favId;
                });

                if (productCard) {
                    const clone = productCard.cloneNode(true);
                    const col = document.createElement('div');
                    col.className = 'col-lg-3 col-md-6';
                    col.appendChild(clone);
                    favoritesList.appendChild(col);
                }
            });
        }

        // Show modal
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }

    // Wishlist functionality
    document.addEventListener('click', function(e) {
        if (e.target.closest('.wishlist-btn-premium')) {
            e.preventDefault();
            e.stopPropagation();

            const button = e.target.closest('.wishlist-btn-premium');
            const productCard = button.closest('.product-card-premium');
            const productId = productCard.querySelector('.product-category-hidden').value;
            const icon = button.querySelector('i');

            if (favorites.includes(productId)) {
                // Remove from favorites
                const index = favorites.indexOf(productId);
                favorites.splice(index, 1);
                button.classList.remove('active');
                icon.className = 'bi bi-heart';
            } else {
                // Add to favorites
                favorites.push(productId);
                button.classList.add('active');
                icon.className = 'bi bi-heart-fill';
            }

            // Save to localStorage
            localStorage.setItem('favorites', JSON.stringify(favorites));

            // Update favorites count
            updateFavoritesCount();
        }
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
    
    // Category filter functionality
    const categoryButtons = document.querySelectorAll('.category-filter-btn');

    categoryButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            // Remove active class from all buttons
            categoryButtons.forEach(btn => btn.classList.remove('active'));

            // Add active class to clicked button
            this.classList.add('active');

            const categoryId = this.getAttribute('data-category');

            // Filter products based on category
            filterProducts(categoryId);
        });
    });

    function filterProducts(categoryId) {
        const productColumns = document.querySelectorAll('.col-lg-3.col-md-6');

        productColumns.forEach(column => {
            const product = column.querySelector('.product-card-premium');
            if (product) {
                const productCategory = product.querySelector('.product-category-hidden').value;
                if (categoryId === 'all' || productCategory.toLowerCase() === categoryId.toLowerCase()) {
                    column.style.display = 'block';
                } else {
                    column.style.display = 'none';
                }
            }
        });

        console.log('Filtering by category:', categoryId);
    }

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