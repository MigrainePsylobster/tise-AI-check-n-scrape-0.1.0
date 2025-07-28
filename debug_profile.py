#!/usr/bin/env python3
"""
Debug script for analyzing nelliekrokstad profile
"""
import sys
import json
sys.path.append('src')

from scraper_new import TiseScraper

def debug_profile(username):
    print(f'🔍 Debugging {username} profile...')
    print()

    scraper = TiseScraper()

    # Step 1: Get user ID
    print('Step 1: Getting user ID...')
    user_id = scraper.get_user_id_from_username(username)
    print(f'User ID: {user_id}')
    print()

    if user_id:
        # Step 2: Test API endpoint
        print('Step 2: Testing API endpoint...')
        api_url = f'https://tise.com/api/user/{user_id}/tises?sort=sold.asc'
        print(f'API URL: {api_url}')
        
        response = scraper._make_request(api_url)
        if response:
            data = response.json()
            print('✅ API response received')
            print(f'Response keys: {list(data.keys())}')
            print(f'Results count: {len(data.get("results", []))}')
            print(f'Next page: {data.get("next")}')
            print()

            # Step 3: Check if there are results
            results = data.get('results', [])
            if results:
                print('Step 3: Analyzing first few posts...')
                for i, post in enumerate(results[:3]):
                    print(f'Post {i+1}:')
                    print(f'  ID: {post.get("id")}')
                    print(f'  Title: {post.get("title", "No title")}')
                    print(f'  Sold: {post.get("sold", False)}')
                    print(f'  Created: {post.get("createdAt", "Unknown")}')
                    print(f'  Images: {len(post.get("imageSets", []))}')
                    print()
                    
                # Step 4: Check for pagination
                if data.get('next'):
                    print('Step 4: Testing pagination...')
                    next_response = scraper._make_request(data.get('next'))
                    if next_response:
                        next_data = next_response.json()
                        print(f'Next page results: {len(next_data.get("results", []))}')
                        print(f'Next page has more: {next_data.get("next") is not None}')
                    else:
                        print('❌ Failed to get next page')
                else:
                    print('Step 4: No pagination - all posts in first response')
                    
            else:
                print('❌ No results found in API response')
                print('Full response:')
                print(json.dumps(data, indent=2)[:500] + '...')
                
            # Step 5: Test different sorting/filtering
            print()
            print('Step 5: Testing different API parameters...')
            test_urls = [
                f'https://tise.com/api/user/{user_id}/tises',  # No sorting
                f'https://tise.com/api/user/{user_id}/tises?sort=created_at.desc',  # Newest first
                f'https://tise.com/api/user/{user_id}/tises?limit=50',  # Higher limit
            ]
            
            for test_url in test_urls:
                print(f'Testing: {test_url}')
                test_response = scraper._make_request(test_url)
                if test_response:
                    test_data = test_response.json()
                    print(f'  Results: {len(test_data.get("results", []))}')
                else:
                    print('  ❌ Failed')
                    
        else:
            print('❌ Failed to get API response')
    else:
        print('❌ Could not get user ID')

    scraper.close()

if __name__ == "__main__":
    debug_profile('nelliekrokstad')
