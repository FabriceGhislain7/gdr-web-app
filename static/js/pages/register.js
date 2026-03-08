// ============================================================================
// REGISTRAZIONE FORM - JAVASCRIPT ENHANCED FEATURES
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // ELEMENTI DOM
    const form = document.getElementById('registerForm');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('psw');
    const confirmPasswordInput = document.getElementById('re_psw');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const toggleIcon = document.getElementById('toggleIcon');
    const suggestPasswordBtn = document.getElementById('suggest-password');
    const showRequirementsBtn = document.getElementById('show-requirements');
    const submitBtn = document.getElementById('submit-btn');
    const resetBtn = document.getElementById('reset-btn');

    // ELEMENTI FEEDBACK
    const strengthIndicator = document.getElementById('password-strength');
    const strengthBar = document.getElementById('strength-bar');
    const strengthMessage = document.getElementById('strength-message');
    const passwordMatch = document.getElementById('password-match');
    const matchMessage = document.getElementById('match-message');
    const requirementsPanel = document.getElementById('password-requirements');

    // ========================================================================
    // FEATURE 1: TOGGLE VISIBILITÀ PASSWORD
    // ========================================================================
    togglePasswordBtn.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        confirmPasswordInput.setAttribute('type', type);
        
        // Cambia icona
        if (type === 'text') {
            toggleIcon.className = 'bi bi-eye-slash';
            togglePasswordBtn.title = 'Nascondi password';
        } else {
            toggleIcon.className = 'bi bi-eye';
            togglePasswordBtn.title = 'Mostra password';
        }
    });

    // ========================================================================
    // FEATURE 2: VALIDAZIONE PASSWORD IN TEMPO REALE
    // ========================================================================
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        
        if (password.length > 0) {
            checkPasswordStrength(password);
            strengthIndicator.style.display = 'block';
        } else {
            strengthIndicator.style.display = 'none';
        }
        
        // Controlla match se conferma non è vuota
        if (confirmPasswordInput.value.length > 0) {
            checkPasswordMatch();
        }
    });

    // ========================================================================
    // FEATURE 3: CONTROLLO MATCH PASSWORD
    // ========================================================================
    confirmPasswordInput.addEventListener('input', checkPasswordMatch);

    function checkPasswordMatch() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        
        if (confirmPassword.length > 0) {
            passwordMatch.style.display = 'block';
            
            if (password === confirmPassword) {
                matchMessage.textContent = '✅ Le password coincidono';
                matchMessage.className = 'text-success';
                confirmPasswordInput.classList.remove('is-invalid');
                confirmPasswordInput.classList.add('is-valid');
            } else {
                matchMessage.textContent = '❌ Le password non coincidono';
                matchMessage.className = 'text-danger';
                confirmPasswordInput.classList.remove('is-valid');
                confirmPasswordInput.classList.add('is-invalid');
            }
        } else {
            passwordMatch.style.display = 'none';
            confirmPasswordInput.classList.remove('is-valid', 'is-invalid');
        }
    }

    // ========================================================================
    // FEATURE 4: CONTROLLO FORZA PASSWORD (API CALL)
    // ========================================================================
    function checkPasswordStrength(password) {
        // Simulazione API call - sostituisci con vera chiamata quando API è pronta
        // fetch('/api/check-password-strength', {
        //     method: 'POST',
        //     headers: {'Content-Type': 'application/json'},
        //     body: JSON.stringify({password: password})
        // })
        // .then(response => response.json())
        // .then(data => updateStrengthIndicator(data));

        // VERSIONE MOCK per ora (sostituisci quando API è pronta)
        const mockStrength = calculateMockStrength(password);
        updateStrengthIndicator(mockStrength);
    }

    function calculateMockStrength(password) {
        let score = 0;
        let color = 'red';
        let message = 'Molto debole';
        
        if (password.length >= 8) score += 25;
        if (/[A-Z]/.test(password)) score += 25;
        if (/[a-z]/.test(password)) score += 25;
        if (/\d/.test(password)) score += 15;
        if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 10;
        
        if (score >= 90) { color = 'green'; message = 'Molto forte'; }
        else if (score >= 70) { color = 'lightgreen'; message = 'Forte'; }
        else if (score >= 50) { color = 'yellow'; message = 'Media'; }
        else if (score >= 30) { color = 'orange'; message = 'Debole'; }
        
        return { score, color, message, progress: score };
    }

    function updateStrengthIndicator(data) {
        strengthBar.style.width = data.progress + '%';
        strengthBar.style.backgroundColor = data.color;
        strengthMessage.textContent = data.message;
        strengthMessage.className = `form-text text-${data.color === 'green' ? 'success' : 
                                      data.color === 'lightgreen' ? 'success' : 
                                      data.color === 'yellow' ? 'warning' : 'danger'}`;
    }

    // ========================================================================
    // FEATURE 5: SUGGERIMENTI PASSWORD
    // ========================================================================
    suggestPasswordBtn.addEventListener('click', function() {
        // Simulazione generazione password - sostituisci con vera API
        // fetch('/api/generate-password?length=12&readable=true')
        // .then(response => response.json())
        // .then(data => {
        //     passwordInput.value = data.password;
        //     confirmPasswordInput.value = data.password;
        //     passwordInput.dispatchEvent(new Event('input'));
        // });

        // VERSIONE MOCK per ora
        const mockPassword = generateMockPassword();
        passwordInput.value = mockPassword;
        confirmPasswordInput.value = mockPassword;
        passwordInput.dispatchEvent(new Event('input'));
        
        // Feedback visivo
        suggestPasswordBtn.innerHTML = '✅ Password Generata!';
        setTimeout(() => {
            suggestPasswordBtn.innerHTML = '🎲 Suggerisci Password Sicura';
        }, 2000);
    });

    function generateMockPassword() {
        const chars = 'ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789!@#$%^&*';
        const length = 12;
        let password = '';
        
        // Assicura almeno un carattere di ogni tipo
        password += 'ABCDEFGHJKMNPQRSTUVWXYZ'[Math.floor(Math.random() * 23)]; // Maiuscola
        password += 'abcdefghjkmnpqrstuvwxyz'[Math.floor(Math.random() * 23)]; // Minuscola  
        password += '23456789'[Math.floor(Math.random() * 8)]; // Numero
        password += '!@#$%^&*'[Math.floor(Math.random() * 8)]; // Speciale
        
        // Riempi resto random
        for (let i = 4; i < length; i++) {
            password += chars[Math.floor(Math.random() * chars.length)];
        }
        
        // Mescola caratteri
        return password.split('').sort(() => Math.random() - 0.5).join('');
    }

    // ========================================================================
    // FEATURE 6: TOGGLE PANNELLO REQUISITI
    // ========================================================================
    showRequirementsBtn.addEventListener('click', function() {
        if (requirementsPanel.style.display === 'none') {
            requirementsPanel.style.display = 'block';
            showRequirementsBtn.innerHTML = '🔼 Nascondi Requisiti';
        } else {
            requirementsPanel.style.display = 'none';
            showRequirementsBtn.innerHTML = 'ℹ️ Requisiti';
        }
    });

    // ========================================================================
    // FEATURE 7: VALIDAZIONE FORM SUBMIT
    // ========================================================================
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Reset classi validazione
        [usernameInput, emailInput, passwordInput, confirmPasswordInput].forEach(input => {
            input.classList.remove('is-invalid', 'is-valid');
        });

        // Validazione username
        if (usernameInput.value.length < 3) {
            usernameInput.classList.add('is-invalid');
            document.getElementById('username-feedback').textContent = 'Username troppo corto (minimo 3 caratteri)';
            isValid = false;
        }

        // Validazione email
        const emailRegex = /^[\w\.-]+@[\w\.-]+\.\w+$/;
        if (!emailRegex.test(emailInput.value)) {
            emailInput.classList.add('is-invalid');
            document.getElementById('email-feedback').textContent = 'Formato email non valido';
            isValid = false;
        }

        // Validazione password
        if (passwordInput.value.length < 8) {
            passwordInput.classList.add('is-invalid');
            document.getElementById('password-feedback').textContent = 'Password troppo corta (minimo 8 caratteri)';
            isValid = false;
        }

        // Validazione match password
        if (passwordInput.value !== confirmPasswordInput.value) {
            confirmPasswordInput.classList.add('is-invalid');
            document.getElementById('confirm-feedback').textContent = 'Le password non coincidono';
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
            return false;
        }

        // Mostra spinner durante submit
        document.getElementById('submit-text').textContent = 'Registrando...';
        document.getElementById('submit-spinner').style.display = 'inline-block';
        submitBtn.disabled = true;
    });

    // ========================================================================
    // FEATURE 8: RESET FORM
    // ========================================================================
    resetBtn.addEventListener('click', function() {
        // Reset indicatori
        strengthIndicator.style.display = 'none';
        passwordMatch.style.display = 'none';
        requirementsPanel.style.display = 'none';
        
        // Reset classi validazione
        [usernameInput, emailInput, passwordInput, confirmPasswordInput].forEach(input => {
            input.classList.remove('is-invalid', 'is-valid');
        });
        
        // Reset bottoni
        showRequirementsBtn.innerHTML = 'ℹ️ Requisiti';
        suggestPasswordBtn.innerHTML = '🎲 Suggerisci Password Sicura';
        
        // Reset password visibility
        passwordInput.setAttribute('type', 'password');
        confirmPasswordInput.setAttribute('type', 'password');
        toggleIcon.className = 'bi bi-eye';
    });

});

// ============================================================================
// FINE JAVASCRIPT
// ============================================================================

