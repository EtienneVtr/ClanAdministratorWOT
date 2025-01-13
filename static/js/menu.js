document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menu-toggle');
    const sideMenu = document.getElementById('side-menu');

    menuToggle.addEventListener('click', () => {
        // Toggle la classe active
        sideMenu.classList.toggle('active');
        menuToggle.classList.toggle('active');

        // Change le symbole (≡ ↔ ✖)
        if (menuToggle.classList.contains('active')) {
            menuToggle.innerHTML = '&times;'; // Symbole de croix
        } else {
            menuToggle.innerHTML = '&#9776;'; // Symbole de menu
        }
    });
});
