// ============================================================================
// MENU PAGE - ENHANCED FUNCTIONALITY
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    initMenuEffects();
    });

/**
 * Mostra una sezione specifica e nasconde le altre
 * @param {string} sectionId - ID della sezione da mostrare
 */
function showSection(sectionId) {
        
    const sections = ['area-personale', 'modalita-gioco'];
    const buttons = {
        'area-personale': document.getElementById('btn-area'),
        'modalita-gioco': document.getElementById('btn-gioco')
    };

    const cardsBySection = {
        'area-personale': [
            document.getElementById('card-profilo'),
            document.getElementById('card-personaggi')
        ],
        'modalita-gioco': [
            document.getElementById('card-gioco'),
            document.getElementById('card-inventario')
        ]
    };

    // Nascondi tutte le sezioni e resetta i pulsanti
    sections.forEach(id => {
        const section = document.getElementById(id);
        if (section) {
            section.style.display = 'none';
            section.classList.remove('section-block');
        }

        const button = buttons[id];
        if (button) {
            // Reset button styles
            button.classList.remove('btn-fantasy-blue', 'btn-fantasy-crimson', 'text-white');
            button.classList.add(
                id === 'area-personale' ? 'btn-outline-fantasy-blue' : 'btn-outline-fantasy-crimson'
            );
        }

        // Rimuovi evidenziazione dalle cards
        if (cardsBySection[id]) {
            cardsBySection[id].forEach(card => {
                if (card) {
                    card.classList.remove('highlight-blue', 'highlight-crimson');
                }
            });
        }
    });

    // Mostra la sezione selezionata con animazione
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.style.display = 'block';
        
        // Piccolo delay per far funzionare l'animazione CSS
        setTimeout(() => {
            targetSection.classList.add('section-block');
        }, 50);
    }

    // Aggiorna stile del pulsante attivo
    const activeButton = buttons[sectionId];
    if (activeButton) {
        if (sectionId === 'area-personale') {
            activeButton.classList.remove('btn-outline-fantasy-blue');
            activeButton.classList.add('btn-fantasy-blue', 'text-white');

            // Evidenzia le cards con animazione ritardata
            if (cardsBySection[sectionId]) {
                cardsBySection[sectionId].forEach((card, index) => {
                    if (card) {
                        setTimeout(() => {
                            card.classList.add('highlight-blue');
                        }, 200 + (index * 100));
                    }
                });
            }
        } else {
            activeButton.classList.remove('btn-outline-fantasy-crimson');
            activeButton.classList.add('btn-fantasy-crimson', 'text-white');

            // Evidenzia le cards con animazione ritardata
            if (cardsBySection[sectionId]) {
                cardsBySection[sectionId].forEach((card, index) => {
                    if (card) {
                        setTimeout(() => {
                            card.classList.add('highlight-crimson');
                        }, 200 + (index * 100));
                    }
                });
            }
        }
    }

    // Scroll fluido alla sezione
    if (targetSection) {
        const offsetTop = targetSection.offsetTop - 100;
        
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }

    }

/**
 * Inizializza gli effetti e interazioni del menu
 */
function initMenuEffects() {
    
    // Effetti hover sulle game cards
    const gameCards = document.querySelectorAll('.game-card');
    gameCards.forEach((card, index) => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });

        // Animazione di entrata scaglionata
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Effetti sui pulsanti principali
    const mainButtons = document.querySelectorAll('.main-button');
    mainButtons.forEach((button, index) => {
        // Animazione shine on hover
        button.addEventListener('mouseenter', function() {
            const shine = this.querySelector('.button-shine');
            if (shine) {
                shine.style.left = '100%';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            const shine = this.querySelector('.button-shine');
            if (shine) {
                // Reset con delay per evitare loop
                setTimeout(() => {
                    shine.style.left = '-100%';
                }, 200);
            }
        });

        // Animazione di entrata
        button.style.opacity = '0';
        button.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            button.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            button.style.opacity = '1';
            button.style.transform = 'translateY(0)';
        }, 300 + (index * 150));
    });

    // Effetto click con feedback visivo su tutti i pulsanti
    const allButtons = document.querySelectorAll('.btn');
    allButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Piccola animazione di feedback
            const originalTransform = this.style.transform || '';
            this.style.transform = 'scale(0.95)';
            
            setTimeout(() => {
                this.style.transform = originalTransform;
            }, 150);
        });
    });

    // Animazione contatori
    animateCounters();

    }

/**
 * Anima i contatori numerici nelle card
 */
function animateCounters() {
    const creditElement = document.querySelector('.text-success.h5');
    const charElement = document.querySelector('.text-info.h5');
    
    if (creditElement) {
        const finalValue = parseInt(creditElement.textContent) || 0;
        animateNumber(creditElement, 0, finalValue, 1500);
    }
    
    if (charElement) {
        const finalValue = parseInt(charElement.textContent) || 0;
        animateNumber(charElement, 0, finalValue, 1000);
    }
}

/**
 * Anima un numero da start a end
 * @param {Element} element - Elemento da animare
 * @param {number} start - Valore iniziale
 * @param {number} end - Valore finale
 * @param {number} duration - Durata in millisecondi
 */
function animateNumber(element, start, end, duration) {
    if (start === end) return;
    
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const current = Math.floor(progress * (end - start) + start);
        element.textContent = current;
        
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    
    window.requestAnimationFrame(step);
}

/**
 * Gestione notifiche di sistema (se necessarie)
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px; 
        right: 20px; 
        z-index: 9999; 
        max-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    `;
    
    notification.innerHTML = `
        <strong>${message}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-rimozione dopo 5 secondi
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 500);
        }
    }, 5000);
}

// Esponi funzioni globalmente per uso nei template
window.showSection = showSection;
window.showNotification = showNotification;


// ============================================================================
// FINE JAVASCRIPT
// ============================================================================

