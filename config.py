# Tise.com Profile Scraper Configuration

# Profile URLs to monitor (add your target profiles here)
# use # to comment out unused profiles
PROFILES_TO_MONITOR = [
    "https://tise.com/profiles/username1",
    "https://tise.com/profiles/username2"
   # "https://tise.com/profiles/username3",
   # "https://tise.com/profiles/username4"
]

# Scraping settings
CHECK_INTERVAL_MINUTES = 2  # How often to check for new posts (shortened for testing)
MAX_RETRIES = 3
REQUEST_DELAY_SECONDS = 2  # Delay between requests to be respectful

# File paths
DOWNLOADS_FOLDER = "data/downloads"
DATABASE_PATH = "data/database.db"
LOGS_FOLDER = "logs"
