document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('extractForm');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const transcriptContainer = document.getElementById('transcriptContainer');
    const transcript = document.getElementById('transcript');
    const copyButton = document.getElementById('copyButton');
    const veniceOutlineButton = document.getElementById('veniceOutlineButton');
    const urlInput = document.getElementById('youtubeUrl');
    
    const VENICE_API_KEY = 'es-6Kh8w7VEnnX7rpCzm7lVlnGb-J8AgGX1tcOC0d9';
    const SYSTEM_PROMPT = `Create a comprehensive outline of the source material, comprised entirely of direct quotes that convey all key information, facts, and evidence in the same order as the original. Correct any transcription errors and condense quotes to remove unnecessary words or phrases, using ellipses (...) to indicate omissions. Ensure that the outline is concise and focused on providing new insights, omitting any information that is redundant, repetitive, or does not add significant value to the understanding of the topic. Remove any quotes that do not provide unique perspectives, findings, or data, and prioritize quotes that convey the author's main arguments, claims, and conclusions. The resulting outline should be a standalone document that can serve as a replacement for the original source material, with the quotes providing a clear and detailed understanding of the content.`;

    function showLoading() {
        loading.classList.remove('d-none');
        error.classList.add('d-none');
        transcriptContainer.classList.add('d-none');
    }

    function showError(message) {
        loading.classList.add('d-none');
        error.textContent = message;
        error.classList.remove('d-none');
        transcriptContainer.classList.add('d-none');
    }

    function showTranscript(text) {
        loading.classList.add('d-none');
        error.classList.add('d-none');
        transcriptContainer.classList.remove('d-none');
        transcript.textContent = text;
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const url = urlInput.value.trim();
        if (!url) {
            showError('Please enter a YouTube URL');
            return;
        }

        showLoading();

        try {
            const response = await fetch('/extract', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `url=${encodeURIComponent(url)}`
            });

            const data = await response.json();

            if (data.success) {
                showTranscript(data.transcript);
            } else {
                showError(data.error);
            }
        } catch (err) {
            showError('An error occurred while extracting the transcript. Please try again.');
            console.error('Error:', err);
        }
    });

    copyButton.addEventListener('click', async function() {
        try {
            await navigator.clipboard.writeText(transcript.textContent);
            const originalText = copyButton.innerHTML;
            copyButton.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
            setTimeout(() => {
                copyButton.innerHTML = originalText;
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text:', err);
        }
    });

    // URL validation feedback
    urlInput.addEventListener('input', function() {
        const url = this.value.trim();
        const isValid = url.match(/^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=[\w-]{11})/);
        
        if (url && !isValid) {
            this.setCustomValidity('Please enter a valid YouTube video URL');
        } else {
            this.setCustomValidity('');
        }
    });

    async function generateVeniceOutline(text) {
        try {
            const response = await fetch('/generate-outline', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });

            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Failed to generate outline');
            }

            return data.outline;
        } catch (err) {
            console.error('Error generating outline:', err);
            throw err;
        }
    }

    veniceOutlineButton.addEventListener('click', async function() {
        try {
            const originalText = transcript.textContent;
            if (!originalText) {
                showError('Please extract a transcript first');
                return;
            }

            // Save original text to restore if needed
            const originalTranscript = originalText;
            
            // Show loading state
            const originalButtonText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
            this.disabled = true;
            showLoading();
            error.classList.add('d-none');

            try {
                const outline = await generateVeniceOutline(originalText);
                if (outline) {
                    transcript.textContent = outline;
                    this.innerHTML = '<i class="fas fa-check me-2"></i>Outline Generated';
                } else {
                    throw new Error('Failed to generate outline');
                }
            } catch (err) {
                console.error('Venice API Error:', err);
                transcript.textContent = originalTranscript;  // Restore original text
                throw err;  // Re-throw to be caught by outer try-catch
            }

        } catch (err) {
            showError(err.message || 'Failed to generate outline. Please try again.');
        } finally {
            // Always cleanup
            loading.classList.add('d-none');
            this.innerHTML = '<i class="fas fa-list me-2"></i>Venice Outline';
            this.disabled = false;
        }
    });
});
