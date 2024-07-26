const form = document.getElementById('settings-form');
const responseLengthSlider = document.getElementById('response-length');
const responseLengthOutput = document.querySelector('output[for="response-length"]');
const themeSelect = document.getElementById('theme');

// Update the response length output text
responseLengthSlider.addEventListener('input', function() {
    const value = this.value;
    let text;
    switch(value) {
        case '1': text = 'Very Short'; break;
        case '2': text = 'Short'; break;
        case '3': text = 'Medium'; break;
        case '4': text = 'Long'; break;
        case '5': text = 'Very Long'; break;
    }
    responseLengthOutput.textContent = text;
});

// Theme changing functionality
function setTheme(theme) {
    if (theme === 'auto') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.body.className = prefersDark ? 'dark-theme' : 'light-theme';
    } else {
        document.body.className = theme + '-theme';
    }
}

// Initialize theme
setTheme(themeSelect.value);

// Listen for theme changes
themeSelect.addEventListener('change', function() {
    setTheme(this.value);
});

// Listen for system theme changes if auto is selected
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (themeSelect.value === 'auto') {
        setTheme('auto');
    }
});

// Handle form submission
form.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(form);
    const settings = Object.fromEntries(formData.entries());
    
    // Here you would typically send these settings to a server
    console.log('Settings saved:', settings);

    // Simulate saving and return to the main chat interface
    alert('Settings saved successfully!');
    window.history.back();
});