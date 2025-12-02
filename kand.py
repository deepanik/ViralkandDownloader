import requests
import re
import logging
from urllib.parse import urlparse
from typing import Dict, Tuple, List, Optional
from bs4 import BeautifulSoup

# Setup logging
logger = logging.getLogger(__name__)


def extract_urls(text: str) -> List[str]:
    """
    Extract URLs from text
    
    Args:
        text: The text to extract URLs from
        
    Returns:
        List[str]: List of URLs found in the text
    """
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return urls


def is_valid_viralkand_url(url: str) -> bool:
    """
    Check if the URL is a valid viralkand.com URL format
    
    Args:
        url: The URL to validate
        
    Returns:
        bool: True if URL format is valid, False otherwise
    """
    try:
        parsed = urlparse(url)
        # Check if domain is viralkand.com
        if parsed.netloc.lower() not in ['viralkand.com', 'www.viralkand.com']:
            return False
        # Check if path exists (not just domain)
        if not parsed.path or parsed.path == '/':
            return False
        # URL should have format: viralkand.com/something/
        return True
    except Exception:
        return False


def check_url_exists(url: str, timeout: int = 10) -> Tuple[bool, int, str]:
    """
    Check if the URL exists and is accessible
    
    Args:
        url: The URL to check
        timeout: Request timeout in seconds (default: 10)
        
    Returns:
        Tuple[bool, int, str]: (exists, status_code, message)
            - exists: True if URL is accessible
            - status_code: HTTP status code
            - message: Status message
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
        
        # If HEAD request fails, try GET request
        if response.status_code >= 400:
            response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        
        status_code = response.status_code
        
        # Consider 2xx and 3xx as valid (exists)
        if 200 <= status_code < 400:
            return True, status_code, "URL exists and is accessible"
        elif status_code == 404:
            return False, status_code, "URL not found (404)"
        elif status_code == 403:
            return False, status_code, "Access forbidden (403)"
        else:
            return False, status_code, f"URL returned status code: {status_code}"
            
    except requests.exceptions.Timeout:
        return False, 0, "Request timeout - URL may not be accessible"
    except requests.exceptions.ConnectionError:
        return False, 0, "Connection error - Unable to reach the URL"
    except requests.exceptions.RequestException as e:
        return False, 0, f"Request error: {str(e)}"
    except Exception as e:
        return False, 0, f"Unexpected error: {str(e)}"


def extract_metadata(url: str, timeout: int = 10) -> Dict[str, Optional[str]]:
    """
    Extract metadata (og:title, og:description, og:image, video URL) from URL
    
    Args:
        url: The URL to extract metadata from
        timeout: Request timeout in seconds (default: 10)
        
    Returns:
        Dict with keys:
            - title: str or None - og:title content
            - description: str or None - og:description content
            - image: str or None - og:image content
            - video_url: str or None - contentURL (video URL)
    """
    metadata = {
        'title': None,
        'description': None,
        'image': None,
        'video_url': None
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract og:title
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                metadata['title'] = og_title.get('content')
            
            # Extract og:description
            og_description = soup.find('meta', property='og:description')
            if og_description and og_description.get('content'):
                metadata['description'] = og_description.get('content')
            
            # Extract og:image
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                metadata['image'] = og_image.get('content')
            
            # Extract video URL from contentURL meta tag
            content_url = soup.find('meta', itemprop='contentURL')
            if content_url and content_url.get('content'):
                metadata['video_url'] = content_url.get('content')
        
    except requests.exceptions.Timeout:
        logger.warning(f"Timeout while extracting metadata from {url}")
    except requests.exceptions.RequestException as e:
        logger.warning(f"Error extracting metadata from {url}: {str(e)}")
    except Exception as e:
        logger.warning(f"Unexpected error extracting metadata from {url}: {str(e)}")
    
    return metadata


def validate_and_check_url(url: str, extract_meta: bool = True) -> Dict:
    """
    Complete API function: Validates URL format, checks if it exists, and extracts metadata
    
    Args:
        url: The URL to validate and check
        extract_meta: Whether to extract metadata if URL is valid and exists (default: True)
        
    Returns:
        Dict with keys:
            - valid: bool - Whether URL format is valid
            - exists: bool - Whether URL exists and is accessible
            - status_code: int - HTTP status code (0 if not checked)
            - message: str - Status message
            - url: str - The original URL
            - metadata: Dict - Contains title, description, image (only if valid and exists)
    """
    result = {
        'valid': False,
        'exists': False,
        'status_code': 0,
        'message': '',
        'url': url,
        'metadata': {
            'title': None,
            'description': None,
            'image': None,
            'video_url': None
        }
    }
    
    # Step 1: Validate URL format
    if not is_valid_viralkand_url(url):
        result['message'] = 'Invalid URL format - Must be a viralkand.com URL'
        return result
    
    result['valid'] = True
    
    # Step 2: Check if URL exists
    exists, status_code, message = check_url_exists(url)
    result['exists'] = exists
    result['status_code'] = status_code
    result['message'] = message
    
    # Step 3: Extract metadata if URL is valid and exists
    if exists and extract_meta:
        metadata = extract_metadata(url)
        result['metadata'] = metadata
    
    return result


# Example usage
if __name__ == "__main__":
    # Test the API
    test_url = "https://viralkand.com/devar-ne-diwar-par-jhuka-ke-bhabhi-ki-chut-faad-di/"
    result = validate_and_check_url(test_url)
    print(f"URL: {result['url']}")
    print(f"Valid: {result['valid']}")
    print(f"Exists: {result['exists']}")
    print(f"Status Code: {result['status_code']}")
    print(f"Message: {result['message']}")
    print("\nMetadata:")
    print(f"Title: {result['metadata']['title']}")
    print(f"Description: {result['metadata']['description']}")
    print(f"Image: {result['metadata']['image']}")

