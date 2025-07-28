#!/usr/bin/env python3
"""
Quick smoke test for the Tise scraper
"""
import sys
import os
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scraper_new import TiseScraper

def main():
    print("🔍 Running smoke test on your Tise profile...")
    
    scraper = TiseScraper()
    
    try:
        # Test scraping your profile
        posts = scraper.scrape_profile_posts('https://tise.com/eirikstrand96')
        
        print(f"✅ Found {len(posts)} posts on your profile")
        
        if posts:
            print("\n📋 First 3 posts:")
            for i, post in enumerate(posts[:3]):
                images = len(json.loads(post['image_urls']))
                print(f"  {i+1}. \"{post['title']}\" - {post['price']} - {images} images")
        else:
            print("ℹ️  No posts found (this could be normal if your profile is private or empty)")
            
    except Exception as e:
        print(f"❌ Error during smoke test: {e}")
        return False
    
    finally:
        scraper.close()
    
    print("\n🎉 Smoke test completed!")
    return True

if __name__ == "__main__":
    main()
