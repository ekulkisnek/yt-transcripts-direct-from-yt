import logging
from flask import Flask, render_template, request, jsonify
from utils import extract_transcript, validate_youtube_url

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    try:
        url = request.form.get('url', '').strip()
        
        # Validate YouTube URL
        if not validate_youtube_url(url):
            return jsonify({
                'success': False,
                'error': 'Invalid YouTube URL. Please provide a valid YouTube video URL.'
            })

        # Extract transcript
        transcript = extract_transcript(url)
        
        if not transcript:
            return jsonify({
                'success': False,
                'error': 'Could not extract transcript. The video might not have captions available.'
            })

        return jsonify({
            'success': True,
            'transcript': transcript
        })

    except Exception as e:
        logger.error(f"Error extracting transcript: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while extracting the transcript.'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
