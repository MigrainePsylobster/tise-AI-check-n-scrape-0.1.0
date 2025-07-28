import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scraper_new import TiseScraper
from downloader import FileDownloader

print("Testing complete scrape + download workflow...")

# Initialize scraper and downloader
scraper = TiseScraper()
downloader = FileDownloader()

# Get new posts (those not already in database)
print("Checking for new posts...")
new_posts = scraper.check_for_new_posts('https://tise.com/joy_will_be_sparked')

print(f"Found {len(new_posts)} new posts to download")

if new_posts:
    # Test download for just the first post
    first_post = new_posts[0]
    print(f"\nDownloading first post: {first_post['title']}")
    
    # Download the post content
    downloaded_files = downloader.download_post_content(first_post)
    
    print(f"Downloaded {len(downloaded_files)} files:")
    for file_path in downloaded_files:
        print(f"  - {file_path}")
        
    # Show folder structure
    print(f"\nFolder structure created:")
    import json
    image_urls = json.loads(first_post['image_urls'])
    print(f"Profile folder: data/downloads/joy_will_be_sparked/")
    print(f"Images folder: data/downloads/joy_will_be_sparked/images/")
    print(f"Metadata folder: data/downloads/joy_will_be_sparked/metadata/")
    print(f"Expected {len(image_urls)} images + 1 metadata file")
    
else:
    print("No new posts found (all already downloaded)")

# Close connections
scraper.close()
print("\nWorkflow test complete!")
