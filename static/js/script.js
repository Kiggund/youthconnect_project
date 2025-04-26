document.addEventListener("DOMContentLoaded", function () {
    const words = ["Welcome", "to", "Youth", "Connect"]; // Words to animate
    const container = document.getElementById("animated-text"); // Target container

    let index = 0; // Current word index

    function displayWord() {
        if (index < words.length) {
            const span = document.createElement("span");
            span.textContent = words[index]; // Add the current word
            span.className = "animated-word"; // Add a class for styling

            // Apply random color for each word
            span.style.color = `hsl(${Math.random() * 360}, 70%, 50%)`;
            span.style.opacity = 0; // Initially hidden
            span.style.transition = "opacity 1s ease"; // Smooth fade-in

            container.appendChild(span); // Add span to the container

            // Fade in the word
            setTimeout(() => {
                span.style.opacity = 1;
            }, 100);

            index++; // Move to the next word
            setTimeout(displayWord, 1500); // Display next word after 1.5 seconds
        } else {
            // Fade out the entire container after the last word
            setTimeout(() => {
                container.style.opacity = 1; // Ensure visibility before fading
                container.style.transition = "opacity 2s ease"; // Fade-out transition
                container.style.opacity = 0; // Fade out

                setTimeout(() => {
                    container.innerHTML = ""; // Clear all words
                    container.style.opacity = 1; // Reset opacity for next loop
                    index = 0; // Reset word index
                    displayWord(); // Restart animation
                }, 2000); // Delay for fade-out duration
            }, 3000); // Wait after the last word
        }
    }

    displayWord(); // Start the animation
});

// NAVIGATION SYSTEM - COMPLETE SOLUTION
document.addEventListener('DOMContentLoaded', function() {
    // 1. Select Elements
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const body = document.body;
    const navItems = document.querySelectorAll('.nav-link');
    const navbar = document.querySelector('.navbar');
    
    // 2. Menu Toggle Function
    function toggleMenu() {
        // Toggle classes
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
        body.classList.toggle('menu-open');
        
        // Update ARIA attributes for accessibility
        const isExpanded = hamburger.getAttribute('aria-expanded') === 'true';
        hamburger.setAttribute('aria-expanded', !isExpanded);
        
        // Add backdrop when menu is open
        if (navLinks.classList.contains('active')) {
            createBackdrop();
        } else {
            removeBackdrop();
        }
    }
    
    // 3. Create Mobile Menu Backdrop
    function createBackdrop() {
        const backdrop = document.createElement('div');
        backdrop.className = 'nav-backdrop';
        backdrop.addEventListener('click', closeMenu);
        document.body.appendChild(backdrop);
    }
    
    // 4. Remove Mobile Menu Backdrop
    function removeBackdrop() {
        const backdrop = document.querySelector('.nav-backdrop');
        if (backdrop) {
            backdrop.remove();
        }
    }
    
    // 5. Close Menu Function
    function closeMenu() {
        hamburger.classList.remove('active');
        navLinks.classList.remove('active');
        body.classList.remove('menu-open');
        hamburger.setAttribute('aria-expanded', 'false');
        removeBackdrop();
    }
    
    // 6. Event Listeners
    hamburger.addEventListener('click', toggleMenu);
    
    // Close menu when clicking on nav items (mobile)
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                closeMenu();
            }
            setActiveLink(this);
        });
    });
    
    // 7. Set Active Link
    function setActiveLink(clickedLink) {
        navItems.forEach(link => link.classList.remove('active'));
        clickedLink.classList.add('active');
    }
    
    // 8. Sticky Navbar on Scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Highlight current section in view
        highlightCurrentSection();
    });
    
    // 9. Current Section Highlight
    function highlightCurrentSection() {
        const fromTop = window.scrollY + 100;
        
        navItems.forEach(link => {
            const sectionId = link.getAttribute('href');
            if (sectionId.startsWith('#')) {
                const section = document.querySelector(sectionId);
                if (section) {
                    if (section.offsetTop <= fromTop && 
                        section.offsetTop + section.offsetHeight > fromTop) {
                        setActiveLink(link);
                    }
                }
            }
        });
    }
    
    // 10. Close menu when pressing Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navLinks.classList.contains('active')) {
            closeMenu();
        }
    });
    
    // Initialize
    hamburger.setAttribute('aria-expanded', 'false');
});
