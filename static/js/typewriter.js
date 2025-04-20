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

    // Animate item buttons and descriptions if typewriter effect is enabled
    if (typewriterEnabled) {
        // For each item-buttons container (take, use, drop)
        document.querySelectorAll('.item-buttons').forEach(container => {
            // Only animate if data-typewriter is true
            if (container.dataset.typewriter === 'true') {
                const localDelay = parseFloat(container.dataset.charDelay || '0') * 1000;
                const actions = Array.from(container.querySelectorAll('.item-action'));
                actions.forEach((actionDiv, idx) => {
                    actionDiv.style.opacity = '0';
                    setTimeout(() => {
                        actionDiv.style.transition = 'opacity 0.7s'; // longer transition
                        actionDiv.style.opacity = '1';
                        // Animate the description text inside the item-action
                        const desc = actionDiv.querySelector('.item-description');
                        if (desc && desc.textContent && desc.textContent.length > 0) {
                            const fullText = desc.textContent;
                            desc.textContent = '';
                            let j = 0;
                            function typeDesc() {
                                if (j < fullText.length) {
                                    desc.textContent += fullText.charAt(j);
                                    j++;
                                    setTimeout(typeDesc, localDelay);
                                }
                            }
                            typeDesc();
                        }
                    }, idx * 250 + 200); // Stagger appearance, 250ms per item, slight initial delay
                });
            }
        });
    }
});
