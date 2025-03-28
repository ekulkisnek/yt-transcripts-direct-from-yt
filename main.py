import logging
import requests
from flask import Flask, render_template, request, jsonify
from utils import extract_transcript, validate_youtube_url

# Venice API configuration
VENICE_API_KEY = 'es-6Kh8w7VEnnX7rpCzm7lVlnGb-J8AgGX1tcOC0d9'
VENICE_API_URL = 'https://api.venice.ai/api/v1/chat/completions'
SYSTEM_PROMPT = '''Create a comprehensive outline of the source material, comprised entirely of direct quotes that convey all key information, facts, and evidence in the same order as the original. Correct any transcription errors and condense quotes to remove unnecessary words or phrases, using ellipses (...) to indicate omissions. Ensure that the outline is concise and focused on providing new insights, omitting any information that is redundant, repetitive, or does not add significant value to the understanding of the topic. Remove any quotes that do not provide unique perspectives, findings, or data, and prioritize quotes that convey the author's main arguments, claims, and conclusions. The resulting outline should be a standalone document that can serve as a replacement for the original source material, with the quotes providing a clear and detailed understanding of the content.'''

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

@app.route('/generate-outline', methods=['POST'])
def generate_outline():
    try:
        text = request.json.get('text')
        if not text:
            return jsonify({
                'success': False,
                'error': 'No text provided for outline generation.'
            })

        # Call Venice API with detailed logging
        headers = {
            'Authorization': f'Bearer {VENICE_API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': 'most_intelligent',
            'messages': [
                {
                    'role': 'system',
                    'content': SYSTEM_PROMPT
                },
                {
                    'role': 'user',
                    'content': text
                }
            ],
            'temperature': 0.7,
            'venice_parameters': {
                'include_venice_system_prompt': False
            }
        }
        
        logger.debug(f"Making request to Venice API: {VENICE_API_URL}")
        response = requests.post(VENICE_API_URL, headers=headers, json=payload)
        
        try:
            data = response.json()
            logger.debug(f"Venice API response status: {response.status_code}")
            logger.debug(f"Venice API response data: {data}")
            
            if response.status_code != 200:
                error_msg = data.get('error', {}).get('message', 'Unknown error from Venice API')
                logger.error(f"Venice API error: {error_msg}")
                raise ValueError(error_msg)
            
            if not data.get('choices'):
                raise ValueError('No choices in Venice API response')
                
            message = data['choices'][0].get('message', {})
            if not message or not message.get('content'):
                raise ValueError('No content in Venice API response')
                
            outline = message['content']
            return jsonify({
                'success': True,
                'outline': outline
            })

        except requests.RequestException as e:
            logger.error(f"Venice API request failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to communicate with Venice API.'
            })
        except Exception as e:
            logger.error(f"Error generating outline: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e) if str(e) else 'An error occurred while generating the outline.'
            })

    except Exception as e:
        logger.error(f"Error in generate_outline: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred.'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
