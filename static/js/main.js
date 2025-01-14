document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const modeSelect = document.getElementById('mode');
    const basicOptions = document.getElementById('basicOptions');
    const patternOptions = document.getElementById('patternOptions');
    const wordInput = document.getElementById('wordInput');
    const generateBtn = document.getElementById('generate');
    const outputField = document.getElementById('output');
    const copyBtn = document.getElementById('copy');
    const darkModeToggle = document.getElementById('darkModeToggle');
    const strengthMeter = document.getElementById('strengthMeter');
    const strengthText = document.getElementById('strengthText');
    const errorMessage = document.getElementById('error-message');

    // Mode change handler
    modeSelect.addEventListener('change', function() {
        basicOptions.classList.add('hidden');
        patternOptions.classList.add('hidden');
        wordInput.classList.add('hidden');

        switch(this.value) {
            case 'basic':
                basicOptions.classList.remove('hidden');
                break;
            case 'pattern':
                patternOptions.classList.remove('hidden');
                break;
            case 'shuffle':
            case 'replace':
                wordInput.classList.remove('hidden');
                break;
        }
    });

    // Generate password
    generateBtn.addEventListener('click', async function() {
        const mode = modeSelect.value;
        let data = { mode };

        // Reset previous error state
        errorMessage.classList.add('hidden');
        errorMessage.textContent = '';
        outputField.value = '';
        strengthMeter.style.width = '0%';
        strengthText.textContent = '';

        switch(mode) {
            case 'basic':
                data.complexity = document.getElementById('complexity').value;
                data.length = parseInt(document.getElementById('length').value);
                break;
            case 'pattern':
                data.pattern = document.getElementById('pattern').value;
                break;
            case 'shuffle':
            case 'replace':
                data.word = document.getElementById('word').value;
                break;
        }

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.error) {
                errorMessage.textContent = result.error;
                errorMessage.classList.remove('hidden');
                return;
            }

            outputField.value = result.password;
            updateStrengthMeter(result.strength);
        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = 'Error generating password';
            errorMessage.classList.remove('hidden');
        }
    });

    // Copy to clipboard
    copyBtn.addEventListener('click', function() {
        outputField.select();
        document.execCommand('copy');
        
        // Visual feedback
        const originalText = this.textContent;
        this.textContent = 'Copied!';
        setTimeout(() => {
            this.textContent = originalText;
        }, 2000);
    });

    // Dark mode toggle
    darkModeToggle.addEventListener('click', function() {
        document.documentElement.classList.toggle('dark');
        this.textContent = document.documentElement.classList.contains('dark') ? '☀️' : '🌙';
        
        // Save preference
        localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
    });

    // Load dark mode preference
    if (localStorage.getItem('darkMode') === 'true' || 
        (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        darkModeToggle.textContent = '☀️';
    }

    // Update strength meter
    function updateStrengthMeter(strength) {
        strengthMeter.className = 'h-full rounded-full transition-all duration-300';
        strengthText.className = 'text-sm font-medium';
        
        switch(strength) {
            case 'weak':
                strengthMeter.classList.add('strength-weak');
                strengthText.classList.add('strength-text-weak');
                strengthText.textContent = 'Weak';
                break;
            case 'medium':
                strengthMeter.classList.add('strength-medium');
                strengthText.classList.add('strength-text-medium');
                strengthText.textContent = 'Medium';
                break;
            case 'strong':
                strengthMeter.classList.add('strength-strong');
                strengthText.classList.add('strength-text-strong');
                strengthText.textContent = 'Strong';
                break;
        }
    }
});
