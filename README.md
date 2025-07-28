# 🛍️ ## ✨ Features

- 🎯 **Profile Monitoring**: Track any Tise.com user profile for new posts
- ⏰ **Automatic Checking**: Set custom intervals (default: every 30 minutes)  
- 🚫 **Smart Duplicates**: Never download the same post twice
- 📂 **Perfect Organization**: Files organized by username with descriptive names
- 🖼️ **Enhanced Naming**: `Post Title_UniqueID_ImageNumber.jpg` format
- 🔄 **Auto WebP→JPG**: Automatically converts .webp images to .jpg
- 💾 **SQLite Tracking**: Built-in database tracks everything
- 📊 **Statistics**: View download stats and success rates
- 🔧 **Easy Configuration**: Simple config file setup
- 🚀 **Service Mode**: Easy `run.bat` for continuous monitoringrofile Scraper

**Automatically monitor Tise.com profiles and download new posts with organized file management!**

A Windows-ready Python application that watches Tise.com user profiles and downloads all their posts (images + metadata) with smart duplicate prevention and beautiful file organization.

## ✨ Features

- 🎯 **Profile Monitoring**: Track any Tise.com user profile for new posts
- ⏰ **Automatic Checking**: Set custom intervals (default: every 30 minutes)  
- 🚫 **Smart Duplicates**: Never download the same post twice
- � **Perfect Organization**: Files organized by username with descriptive names
- �️ **Enhanced Naming**: `Post Title_UniqueID_ImageNumber.jpg` format
- � **SQLite Tracking**: Built-in database tracks everything
- 📊 **Statistics**: View download stats and success rates
- 🔧 **Easy Configuration**: Simple config file setup

## 🚀 Quick Start

### 1️⃣ **Easy Installation**
```cmd
# Run the setup script (installs everything automatically)
setup.bat
```

### 2️⃣ **Configure Your Profile**
Edit `config.py` and add the profile you want to monitor:
```python
PROFILES_TO_MONITOR = [
    "https://tise.com/your-target-username",
]
```

### 3️⃣ **Run the Scraper**
```cmd
# Download all current posts once
python main.py --check

# Start continuous monitoring  
python main.py --auto

# View statistics
python main.py --stats

# OR use the easy service launcher
run.bat
```

## 📁 File Organization

Your downloads will be organized like this:
```
data/downloads/username/
├── images/
│   ├── Air Jordan 6_5f8dd7f28bd2d700127c9dea_1.jpg
│   ├── Air Jordan 6_5f8dd7f28bd2d700127c9dea_2.jpg
│   ├── Dunk Galaxy Blue_60ca34f75e874a00961a617d_1.jpg
│   └── ...
├── metadata/
│   ├── post_metadata_1.json
│   └── ...
└── metadata.json  # Summary of all posts
```

## ⚙️ Configuration

Key settings in `config.py`:
```python
# How often to check (in minutes)
CHECK_INTERVAL_MINUTES = 30

# Profiles to monitor
PROFILES_TO_MONITOR = [
    "https://tise.com/username1",
    "https://tise.com/username2",
]

# File locations
DOWNLOADS_FOLDER = "data/downloads"
DATABASE_PATH = "data/database.db"
```

## 📊 Command Options

| Command | Description | When to Use |
|---------|-------------|-------------|
| `run.bat` | **Easy service launcher** - Starts monitoring automatically | 🚀 **Recommended for daily use** |
| `python main.py --check` | Download all current posts once and exit | ✅ **First time setup or testing** |
| `python main.py --auto` | Start continuous monitoring (every 30 min) | 🔄 **Manual monitoring** |
| `python main.py --stats` | Show download statistics | 📈 **Check progress** |

## 🎯 Example Output

**Successful run example:**
```
==================================================
TISE MONITOR STATISTICS
==================================================
Active Profiles: 1
Total Posts Found: 16
Downloaded Posts: 16
Recent Posts (24h): 16
Download Success Rate: 100.0%
Total Files Downloaded: 68
Total Download Size: 9.8 MB
Downloads Folder: data\downloads
==================================================
```

## 🛠️ Manual Installation (Alternative)

If `setup.bat` doesn't work:
```cmd
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create directories
mkdir data
mkdir logs  
mkdir data\downloads
```

## ⚡ Pro Tips

- 🎯 **First Run**: Always use `--check` first to download existing posts
- ⏰ **Testing**: Lower `CHECK_INTERVAL_MINUTES` to 2 for testing
- 📂 **Organization**: Files are automatically organized by username
- 🔍 **Debugging**: Check `logs/` folder if something goes wrong
- 💾 **Database**: Located at `data/database.db` (can be deleted to reset)

## 🏗️ Project Structure
```
tise-AI-check-n-scrape/
├── 📄 main.py                  # Main application
├── ⚙️ config.py                # Your settings
├── 📋 requirements.txt         # Dependencies
├── 🪟 setup.bat               # Windows installer
├── � run.bat                 # Service launcher
├── �📁 src/
│   ├── 🔧 database.py         # Database handling
│   ├── 🌐 scraper_new.py      # Web scraping (API-based)  
│   └── 📥 downloader.py       # File downloads
├── 📁 data/
│   ├── 📁 downloads/          # Your downloaded files
│   └── 🗄️ database.db        # Tracking database
└── 📁 logs/                   # Application logs
```

## 🔧 Troubleshooting

### ❌ Common Issues

| Problem | Solution |
|---------|----------|
| **"Module not found"** | Run `pip install -r requirements.txt` |
| **"Permission denied"** | Run PowerShell as Administrator |
| **"Profile not found"** | Check the Tise URL is correct and public |
| **"No posts found"** | Profile might be empty or private |

### 📋 Getting Profile URLs

1. Go to Tise.com
2. Search for the user you want to monitor  
3. Copy their profile URL (e.g., `https://tise.com/username`)
4. Add to `PROFILES_TO_MONITOR` in `config.py`

- � **Respect the website**: Built-in delays prevent server overload
- 📋 **Check terms of service**: Ensure compliance with Tise.com's terms
- 🔒 **Private data**: Only monitor public profiles
- 💾 **Local use**: Keep downloaded content for personal use only

## 🤝 Contributing

Found a bug or want to improve the scraper? Feel free to contribute!

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📞 Support

Having issues? Check these resources:

1. 📋 **Logs**: Check `logs/` folder for error details
2. 🗄️ **Database**: Delete `data/database.db` to reset if corrupted
3. 🔄 **Restart**: Try `python main.py --check` for a fresh start

---

**🎉 Happy scraping! This tool helps you easily monitor and organize Tise.com profiles with automated downloads and smart file organization.**

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
