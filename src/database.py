import sqlite3
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional
from config import DATABASE_PATH

class DatabaseManager:
    """Manages SQLite database operations for tracking scraped posts."""
    
    def __init__(self):
        self.db_path = DATABASE_PATH
        self._ensure_db_directory()
        self._init_database()
    
    def _ensure_db_directory(self):
        """Create database directory if it doesn't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _init_database(self):
        """Initialize database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Posts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_url TEXT UNIQUE NOT NULL,
                    profile_url TEXT NOT NULL,
                    title TEXT,
                    description TEXT,
                    price TEXT,
                    image_urls TEXT,  -- JSON string of image URLs
                    post_date TEXT,
                    scraped_date TEXT NOT NULL,
                    downloaded BOOLEAN DEFAULT FALSE,
                    file_paths TEXT  -- JSON string of downloaded file paths
                )
            ''')
            
            # Profiles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_url TEXT UNIQUE NOT NULL,
                    username TEXT,
                    last_checked TEXT,
                    total_posts_found INTEGER DEFAULT 0,
                    active BOOLEAN DEFAULT TRUE
                )
            ''')
            
            # Scraping logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scraping_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    profile_url TEXT,
                    action TEXT,
                    status TEXT,
                    message TEXT
                )
            ''')
            
            conn.commit()
            logging.info("Database initialized successfully")
    
    def add_profile(self, profile_url: str, username: Optional[str] = None) -> bool:
        """Add a new profile to monitor."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO profiles (profile_url, username, last_checked)
                    VALUES (?, ?, ?)
                ''', (profile_url, username, datetime.now().isoformat()))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error adding profile {profile_url}: {e}")
            return False
    
    def get_active_profiles(self) -> List[Dict]:
        """Get all active profiles to monitor."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT profile_url, username, last_checked, total_posts_found
                    FROM profiles WHERE active = TRUE
                ''')
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logging.error(f"Error getting active profiles: {e}")
            return []
    
    def post_exists(self, post_url: str) -> bool:
        """Check if a post has already been scraped."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT 1 FROM posts WHERE post_url = ?', (post_url,))
                return cursor.fetchone() is not None
        except Exception as e:
            logging.error(f"Error checking if post exists: {e}")
            return False
    
    def add_post(self, post_data: Dict) -> bool:
        """Add a new post to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO posts 
                    (post_url, profile_url, title, description, price, image_urls, 
                     post_date, scraped_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    post_data['post_url'],
                    post_data['profile_url'],
                    post_data.get('title', ''),
                    post_data.get('description', ''),
                    post_data.get('price', ''),
                    post_data.get('image_urls', '[]'),
                    post_data.get('post_date', ''),
                    datetime.now().isoformat()
                ))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error adding post: {e}")
            return False
    
    def update_profile_last_checked(self, profile_url: str, posts_count: int = 0):
        """Update when a profile was last checked."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE profiles 
                    SET last_checked = ?, total_posts_found = total_posts_found + ?
                    WHERE profile_url = ?
                ''', (datetime.now().isoformat(), posts_count, profile_url))
                conn.commit()
        except Exception as e:
            logging.error(f"Error updating profile last checked: {e}")
    
    def mark_post_downloaded(self, post_url: str, file_paths: List[str]):
        """Mark a post as downloaded and store file paths."""
        try:
            import json
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE posts 
                    SET downloaded = TRUE, file_paths = ?
                    WHERE post_url = ?
                ''', (json.dumps(file_paths), post_url))
                conn.commit()
        except Exception as e:
            logging.error(f"Error marking post as downloaded: {e}")
    
    def log_scraping_action(self, profile_url: str, action: str, status: str, message: str = ""):
        """Log a scraping action."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO scraping_logs (timestamp, profile_url, action, status, message)
                    VALUES (?, ?, ?, ?, ?)
                ''', (datetime.now().isoformat(), profile_url, action, status, message))
                conn.commit()
        except Exception as e:
            logging.error(f"Error logging scraping action: {e}")
    
    def get_statistics(self) -> Dict:
        """Get scraping statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total posts
                cursor.execute('SELECT COUNT(*) FROM posts')
                total_posts = cursor.fetchone()[0]
                
                # Downloaded posts
                cursor.execute('SELECT COUNT(*) FROM posts WHERE downloaded = TRUE')
                downloaded_posts = cursor.fetchone()[0]
                
                # Active profiles
                cursor.execute('SELECT COUNT(*) FROM profiles WHERE active = TRUE')
                active_profiles = cursor.fetchone()[0]
                
                # Recent activity (last 24 hours)
                cursor.execute('''
                    SELECT COUNT(*) FROM posts 
                    WHERE scraped_date > datetime('now', '-1 day')
                ''')
                recent_posts = cursor.fetchone()[0]
                
                return {
                    'total_posts': total_posts,
                    'downloaded_posts': downloaded_posts,
                    'active_profiles': active_profiles,
                    'recent_posts': recent_posts,
                    'download_percentage': (downloaded_posts / total_posts * 100) if total_posts > 0 else 0
                }
        except Exception as e:
            logging.error(f"Error getting statistics: {e}")
            return {}
