// ============================================================================
// GUIDE PAGE - ENHANCED INTERACTIONS
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    const isItalian = document.documentElement.lang === 'it';
    
    // FEATURE 1: SMOOTH SCROLL PER INDICE NAVIGABILE
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            
            if (target) {
                // Offset per header fisso (se presente)
                const offsetTop = target.offsetTop - 80;
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Evidenzia temporaneamente la sezione
                target.style.backgroundColor = '#f8f9fa';
                target.style.transition = 'background-color 0.3s ease';
                
                setTimeout(() => {
                    target.style.backgroundColor = '';
                }, 2000);
            }
        });
    });

    // FEATURE 2: ANIMATE ON SCROLL PER SEZIONI
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Applica animazione alle sezioni principali
    const sections = document.querySelectorAll('.mb-5');
    sections.forEach((section, index) => {
        // Inizializza stato per animazione
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = `opacity 0.8s ease ${index * 0.1}s, transform 0.8s ease ${index * 0.1}s`;
        
        // Osserva per animazione
        observer.observe(section);
    });

    // FEATURE 3: HIGHLIGHT ATTIVO NELL'INDICE
    const updateActiveSection = () => {
        const sections = ['introduzione', 'personaggio', 'inventario', 'ambienti', 'missioni', 'strategia'];
        let activeSection = '';
        
        sections.forEach(sectionId => {
            const section = document.getElementById(sectionId);
            if (section) {
                const rect = section.getBoundingClientRect();
                if (rect.top <= 100 && rect.bottom >= 100) {
                    activeSection = sectionId;
                }
            }
        });
        
        // Rimuovi active da tutti i link
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.classList.remove('active-section');
        });
        
        // Aggiungi active al link corrente
        if (activeSection) {
            const activeLink = document.querySelector(`a[href="#${activeSection}"]`);
            if (activeLink) {
                activeLink.classList.add('active-section');
            }
        }
    };

    // Ascolta scroll per aggiornare sezione attiva
    window.addEventListener('scroll', updateActiveSection);
    updateActiveSection(); // Inizializza

    // FEATURE 4: TOOLTIP SU CARD PERSONAGGI E AMBIENTI
    const addTooltips = () => {
        // Tooltip per classi
        const guerrieroCard = document.querySelector('.text-danger').closest('.card');
        if (guerrieroCard) {
            guerrieroCard.title = isItalian
                ? 'Ideale per principianti - statistiche bilanciate'
                : 'Ideal for beginners - balanced stats';
        }
        
        const magoCard = document.querySelector('.text-primary').closest('.card');
        if (magoCard) {
            magoCard.title = isItalian
                ? 'Alto rischio, alta ricompensa - per giocatori esperti'
                : 'High risk, high reward - for experienced players';
        }
        
        const ladroCard = document.querySelector('.text-dark').closest('.card');
        if (ladroCard) {
            ladroCard.title = isItalian
                ? 'Versatile ma imprevedibile - richiede strategia'
                : 'Versatile but unpredictable - requires strategy';
        }
    };

    addTooltips();

    // FEATURE 5: COUNTER ANIMATION PER STATISTICHE FINALI
    const animateStats = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statElements = entry.target.querySelectorAll('.text-muted.small');
                
                statElements.forEach((el, index) => {
                    const text = el.textContent;
                    if (text.includes('3 ')) {
                        animateNumber(el, 0, 3, '', 1000, text.split(' ')[1]);
                    }
                });
            }
        });
    };

    const statsObserver = new IntersectionObserver(animateStats, { threshold: 0.5 });
    const statsSection = document.querySelector('.row.text-center.mt-4');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }

    // Funzione helper per animare numeri
    function animateNumber(element, start, end, prefix, duration, suffix) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const current = Math.floor(progress * (end - start) + start);
            element.textContent = `${prefix}${current} ${suffix || ''}`;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // FEATURE 6: EASTER EGG - CLICK SU ICONE SPECIFICHE
    let clickCounts = {};
    const easterEggIcons = document.querySelectorAll('.bi-dice-6, .bi-trophy, .bi-magic');
    
    easterEggIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const iconClass = this.className.split(' ').find(c => c.startsWith('bi-'));
            clickCounts[iconClass] = (clickCounts[iconClass] || 0) + 1;
            
            if (clickCounts[iconClass] === 3) {
                this.style.color = '#ff6b6b';
                this.style.animation = 'bounce 0.5s ease';
                
                // Messaggio speciale
                const message = document.createElement('div');
                message.className = 'alert alert-success mt-2';
                message.innerHTML = isItalian
                    ? '<i class="bi bi-star text-warning me-2"></i>Segreto sbloccato! Hai scoperto un bonus!'
                    : '<i class="bi bi-star text-warning me-2"></i>Secret unlocked! You discovered a bonus!';
                
                const parent = this.closest('.card-body') || this.closest('.ps-4');
                if (parent) {
                    parent.appendChild(message);
                    
                    setTimeout(() => {
                        message.style.opacity = '0';
                        setTimeout(() => message.remove(), 500);
                    }, 3000);
                }
                
                clickCounts[iconClass] = 0; // Reset
            }
        });
    });

    // FEATURE 7: HELP LINK FUNCTIONALITY
    const helpLink = document.getElementById('help-link');
    if (helpLink) {
        helpLink.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Mostra modale di aiuto improvvisato
            const helpModal = document.createElement('div');
            const modalTitle = isItalian ? 'Supporto GDR Web App' : 'GDR Web App Support';
            const needHelp = isItalian ? 'Hai bisogno di aiuto?' : 'Need help?';
            const supportIntro = isItalian ? 'Ecco come puoi ottenere supporto:' : 'Here is how you can get support:';
            const chatLabel = isItalian ? 'Chat: Disponibile nel menu principale' : 'Chat: Available in the main menu';
            const docsLabel = isItalian ? 'Documentazione: Questa guida completa' : 'Documentation: This complete guide';
            const eduNote = isItalian
                ? 'Progetto educativo - Il supporto è fornito dai creatori del corso.'
                : 'Educational project - Support is provided by the course creators.';
            const closeLabel = isItalian ? 'Chiudi' : 'Close';
            const goMenuLabel = isItalian ? 'Vai al Menu' : 'Go to Menu';
            helpModal.innerHTML = `
                <div class="modal fade show" style="display: block; background: rgba(0,0,0,0.5);" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">
                                    <i class="bi bi-question-circle me-2"></i>
                                    ${modalTitle}
                                </h5>
                                <button type="button" class="btn-close" data-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <p><strong>${needHelp}</strong></p>
                                <p>${supportIntro}</p>
                                <ul>
                                    <li><i class="bi bi-envelope me-2"></i>Email: support@gdr-webapp.com</li>
                                    <li><i class="bi bi-chat-dots me-2"></i>${chatLabel}</li>
                                    <li><i class="bi bi-book me-2"></i>${docsLabel}</li>
                                </ul>
                                <div class="alert alert-info">
                                    <small><i class="bi bi-info-circle me-1"></i>
                                    ${eduNote}</small>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-dismiss="modal">${closeLabel}</button>
                                <button type="button" class="btn btn-primary">${goMenuLabel}</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(helpModal);
            
            // Gestisci chiusura
            const closeButtons = helpModal.querySelectorAll('[data-dismiss="modal"]');
            closeButtons.forEach(btn => {
                btn.addEventListener('click', () => {
                    helpModal.remove();
                });
            });
            
            // Gestisci vai al menu
            const menuButton = helpModal.querySelector('.btn-primary');
            menuButton.addEventListener('click', () => {
                window.location.href = helpLink?.dataset?.menuUrl || '/menu';
            });
        });
    }

    // FEATURE 8: PROGRESS INDICATOR
    const createProgressIndicator = () => {
        const progressBar = document.createElement('div');
        progressBar.innerHTML = `
            <div class="position-fixed bottom-0 start-0 w-100" style="z-index: 1000;">
                <div class="progress" style="height: 4px; border-radius: 0;">
                    <div class="progress-bar bg-primary" role="progressbar" style="width: 0%"></div>
                </div>
            </div>
        `;
        document.body.appendChild(progressBar);
        
        const bar = progressBar.querySelector('.progress-bar');
        
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            bar.style.width = scrolled + '%';
        });
    };

    createProgressIndicator();

});

// CSS INLINE PER ANIMAZIONI E STILI
const style = document.createElement('style');
style.textContent = `
    @keyframes bounce {
        0%, 20%, 60%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        80% { transform: translateY(-5px); }
    }
    
    .hover-bg-light:hover {
        background-color: #f8f9fa !important;
        transition: background-color 0.2s ease;
    }
    
    .active-section {
        background-color: #e3f2fd !important;
        border-radius: 0.375rem;
        font-weight: 600 !important;
    }
    
    .animate-in {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        transition: transform 0.2s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .btn:hover {
        transform: translateY(-1px);
        transition: transform 0.2s ease;
    }
    
    .bg-gradient {
        position: relative;
        overflow: hidden;
    }
    
    .bg-gradient::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="white" opacity="0.1"/><circle cx="80" cy="80" r="1" fill="white" opacity="0.1"/><circle cx="40" cy="70" r="1.5" fill="white" opacity="0.1"/></svg>');
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-100px, -100px); }
    }
`;
document.head.appendChild(style);

// ============================================================================
// FINE JAVASCRIPT
// ============================================================================

