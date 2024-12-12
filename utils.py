import re
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup

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
        
        # Find transcript data in page source
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for transcript data in script tags
        scripts = soup.find_all('script')
        transcript_data = None
        
        for script in scripts:
            if script.string and '"captions":' in script.string:
                # Extract caption data
                match = re.search(r'("captions":.+?"captionTracks":.+?])', script.string)
                if match:
                    try:
                        caption_data = '{' + match.group(1) + '}'
                        caption_data = json.loads(caption_data)
                        caption_tracks = caption_data.get('captionTracks', [])
                        
                        if caption_tracks:
                            # Get the first available English transcript or fall back to the first available
                            transcript_url = None
                            for track in caption_tracks:
                                if track.get('languageCode') == 'en':
                                    transcript_url = track.get('baseUrl')
                                    break
                            if not transcript_url:
                                transcript_url = caption_tracks[0].get('baseUrl')
                            
                            if transcript_url:
                                # Get transcript content
                                transcript_response = requests.get(transcript_url)
                                transcript_soup = BeautifulSoup(transcript_response.text, 'xml')
                                
                                # Extract and format transcript text
                                transcript = []
                                for text in transcript_soup.find_all('text'):
                                    transcript.append(text.get_text().strip())
                                
                                return '\n'.join(transcript)
                    except:
                        continue
        
        return None
    except Exception as e:
        raise Exception(f"Failed to extract transcript: {str(e)}")
