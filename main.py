#!/usr/bin/env python3
"""
Tise.com Profile Scraper
Main application entry point for monitoring Tise profiles and downloading new posts.
"""

import sys
import time
import signal
import logging
import schedule
from datetime import datetime
from typing import List

# Add src to path for imports
sys.path.append('src')

from config import (
    PROFILES_TO_MONITOR, 
    CHECK_INTERVAL_MINUTES, 
    REQUEST_DELAY_SECONDS,
    DOWNLOADS_FOLDER, 
    DATABASE_PATH, 
    LOGS_FOLDER
)
from database import DatabaseManager
from scraper_new import TiseScraper
from downloader import FileDownloader

class TiseMonitor:
    """Main application class for monitoring Tise profiles."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.scraper = TiseScraper()
        self.downloader = FileDownloader()
        self.running = True
        self._setup_logging()
        self._setup_signal_handlers()
        
    def _setup_logging(self):
        """Setup logging configuration."""
        import os
        os.makedirs(LOGS_FOLDER, exist_ok=True)
        
        log_filename = f"{LOGS_FOLDER}/tise_scraper_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        logging.info("=== Tise Monitor Started ===")
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logging.info(f"Received signal {signum}, shutting down gracefully...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def initialize_profiles(self):
        """Initialize profiles from config."""
        if not PROFILES_TO_MONITOR:
            logging.warning("No profiles configured in PROFILES_TO_MONITOR")
            return
        
        for profile_url in PROFILES_TO_MONITOR:
            profile_url = profile_url.strip()
            if profile_url:
                self.db.add_profile(profile_url)
                logging.info(f"Added profile to monitor: {profile_url}")
    
    def check_all_profiles(self):
        """Check all active profiles for new posts."""
        try:
            logging.info("Starting profile check cycle...")
            
            profiles = self.db.get_active_profiles()
            if not profiles:
                logging.warning("No active profiles to monitor")
                return
            
            total_new_posts = 0
            
            for profile in profiles:
                try:
                    profile_url = profile['profile_url']
                    logging.info(f"Checking profile: {profile_url}")
                    
                    # Check for new posts
                    new_posts = self.scraper.check_for_new_posts(profile_url)
                    
                    if new_posts:
                        logging.info(f"Found {len(new_posts)} new posts from {profile_url}")
                        
                        # Download content for new posts
                        for post in new_posts:
                            try:
                                downloaded_files = self.downloader.download_post_content(post)
                                if downloaded_files:
                                    logging.info(f"Downloaded {len(downloaded_files)} files for: {post['title']}")
                                else:
                                    logging.warning(f"Failed to download content for: {post['title']}")
                            except Exception as e:
                                logging.error(f"Error downloading post {post['post_url']}: {e}")
                    
                    total_new_posts += len(new_posts)
                    
                    # Add delay between profiles
                    time.sleep(REQUEST_DELAY_SECONDS)
                    
                except Exception as e:
                    logging.error(f"Error checking profile {profile.get('profile_url', 'unknown')}: {e}")
            
            logging.info(f"Profile check cycle completed. Found {total_new_posts} new posts total.")
            
        except Exception as e:
            logging.error(f"Error in check_all_profiles: {e}")
    
    def print_statistics(self):
        """Print current statistics."""
        try:
            db_stats = self.db.get_statistics()
            download_stats = self.downloader.get_download_statistics()
            
            print("\\n" + "="*50)
            print("TISE MONITOR STATISTICS")
            print("="*50)
            print(f"Active Profiles: {db_stats.get('active_profiles', 0)}")
            print(f"Total Posts Found: {db_stats.get('total_posts', 0)}")
            print(f"Downloaded Posts: {db_stats.get('downloaded_posts', 0)}")
            print(f"Recent Posts (24h): {db_stats.get('recent_posts', 0)}")
            print(f"Download Success Rate: {db_stats.get('download_percentage', 0):.1f}%")
            print(f"Total Files Downloaded: {download_stats.get('total_files', 0)}")
            print(f"Total Download Size: {download_stats.get('total_size_mb', 0):.1f} MB")
            print(f"Downloads Folder: {download_stats.get('downloads_folder', 'N/A')}")
            print("="*50 + "\\n")
            
        except Exception as e:
            logging.error(f"Error printing statistics: {e}")
    
    def run_interactive_mode(self):
        """Run in interactive mode with menu."""
        while self.running:
            try:
                print("\\n" + "="*40)
                print("TISE MONITOR - Interactive Mode")
                print("="*40)
                print("1. Check all profiles now")
                print("2. Add new profile")
                print("3. View statistics")
                print("4. Start automatic monitoring")
                print("5. Exit")
                print("-"*40)
                
                choice = input("Choose an option (1-5): ").strip()
                
                if choice == '1':
                    self.check_all_profiles()
                elif choice == '2':
                    self._add_profile_interactive()
                elif choice == '3':
                    self.print_statistics()
                elif choice == '4':
                    self.run_automatic_mode()
                elif choice == '5':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                logging.error(f"Error in interactive mode: {e}")
    
    def _add_profile_interactive(self):
        """Add profile interactively."""
        try:
            profile_url = input("Enter Tise profile URL: ").strip()
            if profile_url:
                if self.db.add_profile(profile_url):
                    print(f"✓ Added profile: {profile_url}")
                    logging.info(f"Added profile interactively: {profile_url}")
                else:
                    print("✗ Profile already exists or error occurred")
            else:
                print("✗ Invalid URL")
        except Exception as e:
            print(f"✗ Error adding profile: {e}")
    
    def run_automatic_mode(self):
        """Run in automatic monitoring mode."""
        try:
            print(f"\\n🚀 Starting automatic monitoring...")
            print(f"⏰ Check interval: {CHECK_INTERVAL_MINUTES} minutes")
            print("⚡ Press Ctrl+C to stop\\n")
            
            # Schedule the monitoring job
            schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(self.check_all_profiles)
            
            # Run initial check
            self.check_all_profiles()
            
            # Main monitoring loop
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute for scheduled jobs
                
        except KeyboardInterrupt:
            logging.info("Automatic monitoring stopped by user")
        except Exception as e:
            logging.error(f"Error in automatic mode: {e}")
    
    def cleanup(self):
        """Clean up resources."""
        try:
            self.scraper.close()
            logging.info("=== Tise Monitor Stopped ===")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

def main():
    """Main entry point."""
    monitor = TiseMonitor()
    
    try:
        # Initialize profiles from config
        monitor.initialize_profiles()
        
        # Check command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == '--auto':
                monitor.run_automatic_mode()
            elif sys.argv[1] == '--check':
                monitor.check_all_profiles()
                monitor.print_statistics()
            elif sys.argv[1] == '--stats':
                monitor.print_statistics()
            else:
                print("Usage: python main.py [--auto|--check|--stats]")
                print("  --auto  : Run in automatic monitoring mode")
                print("  --check : Check all profiles once and exit")
                print("  --stats : Show statistics and exit")
        else:
            # Run interactive mode
            monitor.run_interactive_mode()
            
    except Exception as e:
        logging.error(f"Fatal error: {e}")
    finally:
        monitor.cleanup()

if __name__ == "__main__":
    main()
