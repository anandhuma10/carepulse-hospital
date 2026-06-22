document.addEventListener('DOMContentLoaded', () => {
    // Select elements
    const header = document.querySelector('.header');
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');
<<<<<<< HEAD
=======
    const bookingForm = document.getElementById('bookingForm');
>>>>>>> feature/department

    // Sticky Header Scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Mobile Hamburger Menu toggle
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            // Toggle hamburger icon animation class
            const icon = navToggle.querySelector('i');
            if (icon) {
                if (navMenu.classList.contains('active')) {
                    icon.className = 'fa-solid fa-xmark';
                } else {
                    icon.className = 'fa-solid fa-bars';
                }
            }
        });
    }

<<<<<<< HEAD
    // Set active class based on current URL path
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        // Handle path highlight logic
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        } else if (href.includes('about') && currentPath.includes('about')) {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        }
    });

=======
>>>>>>> feature/department
    // Close mobile menu when a nav link is clicked
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                const icon = navToggle?.querySelector('i');
                if (icon) icon.className = 'fa-solid fa-bars';
            }
<<<<<<< HEAD
        });
    });
=======

            // Update active link state
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // Simple Intersection Observer to highlight active nav link on scroll
    const sections = document.querySelectorAll('section[id]');
    const observerOptions = {
        root: null,
        rootMargin: '-20% 0px -60% 0px',
        threshold: 0
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    if (link.getAttribute('href').includes(id)) {
                        navLinks.forEach(l => l.classList.remove('active'));
                        link.classList.add('active');
                    }
                });
            }
        });
    }, observerOptions);

    sections.forEach(section => observer.observe(section));
>>>>>>> feature/department
});
