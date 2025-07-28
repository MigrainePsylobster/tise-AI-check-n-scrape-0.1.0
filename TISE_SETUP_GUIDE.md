# Tise.com Specific Configuration and Setup Guide

## About Tise.com
Tise is a Norwegian marketplace app for buying and selling second-hand items, particularly popular for clothing and accessories.

## Important Note
**This scraper template needs customization for Tise.com specifically.** The current code uses generic selectors that will need to be adapted to Tise's actual website structure.

## Before You Start

### 1. Analyze Tise.com Structure
You'll need to inspect Tise.com to understand:
- How profile URLs are structured
- How posts/items are displayed on profile pages
- What HTML elements contain the data you want
- Whether the site uses JavaScript loading (may need Selenium)

### 2. Find Profile URLs
Tise profile URLs typically look like:
- `https://tise.com/u/username`
- `https://tise.com/users/username`
- Or similar format

### 3. Test with Browser Developer Tools
1. Open a Tise profile in your browser
2. Press F12 to open Developer Tools
3. Look at the HTML structure of posts/items
4. Note the CSS classes and element types used

## Customization Required

### Update Scraper Selectors
In `src/scraper.py`, you'll need to update the `_parse_posts_from_soup` method with actual Tise.com selectors:

```python
def _parse_posts_from_soup(self, soup: BeautifulSoup, profile_url: str) -> List[Dict]:
    posts = []
    
    # UPDATE THESE SELECTORS FOR TISE.COM:
    # Example - replace with actual Tise selectors
    post_elements = soup.find_all('div', class_='item-card')  # Replace with actual class
    
    for post_elem in post_elements:
        # Extract data using actual Tise HTML structure
        post_url = post_elem.find('a')['href']  # Adapt to actual structure
        title = post_elem.find('h3', class_='item-title').text  # Adapt
        price = post_elem.find('span', class_='price').text  # Adapt
        # ... etc
```

### Check Authentication Requirements
- Does Tise require login to view profiles?
- Are there rate limits or anti-bot measures?
- Do you need to handle cookies/sessions?

## Sample Tise.com Configuration

Once you've analyzed the site structure, update your `config.py`:

```python
# Example Tise profiles (replace with real URLs)
PROFILES_TO_MONITOR = [
    "https://tise.com/u/fashion_seller_123",
    "https://tise.com/u/vintage_clothes_oslo",
    # Add more profiles here
]

# Tise-specific settings
CHECK_INTERVAL_MINUTES = 15  # Check every 15 minutes
REQUEST_DELAY_SECONDS = 3    # Be respectful - 3 seconds between requests

# May need longer delays for Tise specifically
BROWSER_TIMEOUT = 45
USE_HEADLESS_BROWSER = True
```

## Testing Strategy

### 1. Start Small
- Test with just one profile first
- Check the logs to see what's being detected
- Verify downloads are working correctly

### 2. Inspect Results
```bash
python main.py --check
```
- Look in `data/downloads/` for results
- Check `logs/` for any errors
- Verify metadata.json files contain correct data

### 3. Debugging
If posts aren't being detected:
1. Check the HTML selectors in `_parse_posts_from_soup`
2. Enable debug logging by changing log level to DEBUG
3. Use Selenium mode if the site is JavaScript-heavy

## Legal Considerations for Tise.com

### Terms of Service
- Review Tise.com's terms of service before scraping
- Ensure your use case is acceptable under their terms
- Consider reaching out to Tise if you need higher-volume access

### Rate Limiting
- Tise may have anti-bot measures
- Start with longer delays (5-10 seconds) between requests
- Monitor for any blocking or rate limiting responses

### Content Rights
- Scraped images and content belong to the original sellers
- Be respectful of intellectual property rights
- This tool is for personal use only

## Potential Issues

### JavaScript Loading
If Tise loads content dynamically with JavaScript:
- The scraper will automatically fall back to Selenium
- Make sure Chrome browser is installed
- Consider increasing `BROWSER_TIMEOUT`

### Authentication
If profiles require login:
- You may need to implement login functionality
- Consider using session cookies
- Be aware of account security implications

### Regional Restrictions
Tise may show different content based on location:
- Consider using a Norwegian VPN if accessing from outside Norway
- Be aware of regional privacy laws (GDPR)

## Next Steps

1. **Research Tise.com structure** using browser developer tools
2. **Update the selectors** in `src/scraper.py`
3. **Test with one profile** using `python main.py --check`
4. **Gradually add more profiles** once working
5. **Monitor logs** for any issues or blocks

## Example Workflow

```bash
# 1. Initial setup
setup.bat

# 2. Configure profiles in config.py
# Edit config.py with your target Tise profiles

# 3. Test single run
python main.py --check

# 4. Check results
dir data\downloads
type logs\tise_scraper_*.log

# 5. Start monitoring if working
python main.py --auto
```

Remember: This is a template that requires customization for Tise.com specifically. The actual HTML structure and API endpoints will determine how well it works.
