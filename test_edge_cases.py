import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scraper_new import TiseScraper
import json

print("Testing edge cases for post/image count...")

scraper = TiseScraper()

# Test with joy_will_be_sparked (9 posts)
posts = scraper.scrape_profile_posts('https://tise.com/joy_will_be_sparked')

print(f"Profile: joy_will_be_sparked")
print(f"Total posts: {len(posts)}")

# Analyze image counts per post
image_counts = []
for i, post in enumerate(posts):
    image_urls = json.loads(post['image_urls'])
    image_count = len(image_urls)
    image_counts.append(image_count)
    print(f"Post {i+1}: '{post['title'][:30]}...' has {image_count} images")

print(f"\nImage count statistics:")
print(f"Min images per post: {min(image_counts) if image_counts else 0}")
print(f"Max images per post: {max(image_counts) if image_counts else 0}")
print(f"Average images per post: {sum(image_counts)/len(image_counts):.1f}" if image_counts else 0)

# Test empty case (this will likely fail gracefully)
print(f"\nTesting non-existent profile...")
empty_posts = scraper.scrape_profile_posts('https://tise.com/nonexistent_user_12345')
print(f"Non-existent profile posts: {len(empty_posts)}")

scraper.close()

print("\nEdge case testing complete!")
