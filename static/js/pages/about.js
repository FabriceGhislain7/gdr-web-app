// ============================================================================
// ABOUT PAGE - ENHANCED INTERACTIONS
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    
    // FEATURE 1: SMOOTH SCROLL PER SEZIONI (se servisse)
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // FEATURE 2: ANIMATE ON SCROLL (opzionale - leggero)
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Applica animazione alle sezioni
    const sections = document.querySelectorAll('.mb-5');
    sections.forEach((section, index) => {
        // Inizializza stato
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = `opacity 0.6s ease, transform 0.6s ease`;
        section.style.transitionDelay = `${index * 0.1}s`;
        
        // Osserva per animazione
        observer.observe(section);
    });

    // FEATURE 3: TOOLTIP SU BADGE E ICONE (se Bootstrap tooltip è disponibile)
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // FEATURE 4: COUNTER ANIMATION PER STATISTICHE
    const counters = document.querySelectorAll('.text-muted.small');
    const animateCounters = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const text = counter.textContent;
                
                // Se contiene numeri, animali
                if (text.includes('3000+')) {
                    animateNumber(counter, 0, 3000, '+', 2000);
                } else if (text.includes('100+')) {
                    animateNumber(counter, 0, 100, '+', 1500);
                }
            }
        });
    };

    const counterObserver = new IntersectionObserver(animateCounters, {
        threshold: 0.5
    });

    counters.forEach(counter => {
        if (counter.textContent.includes('+')) {
            counterObserver.observe(counter);
        }
    });

    // Funzione helper per animare numeri
    function animateNumber(element, start, end, suffix, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const current = Math.floor(progress * (end - start) + start);
            element.textContent = `~${current}${suffix}`;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // FEATURE 5: EASTER EGG - Click su logo/icone speciali
    let clickCount = 0;
    const heartIcon = document.querySelector('.bi-heart');
    if (heartIcon) {
        heartIcon.addEventListener('click', function() {
            clickCount++;
            if (clickCount === 5) {
                this.style.color = '#ff6b6b';
                this.style.animation = 'pulse 1s infinite';
                
                // Mostra messaggio nascosto
                const message = document.createElement('div');
                message.className = 'alert alert-success mt-3';
                message.innerHTML = '<i class="bi bi-heart-fill text-danger me-2"></i>Grazie per aver esplorato il nostro progetto! 🎮❤️';
                this.closest('.ps-4').appendChild(message);
                
                // Rimuovi dopo 5 secondi
                setTimeout(() => {
                    message.style.opacity = '0';
                    setTimeout(() => message.remove(), 500);
                }, 5000);
                
                clickCount = 0; // Reset
            }
        });
    }

});

// CSS INLINE PER ANIMAZIONI
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .btn:hover {
        transform: translateY(-2px);
        transition: transform 0.2s ease;
    }
    
    .bg-light:hover {
        background-color: #f8f9fa !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
`;
document.head.appendChild(style);

// ============================================================================
// FINE JAVASCRIPT
// ============================================================================

