import re
import json
import html
import logging
import urllib.parse
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def validate_youtube_url(url):
    """Validate YouTube URL format."""
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.netloc not in ['www.youtube.com', 'youtube.com']:
            return False
        
        if parsed.path != '/watch':
            return False
            
        video_id = urllib.parse.parse_qs(parsed.query).get('v')
        if not video_id or len(video_id[0]) != 11:
            return False
            
        return True
    except:
        return False

def extract_transcript(url):
    """Extract transcript from YouTube video page."""
    try:
        # Get video page content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.debug(f"Got response from YouTube with status: {response.status_code}")
        
        # Find transcript data in page source
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for transcript data in script tags
        scripts = soup.find_all('script')
        logging.debug(f"Found {len(scripts)} script tags in the page")
        transcript_data = None
        
        for i, script in enumerate(scripts):
            if script.string and '"captions":' in script.string:
                logging.debug(f"Found script with captions data at index {i}")
                # Extract caption data
                match = re.search(r'(?:"playerCaptionsTracklistRenderer":{"captionTracks":)(.*?)(?:,"audioTracks"|,"translationLanguages")', script.string)
                if match:
                    try:
                        caption_data_str = match.group(1)
                        logging.debug(f"Found caption data: {caption_data_str[:200]}...")  # Log first 200 chars
                        caption_tracks = json.loads(caption_data_str)
                        logging.debug(f"Found {len(caption_tracks)} caption tracks")
                        
                        if caption_tracks:
                            # Get the first available English transcript or fall back to the first available
                            transcript_url = None
                            for track in caption_tracks:
                                if track.get('languageCode') == 'en':
                                    transcript_url = track.get('baseUrl')
                                    logging.debug("Found English caption track")
                                    break
                            if not transcript_url:
                                transcript_url = caption_tracks[0].get('baseUrl')
                                logging.debug("No English track found, using first available track")
                            
                            if transcript_url:
                                # Get transcript content
                                logging.debug("Fetching transcript content from URL")
                                transcript_response = requests.get(transcript_url)
                                transcript_soup = BeautifulSoup(transcript_response.text, 'xml')
                                
                                # Extract and format transcript text
                                transcript = []
                                for text in transcript_soup.find_all('text'):
                                    # Unescape HTML entities like &#39; to proper characters
                                    cleaned_text = html.unescape(text.get_text().strip())
                                    transcript.append(cleaned_text)
                                
                                return '\n'.join(transcript)
                    except Exception as e:
                        logging.error(f"Error processing caption data: {str(e)}")
                        continue
        
        return None
    except Exception as e:
        raise Exception(f"Failed to extract transcript: {str(e)}")
