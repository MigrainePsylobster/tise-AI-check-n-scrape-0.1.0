# Tise.com Profile Scraper

A Python application for monitoring Tise.com profiles and automatically downloading new posts with images and metadata.

## Features

- 🔍 **Monitor Multiple Profiles**: Track multiple Tise.com user profiles simultaneously
- 🕒 **Scheduled Checking**: Automatically check for new posts at configurable intervals
- 🚫 **Duplicate Prevention**: Skip posts that have already been downloaded
- 📁 **Organized Downloads**: Save images and metadata in organized folder structure
- 💾 **SQLite Database**: Track all posts and download history
- 🔄 **Resume Support**: Continue monitoring after interruptions
- 📊 **Statistics**: View detailed statistics about scraping activity
- 🔧 **Configurable**: Easy configuration through config.py

## Project Structure

```
tise-scraper/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── setup.bat             # Windows setup script
├── src/
│   ├── database.py       # Database operations
│   ├── scraper.py        # Web scraping logic
│   └── downloader.py     # File download handling
├── data/
│   ├── downloads/        # Downloaded files organized by profile/post
│   └── database.db       # SQLite database
└── logs/                 # Application logs
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows (script designed for Windows, but can be adapted for other OS)

### Quick Setup
1. **Run the setup script:**
   ```bash
   setup.bat
   ```

### Manual Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create directories:**
   ```bash
   mkdir data logs data\\downloads
   ```

## Configuration

Edit `config.py` to configure your monitoring settings:

```python
# Add your target Tise profile URLs
PROFILES_TO_MONITOR = [
    "https://tise.com/profiles/username1",
    "https://tise.com/profiles/username2",
]

# Check interval (minutes)
CHECK_INTERVAL_MINUTES = 30

# Other settings...
```

## Usage

### Interactive Mode
Run the application in interactive mode with a menu:
```bash
python main.py
```

### Automatic Mode
Start continuous monitoring:
```bash
python main.py --auto
```

### One-time Check
Check all profiles once and exit:
```bash
python main.py --check
```

### View Statistics
Display current statistics:
```bash
python main.py --stats
```

## How It Works

1. **Profile Monitoring**: The scraper visits each configured Tise profile page
2. **Post Detection**: Identifies individual posts/items on the profile
3. **Duplicate Check**: Compares against database to avoid re-downloading
4. **Content Download**: Downloads images and saves metadata for new posts
5. **Organization**: Saves files in organized folder structure by profile/post
6. **Logging**: Records all activities for monitoring and debugging

## Download Structure

Downloads are organized as follows:
```
data/downloads/
├── username1_post_title_12345678/
│   ├── image_1.jpg
│   ├── image_2.jpg
│   └── metadata.json
├── username2_another_post_87654321/
│   ├── image_1.png
│   └── metadata.json
└── ...
```

Each post folder contains:
- **Images**: All images from the post (jpg, png, gif, webp)
- **metadata.json**: Post information (title, description, price, URLs, dates)

## Database Schema

The SQLite database tracks:
- **posts**: All discovered posts with metadata
- **profiles**: Monitored profiles and check history  
- **scraping_logs**: Detailed activity logs

## Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `PROFILES_TO_MONITOR` | List of profile URLs to monitor | `[]` |
| `CHECK_INTERVAL_MINUTES` | How often to check for new posts | `30` |
| `REQUEST_DELAY_SECONDS` | Delay between HTTP requests | `2` |
| `USE_HEADLESS_BROWSER` | Use headless Chrome for JS-heavy pages | `True` |
| `DOWNLOADS_FOLDER` | Where to save downloaded files | `"data/downloads"` |
| `ENABLE_NOTIFICATIONS` | Enable notifications for new posts | `True` |

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **Chrome Driver Issues**: The script auto-downloads ChromeDriver, but ensure Chrome browser is installed

3. **Permission Errors**: Make sure the script has write permissions to the data and logs folders

4. **Rate Limiting**: If you get blocked, increase `REQUEST_DELAY_SECONDS` in config.py

### Logs

Check the logs folder for detailed information:
- `logs/tise_scraper_YYYYMMDD.log` - Daily log files
- Look for ERROR and WARNING messages for issues

### Database Issues

If database gets corrupted, delete `data/database.db` - it will be recreated automatically.

## Legal and Ethical Considerations

- ⚖️ **Respect Terms of Service**: Review Tise.com's terms of service before use
- 🕒 **Rate Limiting**: Built-in delays to avoid overloading servers
- 🤖 **robots.txt**: Check and respect robots.txt directives
- 📄 **Personal Use**: This tool is intended for personal use only
- 🔒 **Data Privacy**: Be mindful of privacy when downloading content

## Support

This project is designed to be educational and for personal use. Key points:

- The HTML selectors may need updates if Tise.com changes their website structure
- Test with a small number of profiles first
- Monitor logs for any issues
- Respect the website and other users

## License

This project is for educational and personal use only. Users are responsible for complying with all applicable laws and website terms of service.

---

**Note**: This scraper may need updates if Tise.com changes their website structure. The current implementation uses generic selectors that should work with most profile-based content sites, but may require customization for optimal results.
