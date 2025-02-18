// Ses efektleri
const sounds = {
    correct: new Audio('/static/sounds/correct.mp3'),
    wrong: new Audio('/static/sounds/wrong.mp3'),
    success: new Audio('/static/sounds/success.mp3'),
    click: new Audio('/static/sounds/click.mp3')
};

// Ses ayarları
let soundEnabled = localStorage.getItem('soundEnabled') !== 'false';

// Ses kontrolü
function toggleSound() {
    soundEnabled = !soundEnabled;
    localStorage.setItem('soundEnabled', soundEnabled);
    document.getElementById('soundToggle').innerHTML = 
        `<i class="fas fa-volume-${soundEnabled ? 'up' : 'mute'}"></i>`;
}

// Ses çalma fonksiyonu
function playSound(soundName) {
    if (soundEnabled && sounds[soundName]) {
        sounds[soundName].currentTime = 0;
        sounds[soundName].play().catch(() => {});
    }
}

// Alert mesajlarını otomatik kapat
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap alert'lerini otomatik kapat
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Ses toggle butonunu ekle
    const navbar = document.querySelector('.navbar-nav');
    if (navbar) {
        const soundToggle = document.createElement('li');
        soundToggle.className = 'nav-item';
        soundToggle.innerHTML = `
            <button id="soundToggle" class="btn nav-link" onclick="toggleSound()">
                <i class="fas fa-volume-${soundEnabled ? 'up' : 'mute'}"></i>
            </button>
        `;
        navbar.appendChild(soundToggle);
    }
});

// Form doğrulama
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// CSRF token yönetimi
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

// Ajax istekleri için yardımcı fonksiyon
async function fetchWithCSRF(url, options = {}) {
    const defaultOptions = {
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    };
    
    const finalOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(url, finalOptions);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// Animasyon yardımcıları
function addAnimation(element, animationName, duration = 500) {
    element.classList.add(animationName);
    setTimeout(() => {
        element.classList.remove(animationName);
    }, duration);
}

// Responsive image loading
function loadResponsiveImage(img) {
    const src = img.dataset.src;
    if (src) {
        img.src = src;
        img.removeAttribute('data-src');
    }
}

// Lazy loading için Intersection Observer
const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            loadResponsiveImage(entry.target);
            observer.unobserve(entry.target);
        }
    });
});

// Lazy loading uygula
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}); 