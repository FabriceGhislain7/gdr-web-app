document.addEventListener('DOMContentLoaded', function() {
    // Effetto parallax sulle particelle
    document.addEventListener('mousemove', function(e) {
      const particles = document.querySelectorAll('.particle');
      const mouseX = e.clientX / window.innerWidth;
      const mouseY = e.clientY / window.innerHeight;
      
      particles.forEach((particle, index) => {
        const speed = (index + 1) * 0.3;
        const x = (mouseX - 0.5) * speed * 10;
        const y = (mouseY - 0.5) * speed * 10;
        
        particle.style.transform = `translate(${x}px, ${y}px)`;
      });
    });

    // Effetto scintillio sulle icone delle features
    const featureIcons = document.querySelectorAll('.feature-icon');
    featureIcons.forEach(icon => {
      setInterval(() => {
        icon.style.transform = 'scale(1.1)';
        setTimeout(() => {
          icon.style.transform = 'scale(1)';
        }, 200);
      }, Math.random() * 5000 + 3000);
    });

    // Effetto ondulazione sui pulsanti
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
      button.addEventListener('mouseenter', function() {
        this.style.boxShadow = '0 0 20px rgba(0,0,0,0.3)';
      });
      
      button.addEventListener('mouseleave', function() {
        this.style.boxShadow = '';
      });
    });
  });

  // Funzione per rimuovere completamente l'overlay
  function removeOverlay() {
    const style = document.createElement('style');
    style.textContent = 'body::before { display: none !important; }';
    document.head.appendChild(style);
    console.log('Overlay rimosso - immagine a piena visibilità');
  }

  // Funzione per cambiare sfondo
  function changeBackgroundImage(imageUrl) {
    document.body.style.backgroundImage = `url('${imageUrl}')`;
    console.log('Sfondo cambiato a:', imageUrl);
  }

