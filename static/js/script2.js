// ===== DOM Elements =====
const themeToggle = document.getElementById('themeToggle');
const menuToggle = document.querySelector('.hamburger'); // Changed from #menuToggle
const navLinks = document.querySelector('.nav-links'); // Changed from #navLinks
const animatedText = document.getElementById('animated-text');
const successCheckmark = document.querySelector('.success-checkmark');

// ===== Theme Management =====
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    document.querySelectorAll('.theme-icon').forEach(icon => {
        icon.style.display = 'none';
    });
    const activeIcon = document.querySelector(`.theme-icon-${theme}`);
    if (activeIcon) activeIcon.style.display = 'inline-block';
}

function initializeTheme() {
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
    
    document.documentElement.setAttribute('data-theme', initialTheme);
    updateThemeIcon(initialTheme);
}

// ===== Navigation System =====
function createBackdrop() {
    if (document.querySelector('.nav-backdrop')) return;
    
    const backdrop = document.createElement('div');
    backdrop.className = 'nav-backdrop';
    backdrop.addEventListener('click', closeMenu);
    document.body.appendChild(backdrop);
}

function removeBackdrop() {
    const backdrop = document.querySelector('.nav-backdrop');
    if (backdrop) backdrop.remove();
}

function closeMenu() {
    if (menuToggle) menuToggle.classList.remove('active');
    if (navLinks) navLinks.classList.remove('active');
    document.body.classList.remove('menu-open');
    removeBackdrop();
}

function toggleMenu() {
    if (!menuToggle || !navLinks) return;
    
    menuToggle.classList.toggle('active');
    navLinks.classList.toggle('active');
    document.body.classList.toggle('menu-open');

    if (navLinks.classList.contains('active')) {
        createBackdrop();
    } else {
        removeBackdrop();
    }
}

function handleNavLinkClick(event) {
    if (window.innerWidth <= 768) closeMenu();
    
    // Update active link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
}

function highlightCurrentSection() {
    const fromTop = window.scrollY + 100;
    document.querySelectorAll('.nav-links a').forEach(link => {
        const sectionId = link.getAttribute('href');
        if (sectionId?.startsWith('#')) {
            const section = document.querySelector(sectionId);
            if (section && section.offsetTop <= fromTop && section.offsetTop + section.offsetHeight > fromTop) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        }
    });
}

function initNavigation() {
    if (!menuToggle || !navLinks) return;

    menuToggle.addEventListener('click', toggleMenu);

    document.querySelectorAll('.nav-links a').forEach(item => {
        item.addEventListener('click', handleNavLinkClick);
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navLinks.classList.contains('active')) {
            closeMenu();
        }
    });

    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.header');
        if (navbar) {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        }
        highlightCurrentSection();
    });
}

// ===== Animated Text =====
function initAnimatedText() {
    if (!animatedText) return;

    const words = ["Welcome", "to", "Youth", "Connect"];
    let index = 0;

    function displayWord() {
        if (index < words.length) {
            const span = document.createElement("span");
            span.textContent = words[index];
            span.className = "animated-word";
            span.style.opacity = 0;
            
            // Use CSS variable for color
            span.style.color = `var(--accent)`;
            
            animatedText.appendChild(span);

            setTimeout(() => {
                span.style.opacity = 1;
            }, 100);

            index++;
            setTimeout(displayWord, 800); // Faster animation
        } else {
            setTimeout(() => {
                animatedText.style.opacity = 0;
                setTimeout(() => {
                    animatedText.innerHTML = "";
                    animatedText.style.opacity = 1;
                    index = 0;
                    displayWord();
                }, 500);
            }, 2000);
        }
    }

    displayWord();
}

// ===== Initialize Everything =====
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    initAnimatedText();
    initNavigation();

    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // System theme change listener
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            initializeTheme();
        }
    });
});
