# Tise Profile Monitor

A Python-based API scraper and monitoring tool for Tise.com profiles. This application automatically monitors specified Tise profiles for new posts, downloads associated content, and maintains a local database to prevent duplicate processing.

## Overview

This project demonstrates reverse engineering of Tise.com's front-end API to extract profile data and media content. The application provides automated monitoring capabilities with configurable check intervals and comprehensive logging.

## Features

- **Automated Profile Monitoring**: Continuously monitors specified Tise profiles for new posts
- **Content Download**: Automatically downloads images and metadata from new posts
- **Duplicate Prevention**: Uses SQLite database to track processed posts and avoid reprocessing
- **Flexible Operation Modes**: Supports both interactive and automatic monitoring modes
- **Comprehensive Logging**: Detailed logging with both file and console output
- **Statistics Tracking**: Built-in statistics for monitoring performance and download metrics
- **Configurable Settings**: Easy configuration through centralized config file

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd tise-AI-check-n-scrape
   ```

2. Run `setup.bat`:
   This will create a virtual Python environment and install requirements

3. Open `config.py`:
   Add the target profile names
     Configure profiles
   ```python
   PROFILES_TO_MONITOR = [
       "https://tise.com/profiles/username1",
       "https://tise.com/profiles/username2"
   ]
   ```

4. Run `run.bat`:
   This will start the application


### Configuration

Edit `config.py` to customize the application behavior:

- `PROFILES_TO_MONITOR`: List of Tise profile URLs to monitor
- `CHECK_INTERVAL_MINUTES`: Time between automatic checks (default: 30 minutes)
- `REQUEST_DELAY_SECONDS`: Delay between profile requests (default: 2 seconds)
- `DOWNLOADS_FOLDER`: Directory for downloaded content (default: "data/downloads")
- `DATABASE_PATH`: SQLite database file location (default: "data/database.db")


## Technical Details

### Dependencies

- **requests**: HTTP requests and API communication
- **beautifulsoup4**: HTML parsing and data extraction
- **selenium**: Web automation for dynamic content
- **schedule**: Task scheduling for automatic monitoring
- **Pillow**: Image processing and manipulation
- **lxml**: XML/HTML processing
- **python-dotenv**: Environment variable management

### Database Schema

The application uses SQLite to store:
- Profile information and monitoring status
- Post metadata and processing history
- Download statistics and file tracking
- Timestamp data for duplicate prevention

## Legal and Ethical Considerations

This tool is designed for educational and research purposes to demonstrate web scraping techniques. Users are responsible for:

- Complying with Tise.com's Terms of Service
- Respecting rate limits and server resources
- Using scraped data responsibly and ethically
- Ensuring compliance with applicable laws and regulations

## Contributing

Contributions are welcome. Please ensure all code follows the established patterns and includes appropriate error handling and logging.

## License

This project is provided as-is for educational purposes. Please review and comply with all applicable terms of service and legal requirements before use.

