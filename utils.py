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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.debug(f"Got response from YouTube with status: {response.status_code}")
        logging.debug(f"Response headers: {dict(response.headers)}")
        
        if 'content-type' in response.headers:
            logging.debug(f"Content-Type: {response.headers['content-type']}")
        
        # Find transcript data in page source
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for transcript data in script tags
        scripts = soup.find_all('script')
        logging.debug(f"Found {len(scripts)} script tags in the page")
        transcript_data = None
        
        for i, script in enumerate(scripts):
            if not script.string:
                continue
            
            script_content = script.string
            
            # Try different patterns for finding caption data
            patterns = [
                r'(?:"playerCaptionsTracklistRenderer":{"captionTracks":)(.*?)(?:,"audioTracks"|,"translationLanguages")',
                r'(?:"captions":{[^}]*"playerCaptionsTracklistRenderer":{[^}]*"captionTracks":)(.*?)(?:]}|},")',
                r'"captionTracks":(.*?)(?:,"audioTracks"|,"translationLanguages"|,"isTranslatable")',
                r'(?:"captionTracks":)(.*?)(?:,"translationLanguages"|,"audioTracks"|,"isTranslatable")',
                r'"captions":\{"playerCaptionsTracklistRenderer":\{"captionTracks":(.*?),',
                r'captionTracks":\[(.*?)\]',
                r'"captions":({[^}]*"captionTracks":\[.*?\]})',
                r'playerCaptionsTracklistRenderer":({"captionTracks":.*?})'
            ]
            
            # Log the total size of the script content for debugging
            logging.debug(f"Total script size: {len(script_content)} characters")
            
            # Look for indicators of caption data
            indicators = ['"captionTracks"', 'playerCaptionsTracklistRenderer', 'timedtext']
            for indicator in indicators:
                if indicator in script_content:
                    logging.debug(f"Found caption indicator: {indicator}")
            
            # Log some context about the script content
            content_preview = script_content[:200] if len(script_content) > 200 else script_content
            logging.debug(f"Analyzing script {i} content preview: {content_preview}")
            
            for pattern in patterns:
                logging.debug(f"Trying pattern: {pattern}")
                match = re.search(pattern, script_content)
                if match:
                    logging.debug(f"Found script with captions data at index {i} using pattern: {pattern}")
                    try:
                        caption_data_str = match.group(1)
                        logging.debug(f"Found caption data: {caption_data_str[:200]}...")  # Log first 200 chars
                        # Try to parse the caption data as JSON
                        try:
                            caption_tracks = json.loads(caption_data_str)
                            if isinstance(caption_tracks, list) and len(caption_tracks) > 0:
                                logging.debug(f"Successfully parsed caption data, found {len(caption_tracks)} tracks")
                            else:
                                logging.debug("Parsed caption data but found no tracks, continuing search...")
                                continue
                            logging.debug(f"Found {len(caption_tracks)} caption tracks")
                        except json.JSONDecodeError as e:
                            logging.error(f"Failed to parse caption data as JSON: {str(e)}")
                            continue
                        
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
                                try:
                                    # Get transcript content
                                    logging.debug(f"Fetching transcript content from URL: {transcript_url}")
                                    transcript_response = requests.get(transcript_url, headers=headers)
                                    transcript_response.raise_for_status()
                                    
                                    # Try different parsing approaches
                                    transcript = []
                                    try:
                                        # First try XML parser
                                        transcript_soup = BeautifulSoup(transcript_response.text, 'xml')
                                        texts = transcript_soup.find_all('text')
                                        
                                        if texts:
                                            for text in texts:
                                                cleaned_text = html.unescape(text.get_text().strip())
                                                if cleaned_text:  # Only add non-empty lines
                                                    transcript.append(cleaned_text)
                                        else:
                                            # Fallback to HTML parser if XML structure not found
                                            transcript_soup = BeautifulSoup(transcript_response.text, 'html.parser')
                                            texts = transcript_soup.find_all('text') or transcript_soup.find_all(class_='caption-line')
                                            
                                            for text in texts:
                                                cleaned_text = html.unescape(text.get_text().strip())
                                                if cleaned_text:  # Only add non-empty lines
                                                    transcript.append(cleaned_text)
                                    except Exception as parse_error:
                                        logging.error(f"Error parsing transcript content: {str(parse_error)}")
                                        # Try raw text extraction if parsing fails
                                        raw_text = transcript_response.text
                                        if '"text":' in raw_text:
                                            try:
                                                # Try to extract text from JSON-like structure
                                                text_matches = re.findall(r'"text"\s*:\s*"([^"]+)"', raw_text)
                                                for text in text_matches:
                                                    cleaned_text = html.unescape(text.strip())
                                                    if cleaned_text:
                                                        transcript.append(cleaned_text)
                                            except Exception as e:
                                                logging.error(f"Failed to extract text from raw content: {str(e)}")
                                                raise
                                    
                                    if not transcript:
                                        logging.error("No transcript text found in the response")
                                        return None
                                        
                                    return '\n'.join(transcript)
                                except requests.RequestException as e:
                                    logging.error(f"Failed to fetch transcript URL: {str(e)}")
                                    return None
                                except Exception as e:
                                    logging.error(f"Failed to process transcript content: {str(e)}")
                                    return None
                    except Exception as e:
                        logging.error(f"Error processing caption data: {str(e)}")
                        continue
        
        # If no captions found through patterns, try a more general search
        logging.debug("No captions found with specific patterns, trying general search...")
        for script in scripts:
            if not script.string:
                continue
            if '"baseUrl"' in script.string and ('timedtext' in script.string or 'captions' in script.string):
                logging.debug("Found potential caption data using general search")
                try:
                    # Try to find any URL containing timedtext
                    urls = re.findall(r'"baseUrl":"(https://[^"]+timedtext[^"]+)"', script.string)
                    if urls:
                        logging.debug(f"Found {len(urls)} potential caption URLs")
                        for url in urls:
                            try:
                                url = url.replace('\\u0026', '&')  # Fix escaped characters
                                logging.debug(f"Trying caption URL: {url}")
                                response = requests.get(url, headers=headers)
                                if response.status_code == 200:
                                    soup = BeautifulSoup(response.text, 'xml')
                                    texts = soup.find_all('text')
                                    if texts:
                                        transcript = []
                                        for text in texts:
                                            cleaned_text = html.unescape(text.get_text().strip())
                                            if cleaned_text:
                                                transcript.append(cleaned_text)
                                        if transcript:
                                            return '\n'.join(transcript)
                            except Exception as e:
                                logging.error(f"Error fetching caption URL: {str(e)}")
                                continue
                except Exception as e:
                    logging.error(f"Error in general caption search: {str(e)}")
        
        logging.error("No captions found through any method")
        return None
    except Exception as e:
        logging.error(f"Failed to extract transcript: {str(e)}")
        return None
