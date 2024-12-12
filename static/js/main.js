document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('extractForm');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const transcriptContainer = document.getElementById('transcriptContainer');
    const transcript = document.getElementById('transcript');
    const copyButton = document.getElementById('copyButton');
    const urlInput = document.getElementById('youtubeUrl');

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
});
