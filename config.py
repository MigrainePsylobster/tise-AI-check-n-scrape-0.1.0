# Tise.com Profile Scraper Configuration

# Profile URLs to monitor (add your target profiles here)
PROFILES_TO_MONITOR = [
    "https://tise.com/eirikstrand96",
    "https://tise.com/joy_will_be_sparked"
    # Example: "https://tise.com/profiles/username2",
]

# Scraping settings
CHECK_INTERVAL_MINUTES = 2  # How often to check for new posts (shortened for testing)
MAX_RETRIES = 3
REQUEST_DELAY_SECONDS = 2  # Delay between requests to be respectful

# File paths
DOWNLOADS_FOLDER = "data/downloads"
DATABASE_PATH = "data/database.db"
LOGS_FOLDER = "logs"
