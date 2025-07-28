import requests
import time
import random
import logging
import json
from typing import List, Dict, Optional
from datetime import datetime

from config import USER_AGENTS, REQUEST_DELAY_SECONDS, MAX_RETRIES
from database import DatabaseManager

class TiseScraper:
    """API-based scraper class for Tise.com profiles."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.session = requests.Session()
        self._setup_session()
        
    def _setup_session(self):
        """Setup requests session with proper headers for Tise API."""
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en,en;q=0.9',
            'sec-ch-ua-platform': '"Windows"',
            'tise-system-os': 'web',
            'Referer': 'https://tise.com/',
        })
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Make HTTP request with retry logic."""
        for attempt in range(MAX_RETRIES):
            try:
                # Rotate user agent
                self.session.headers['User-Agent'] = random.choice(USER_AGENTS)
                
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                # Add delay to be respectful
                time.sleep(REQUEST_DELAY_SECONDS + random.uniform(0, 1))
                return response
                
            except requests.RequestException as e:
                logging.warning(f"Request attempt {attempt + 1} failed for {url}: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logging.error(f"All request attempts failed for {url}")
                    return None
    
    def get_user_id_from_username(self, username: str) -> Optional[str]:
        """Get internal user ID from username using Tise API."""
        try:
            # Update referer for this specific profile
            self.session.headers['Referer'] = f'https://tise.com/{username}'
            
            api_url = f"https://tise.com/api/users/{username}"
            response = self._make_request(api_url)
            
            if response and response.status_code == 200:
                data = response.json()
                # API returns nested structure: {"result": {"id": "...", "username": "..."}}
                result = data.get('result', {})
                user_id = result.get('id')
                if user_id:
                    logging.info(f"Found user ID {user_id} for username {username}")
                    return user_id
                else:
                    logging.error(f"No user ID found in API response for {username}")
                    logging.debug(f"API response structure: {list(data.keys())}")
            else:
                logging.error(f"Failed to get user info for {username}: Status {response.status_code if response else 'No response'}")
                
        except Exception as e:
            logging.error(f"Error getting user ID for {username}: {e}")
        
        return None
    
    def scrape_profile_posts(self, profile_url: str) -> List[Dict]:
        """Scrape posts from a Tise profile using the API."""
        # Extract username from URL
        username = profile_url.rstrip('/').split('/')[-1]
        logging.info(f"Scraping profile: {username}")
        
        try:
            # Get user ID from username
            user_id = self.get_user_id_from_username(username)
            if not user_id:
                logging.error(f"Could not get user ID for {username}")
                return []
            
            # Get posts using the API
            posts_api_url = f"https://tise.com/api/user/{user_id}/tises?sort=sold.asc"
            response = self._make_request(posts_api_url)
            
            if not response or response.status_code != 200:
                logging.error(f"Failed to get posts for user {username}")
                return []
            
            data = response.json()
            posts_data = data.get('results', [])
            
            # Convert API data to our standard format
            posts = []
            for post_data in posts_data:
                processed_post = self._process_api_post(post_data, profile_url)
                if processed_post:
                    posts.append(processed_post)
            
            logging.info(f"Found {len(posts)} posts for {username}")
            return posts
            
        except Exception as e:
            logging.error(f"Error scraping profile {profile_url}: {e}")
            return []
    
    def _process_api_post(self, api_post: Dict, profile_url: str) -> Optional[Dict]:
        """Convert API post data to our standard format."""
        try:
            post_id = api_post.get('id')
            if not post_id:
                return None
            
            # Extract image URLs from imageSets
            image_urls = []
            for image_set in api_post.get('imageSets', []):
                # Use original quality images
                original_url = image_set.get('original')
                if original_url:
                    image_urls.append(original_url)
            
            # Create post URL
            post_url = f"https://tise.com/t/{api_post.get('a', post_id)}"
            
            # Convert price from øre to NOK (divide by 100)
            price_ore = api_post.get('price', 0)
            price_nok = price_ore / 100 if price_ore else 0
            
            processed_post = {
                'post_id': post_id,
                'post_url': post_url,
                'profile_url': profile_url,
                'title': api_post.get('title', ''),
                'description': api_post.get('caption', ''),
                'price': f"{price_nok:.0f} NOK" if price_nok > 0 else "Not specified",
                'image_urls': json.dumps(image_urls),
                'scraped_date': datetime.now().isoformat(),
                'created_date': api_post.get('createdAt', ''),
                'is_sold': api_post.get('sold', False),
                'category': api_post.get('category', ''),
                'condition': api_post.get('condition', ''),
                'size': api_post.get('productSize', ''),
                'location': self._extract_location(api_post.get('location', {})),
                'colors': self._extract_colors(api_post.get('colors', [])),
                'raw_api_data': json.dumps(api_post)  # Store full API response for debugging
            }
            
            return processed_post
            
        except Exception as e:
            logging.error(f"Error processing post data: {e}")
            return None
    
    def _extract_location(self, location_data: Dict) -> str:
        """Extract location string from API location data."""
        if location_data and isinstance(location_data, dict):
            return location_data.get('label', 'Unknown location')
        return 'Unknown location'
    
    def _extract_colors(self, colors_data: List) -> str:
        """Extract color names from API colors data."""
        if colors_data and isinstance(colors_data, list):
            color_names = [color.get('name', '') for color in colors_data if color.get('name')]
            return ', '.join(color_names) if color_names else 'No colors specified'
        return 'No colors specified'
    
    def check_for_new_posts(self, profile_url: str) -> List[Dict]:
        """Check for new posts that haven't been downloaded yet."""
        try:
            all_posts = self.scrape_profile_posts(profile_url)
            new_posts = []
            
            for post in all_posts:
                if not self.db.post_exists(post['post_url']):
                    new_posts.append(post)
                    # Add to database as discovered
                    self.db.add_post(post)
            
            if new_posts:
                logging.info(f"Found {len(new_posts)} new posts from {profile_url}")
            else:
                logging.info(f"No new posts found from {profile_url}")
            
            return new_posts
            
        except Exception as e:
            logging.error(f"Error checking for new posts from {profile_url}: {e}")
            return []
    
    def close(self):
        """Clean up resources."""
        if hasattr(self, 'session'):
            self.session.close()
        logging.info("TiseScraper closed")
