import requests
import time
import random
import logging
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
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
    
    def _get_selenium_driver(self):
        """Initialize Selenium WebDriver if needed."""
        if self.driver is None:
            chrome_options = Options()
            if USE_HEADLESS_BROWSER:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument(f'--user-agent={random.choice(USER_AGENTS)}')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(BROWSER_TIMEOUT)
        return self.driver
    
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
    
    def scrape_profile_posts(self, profile_url: str) -> List[Dict]:
        """Scrape posts from a Tise profile page."""
        logging.info(f"Scraping profile: {profile_url}")
        
        try:
            # First try with requests
            response = self._make_request(profile_url)
            if not response:
                # Fallback to Selenium for JavaScript-heavy pages
                return self._scrape_with_selenium(profile_url)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            posts = self._parse_posts_from_soup(soup, profile_url)
            
            # If no posts found with requests, try Selenium
            if not posts:
                logging.info(f"No posts found with requests, trying Selenium for {profile_url}")
                return self._scrape_with_selenium(profile_url)
            
            return posts
            
        except Exception as e:
            logging.error(f"Error scraping profile {profile_url}: {e}")
            return []
    
    def _scrape_with_selenium(self, profile_url: str) -> List[Dict]:
        """Scrape using Selenium WebDriver."""
        try:
            driver = self._get_selenium_driver()
            driver.get(profile_url)
            
            # Wait for posts to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll to load more posts if needed
            self._scroll_to_load_posts(driver)
            
            # Parse the page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            return self._parse_posts_from_soup(soup, profile_url)
            
        except Exception as e:
            logging.error(f"Error scraping with Selenium {profile_url}: {e}")
            return []
    
    def _scroll_to_load_posts(self, driver):
        """Scroll down to load more posts (if infinite scroll)."""
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for _ in range(3):  # Scroll a few times
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def _parse_posts_from_soup(self, soup: BeautifulSoup, profile_url: str) -> List[Dict]:
        """Parse posts from BeautifulSoup object."""
        posts = []
        
        # These selectors need to be updated based on actual Tise.com HTML structure
        # This is a generic approach that will need customization
        post_elements = soup.find_all(['div', 'article'], class_=lambda x: x and ('post' in x.lower() or 'item' in x.lower() or 'product' in x.lower()))
        
        if not post_elements:
            # Try alternative selectors
            post_elements = soup.find_all('a', href=True)
            post_elements = [elem for elem in post_elements if '/post/' in elem.get('href', '') or '/item/' in elem.get('href', '')]
        
        for post_elem in post_elements:
            try:
                post_data = self._extract_post_data(post_elem, profile_url)
                if post_data and post_data['post_url']:
                    posts.append(post_data)
            except Exception as e:
                logging.warning(f"Error parsing post element: {e}")
        
        logging.info(f"Found {len(posts)} posts from {profile_url}")
        return posts
    
    def _extract_post_data(self, post_elem, profile_url: str) -> Optional[Dict]:
        """Extract data from a single post element."""
        try:
            # Extract post URL
            post_url = None
            if post_elem.name == 'a':
                post_url = post_elem.get('href')
            else:
                link = post_elem.find('a', href=True)
                if link:
                    post_url = link.get('href')
            
            if not post_url:
                return None
            
            # Make URL absolute
            if post_url.startswith('/'):
                base_url = f"https://{urlparse(profile_url).netloc}"
                post_url = urljoin(base_url, post_url)
            
            # Extract other data
            title = self._extract_text(post_elem, ['h1', 'h2', 'h3', '.title', '.name'])
            description = self._extract_text(post_elem, ['.description', '.desc', 'p'])
            price = self._extract_text(post_elem, ['.price', '.cost', '.amount'])
            
            # Extract images
            image_urls = []
            img_elements = post_elem.find_all('img', src=True)
            for img in img_elements:
                img_src = img.get('src')
                if img_src:
                    if img_src.startswith('/'):
                        base_url = f"https://{urlparse(profile_url).netloc}"
                        img_src = urljoin(base_url, img_src)
                    image_urls.append(img_src)
            
            return {
                'post_url': post_url,
                'profile_url': profile_url,
                'title': title or 'No title',
                'description': description or '',
                'price': price or '',
                'image_urls': json.dumps(image_urls),
                'post_date': '',  # Could be extracted if available in HTML
            }
            
        except Exception as e:
            logging.warning(f"Error extracting post data: {e}")
            return None
    
    def _extract_text(self, element, selectors: List[str]) -> str:
        """Extract text using multiple possible selectors."""
        for selector in selectors:
            if selector.startswith('.'):
                found = element.find(class_=selector[1:])
            elif selector.startswith('#'):
                found = element.find(id=selector[1:])
            else:
                found = element.find(selector)
            
            if found:
                return found.get_text(strip=True)
        return ''
    
    def check_for_new_posts(self, profile_url: str) -> List[Dict]:
        """Check a profile for new posts and return only new ones."""
        all_posts = self.scrape_profile_posts(profile_url)
        new_posts = []
        
        for post in all_posts:
            if not self.db.post_exists(post['post_url']):
                new_posts.append(post)
                self.db.add_post(post)
                logging.info(f"New post found: {post['title']} - {post['post_url']}")
        
        # Update profile last checked
        self.db.update_profile_last_checked(profile_url, len(all_posts))
        
        if new_posts:
            self.db.log_scraping_action(profile_url, "check_posts", "success", f"Found {len(new_posts)} new posts")
        else:
            self.db.log_scraping_action(profile_url, "check_posts", "success", "No new posts found")
        
        return new_posts
    
    def close(self):
        """Clean up resources."""
        if self.driver:
            self.driver.quit()
        self.session.close()
