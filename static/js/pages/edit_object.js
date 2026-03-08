function showObjectInfo() {
    const select = document.getElementById('oggetto');
    const infoDiv = document.getElementById('object-info');
    const infoContent = document.getElementById('info-content');
    const isItalian = document.documentElement.lang === 'it';

    if (select.value) {
        const descriptions = {
            Arma: {
                description: isItalian ? 'Oggetti per aumentare il danno in combattimento' : 'Items that increase combat damage',
                icon: 'fas fa-sword',
                color: '#dc3545'
            },
            Pozione: {
                description: isItalian ? 'Consumabili per recuperare salute o energie' : 'Consumables to restore health or energy',
                icon: 'fas fa-flask',
                color: '#28a745'
            },
            Armatura: {
                description: isItalian ? 'Protezioni per ridurre i danni subiti' : 'Protection to reduce incoming damage',
                icon: 'fas fa-shield-alt',
                color: '#6c757d'
            },
            Accessorio: {
                description: isItalian ? 'Oggetti speciali con effetti unici' : 'Special items with unique effects',
                icon: 'fas fa-ring',
                color: '#ffc107'
            },
            Strumento: {
                description: isItalian ? 'Utilità varie per esplorazioni e crafting' : 'Utility tools for exploration and crafting',
                icon: 'fas fa-tools',
                color: '#17a2b8'
            },
            Consumabile: {
                description: isItalian ? 'Oggetti usa e getta con effetti immediati' : 'Single-use items with immediate effects',
                icon: 'fas fa-apple-alt',
                color: '#fd7e14'
            }
        };

        const objInfo = descriptions[select.value];
        if (objInfo) {
            infoContent.innerHTML = `
                <div class="d-flex align-items-center">
                    <i class="${objInfo.icon} me-2" style="color: ${objInfo.color}; font-size: 1.5rem;"></i>
                    <div>
                        <strong>${select.value}</strong><br>
                        <small class="text-muted">${objInfo.description}</small>
                    </div>
                </div>
            `;
        } else {
            infoContent.innerHTML = `
                <div class="d-flex align-items-center">
                    <i class="fas fa-box me-2" style="color: #6c757d; font-size: 1.5rem;"></i>
                    <div>
                        <strong>${select.value}</strong><br>
                        <small class="text-muted">${isItalian ? 'Oggetto generico del gioco' : 'Generic game item'}</small>
                    </div>
                </div>
            `;
        }

        infoDiv.classList.remove('d-none');
    } else {
        infoDiv.classList.add('d-none');
    }
}

document.querySelector('form').addEventListener('submit', function(e) {
    const oggetto = document.getElementById('oggetto').value;
    const isItalian = document.documentElement.lang === 'it';

    if (!oggetto) {
        e.preventDefault();
        alert(isItalian ? 'Seleziona un tipo di oggetto!' : 'Select an item type!');
    }
});
