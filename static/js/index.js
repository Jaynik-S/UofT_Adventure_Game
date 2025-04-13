document.addEventListener('DOMContentLoaded', function() {
    const radioButtons = document.querySelectorAll('input[name="typewriter_effect"]');
    const applyButton = document.getElementById('apply-typewriter');
    const introSection = document.getElementById('intro-section');
    const startForm = document.getElementById('start-form');
    const finalEffectType = document.getElementById('final-effect-type');
    const finalDelayValue = document.getElementById('final-delay-value');
    
    // Initial text content
    const welcomeTitle = document.getElementById('welcome-title');
    const selectExperience = document.getElementById('select-experience');
    const chooseStory = document.getElementById('choose-story');
    const typewriterLabel = document.getElementById('typewriter-label');
    
    // Set the text content for elements
    welcomeTitle.dataset.originalText = "Welcome to A UofT Adventure Game";
    selectExperience.dataset.originalText = "Select Your Experience";
    chooseStory.dataset.originalText = "Choose how you'd like the story to be revealed:";
    typewriterLabel.dataset.originalText = "Typewriter Effect:";
    
    // Function to apply typewriter effect to an element
    function applyTypewriterToElement(element, callback) {
        const text = element.dataset.originalText;
        element.textContent = '';
        let i = 0;
        
        function typeText() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typeText, 0.03 * 1000);
            } else if (callback) {
                callback();
            }
        }
        
        typeText();
    }
    
    // Type each element in sequence
    applyTypewriterToElement(welcomeTitle, function() {
        // Show typewriter selection after welcome title is typed
        document.getElementById('typewriter-selection').classList.remove('hidden');
        
        // Continue with remaining elements
        applyTypewriterToElement(selectExperience, function() {
            applyTypewriterToElement(chooseStory, function() {
                applyTypewriterToElement(typewriterLabel);
            });
        });
    });
    
    // Handle radio button changes
    radioButtons.forEach(function(radio) {
        radio.addEventListener('change', function() {
            // Enable/disable the hidden input for the selected option
            document.querySelectorAll('.speed-option input[type="hidden"]').forEach(function(input) {
                input.disabled = true;
            });
            
            if (this.value === 'yes') {
                const hiddenInput = this.parentNode.querySelector('input[type="hidden"]');
                if (hiddenInput) {
                    hiddenInput.disabled = false;
                }
            }
        });
    });
    
    // Handle Apply button click
    applyButton.addEventListener('click', function() {
        // Get selected typewriter effect
        const selectedRadio = document.querySelector('input[name="typewriter_effect"]:checked');
        const isTypewriterEffect = selectedRadio.value === 'yes';
        let charDelay = 0;
        
        if (isTypewriterEffect) {
            const hiddenInput = selectedRadio.parentNode.querySelector('input[type="hidden"]');
            charDelay = parseFloat(hiddenInput.value);
        }
        
        // Set values for the form submission
        finalEffectType.value = isTypewriterEffect ? 'yes' : 'no';
        finalDelayValue.value = charDelay;
        
        // Hide the typewriter selection
        document.getElementById('typewriter-selection').classList.add('hidden');
        
        // Prepare paragraphs for typewriter effect
        const paragraphs = introSection.querySelectorAll('p');
        
        if (isTypewriterEffect) {
            // Store original text and clear content BEFORE showing the section
            paragraphs.forEach(paragraph => {
                // Store original text in data attribute
                paragraph.dataset.originalText = paragraph.textContent;
                // Clear the text so it's not visible when intro section appears
                paragraph.textContent = '';
            });
        }
        
        // Now show the intro section (with empty paragraphs if typewriter effect is on)
        introSection.classList.remove('hidden');
        
        // Apply typewriter effect if selected
        if (isTypewriterEffect) {
            let paragraphIndex = 0;
            
            function typeNextParagraph() {
                if (paragraphIndex < paragraphs.length) {
                    const paragraph = paragraphs[paragraphIndex];
                    const text = paragraph.dataset.originalText;
                    let charIndex = 0;
                    
                    function typeWriter() {
                        if (charIndex < text.length) {
                            paragraph.textContent += text.charAt(charIndex);
                            charIndex++;
                            setTimeout(typeWriter, charDelay * 1000);
                        } else {
                            paragraphIndex++;
                            setTimeout(typeNextParagraph, 100); // Small delay between paragraphs
                        }
                    }
                    
                    typeWriter();
                } else {
                    // Show start button after all paragraphs are typed
                    startForm.classList.remove('hidden');
                }
            }
            
            typeNextParagraph();
        } else {
            // Show start button immediately if no typewriter effect
            startForm.classList.remove('hidden');
        }
    });
});
