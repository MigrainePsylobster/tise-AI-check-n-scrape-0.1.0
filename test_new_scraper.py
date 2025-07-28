import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scraper_new import TiseScraper

print("Testing new API-based scraper...")

scraper = TiseScraper()
posts = scraper.scrape_profile_posts('https://tise.com/joy_will_be_sparked')

print(f'Found {len(posts)} posts')

if posts:
    first_post = posts[0]
    print(f'First post: {first_post["title"]}')
    print(f'Price: {first_post["price"]}')
    
    # Parse image URLs
    import json
    image_urls = json.loads(first_post["image_urls"])
    print(f'Images: {len(image_urls)} images')
    print(f'Post URL: {first_post["post_url"]}')
    print(f'Created: {first_post["created_date"]}')
    print(f'Sold: {first_post["is_sold"]}')
    print(f'Category: {first_post["category"]}')
    
    print("\nFirst image URL:")
    if image_urls:
        print(image_urls[0])
else:
    print("No posts found!")

scraper.close()
