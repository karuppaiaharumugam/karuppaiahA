// theme.js
document.addEventListener('DOMContentLoaded', () => {
    // 1. Initial Load & Apply Theme
    const applyTheme = (theme) => {
        if (theme === 'light') {
            document.body.classList.remove('dark');
            document.body.classList.add('light');
            document.documentElement.setAttribute('data-theme', 'light');
        } else {
            // Default to dark
            document.body.classList.remove('light');
            document.body.classList.add('dark');
            document.documentElement.setAttribute('data-theme', 'dark');
        }

        // Specifically for TradingView graphs if they exist
        if (typeof loadCharts === 'function') {
            loadCharts(theme === 'light' ? 'light' : 'dark');
        }

        // Sync toggle button state if checkboxes are used
        const checkbox = document.querySelector('.theme-switch input[type="checkbox"]');
        if (checkbox) {
            checkbox.checked = theme === 'light';
        }
    };

    const savedTheme = localStorage.getItem('global-theme') || 'dark';
    applyTheme(savedTheme);

    // 2. Attach toggle behavior globally to any buttons with class 'btn-theme-toggle'
    window.toggleGlobalTheme = function () {
        const isDark = document.body.classList.contains('dark');
        const newTheme = isDark ? 'light' : 'dark';

        localStorage.setItem('global-theme', newTheme);
        applyTheme(newTheme);
    };

    // If there is an explicit checkbox
    const themeCheckbox = document.querySelector('.theme-switch input[type="checkbox"]');
    if (themeCheckbox) {
        themeCheckbox.addEventListener('change', (e) => {
            const newTheme = e.target.checked ? 'light' : 'dark';
            localStorage.setItem('global-theme', newTheme);
            applyTheme(newTheme);
        });
    }

    // 3. Sync between tabs
    window.addEventListener('storage', (e) => {
        if (e.key === 'global-theme') {
            applyTheme(e.newValue);
        }
    });

    // Setup Socket.IO Live Data stream (if socket.io is included)
    if (typeof io !== 'undefined') {
        const socket = io('http://localhost:5000'); // Assuming Node.js server is at port 5000

        socket.on('connect', () => {
            console.log('Connected to real-time price server.');
        });

        socket.on('price_update', (data) => {
            // Update UI dynamically if elements present
            const liveGoldElem = document.getElementById('live-gold-price');
            const liveSilverElem = document.getElementById('live-silver-price');

            if (liveGoldElem && data.gold) liveGoldElem.innerText = `$${parseFloat(data.gold).toFixed(2)}`;
            if (liveSilverElem && data.silver) liveSilverElem.innerText = `$${parseFloat(data.silver).toFixed(2)}`;

            // Visual highlight logic on change
            const animateUpdate = (elem) => {
                elem.style.color = '#32cd32'; // Green flash
                setTimeout(() => {
                    elem.style.color = ''; // Back to theme
                }, 1000);
            };

            if (liveGoldElem && data.gold) animateUpdate(liveGoldElem);
            if (liveSilverElem && data.silver) animateUpdate(liveSilverElem);
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from real-time server.');
        });
    }
});
