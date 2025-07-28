import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scraper_new import TiseScraper
from downloader import FileDownloader
from database import DatabaseManager
import json

print("Testing duplicate prevention (second run)...")

# Initialize components
scraper = TiseScraper()
downloader = FileDownloader()
db = DatabaseManager()

print("\n=== FIRST CHECK: What's in database already ===")
# Check if posts exist using the DatabaseManager methods
test_post_url = "https://tise.com/t/IzFGdSNcK"  # The "Thrifted kjole" post
exists = db.post_exists(test_post_url)
print(f"Post 'Thrifted kjole' exists in database: {exists}")

# Get database statistics
stats = db.get_statistics()
print(f"Database statistics:")
print(f"  - Total posts: {stats.get('total_posts', 0)}")
print(f"  - Downloaded posts: {stats.get('downloaded_posts', 0)}")
print(f"  - Active profiles: {stats.get('active_profiles', 0)}")

print("\n=== SECOND CHECK: Check for new posts ===")
# This should find NO new posts since we just scraped them
new_posts = scraper.check_for_new_posts('https://tise.com/joy_will_be_sparked')

print(f"New posts found: {len(new_posts)}")

if new_posts:
    print("⚠️ WARNING: Found new posts (unexpected!):")
    for post in new_posts:
        print(f"  - {post['title']}")
else:
    print("✅ SUCCESS: No new posts found (all already in database)")

print("\n=== THIRD CHECK: Verify specific post exists ===")
# Check if the "Thrifted kjole" post is marked as existing
test_post_url = "https://tise.com/t/IzFGdSNcK"
exists = db.post_exists(test_post_url)
print(f"Post 'Thrifted kjole' exists in database: {exists}")

print("\n=== FOURTH CHECK: Manual scrape (should still work) ===")
# Direct scrape should still work, but check_for_new_posts should filter duplicates
all_posts = scraper.scrape_profile_posts('https://tise.com/joy_will_be_sparked')
print(f"Total posts from API: {len(all_posts)}")
print("But new_posts should be 0 because they're all in database already")

# Close connections
scraper.close()

print("\nDuplicate prevention test complete!")
