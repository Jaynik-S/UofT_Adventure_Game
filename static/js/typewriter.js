document.addEventListener('DOMContentLoaded', function() {
    // Get character delay from the data attribute on body element
    const charDelay = parseFloat(document.body.dataset.charDelay || 0) * 1000; // Convert to milliseconds
    const typewriterEnabled = document.body.dataset.typewriterEnabled === 'true';
    
    if (typewriterEnabled) {
        const typewriterElements = document.querySelectorAll('.typewriter');
        
        typewriterElements.forEach(element => {
            const text = element.textContent;
            element.textContent = '';
            let i = 0;
            
            function typeWriter() {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, charDelay);
                }
            }
            
            typeWriter();
        });
    }
});
