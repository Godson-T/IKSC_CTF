document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('theme-toggle');
    const themeText = document.getElementById('theme-text');
    const navbar = document.querySelector('.navbar');

    // Apply theme
    function applyTheme(theme){
        if(theme === 'dark'){
            document.body.classList.add('bg-dark','text-light');
            document.body.classList.remove('bg-light','text-dark');
            navbar.classList.remove('navbar-light','bg-white');
            navbar.classList.add('navbar-dark','bg-dark');
            themeText.textContent = 'Light';
        } else {
            document.body.classList.add('bg-light','text-dark');
            document.body.classList.remove('bg-dark','text-light');
            navbar.classList.remove('navbar-dark','bg-dark');
            navbar.classList.add('navbar-light','bg-white');
            themeText.textContent = 'Dark';
        }
    }

    // Load saved theme or default
    applyTheme(localStorage.getItem('theme') || 'light');

    // Toggle theme
    toggleBtn.addEventListener('click', () => {
        const isDark = document.body.classList.contains('bg-dark');
        const newTheme = isDark ? 'light' : 'dark';
        applyTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    });
});


    // Update icon
    function updateThemeButton() {
        if(document.body.classList.contains('bg-dark')){
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        } else {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        }
    }

    // Toggle theme
    toggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('bg-dark');
        document.body.classList.toggle('text-light');
        document.body.classList.toggle('bg-light');
        document.body.classList.toggle('text-dark');

        const navbar = document.querySelector('.navbar');
        navbar.classList.toggle('navbar-dark');
        navbar.classList.toggle('bg-dark');
        navbar.classList.toggle('navbar-light');
        navbar.classList.toggle('bg-white');

        localStorage.setItem('theme', document.body.classList.contains('bg-dark') ? 'dark' : 'light');

        // Smooth icon rotation
        themeIcon.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            themeIcon.style.transform = 'rotate(0deg)';
            updateThemeButton();
        }, 300);
    });