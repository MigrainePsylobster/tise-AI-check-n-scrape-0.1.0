# Tise.com Profile Scraper Configuration

# Profile URLs to monitor (add your target profiles here)
PROFILES_TO_MONITOR = [
    "https://tise.com/joy_will_be_sparked",
    # Example: "https://tise.com/profiles/username2",
]

# Scraping settings
CHECK_INTERVAL_MINUTES = 30  # How often to check for new posts
MAX_RETRIES = 3
REQUEST_DELAY_SECONDS = 2  # Delay between requests to be respectful

# File paths
DOWNLOADS_FOLDER = "data/downloads"
DATABASE_PATH = "data/database.db"
LOGS_FOLDER = "logs"

# Browser settings (for Selenium if needed)
USE_HEADLESS_BROWSER = True
BROWSER_TIMEOUT = 30

# User agent for requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

# Notification settings
ENABLE_NOTIFICATIONS = True
NOTIFICATION_SOUND = True
