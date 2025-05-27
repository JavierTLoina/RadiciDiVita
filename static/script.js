document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.add("loaded");
});

document.addEventListener("DOMContentLoaded", () => {
  const words = document.querySelectorAll(".word");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      } else {
        entry.target.classList.remove("visible");
      }
    });
  }, {
    threshold: 0.5, // Qué porcentaje del elemento debe estar visible
    rootMargin: "-30% 0% -10% 30%" // "Zona activa" más estrecha (parte media de la pantalla)
  });

  words.forEach(word => observer.observe(word));
});

const hamburger = document.getElementById('hamburger');
const sideMenu = document.getElementById('sideMenu');

hamburger.addEventListener('click', (e) => {
    e.stopPropagation(); 
    const isMenuOpen = sideMenu.style.right === '0px';
    sideMenu.style.right = isMenuOpen ? '-250px' : '0px';
});

document.addEventListener('click', (e) => {
    const isClickInsideMenu = sideMenu.contains(e.target);
    const isClickOnHamburger = hamburger.contains(e.target);

    if (!isClickInsideMenu && !isClickOnHamburger) {
        sideMenu.style.right = '-250px';
    }
});






