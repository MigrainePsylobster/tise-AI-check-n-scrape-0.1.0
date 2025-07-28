# 🐍 Python Virtual Environment Setup Guide

## What is a Virtual Environment?
Think of it like creating a **separate workspace** for your project - it keeps all your Python packages organized and prevents conflicts with other projects.

## Step-by-Step Setup

### 1. Open Command Prompt (PowerShell)
- Press `Win + R`
- Type `cmd` and press Enter
- Navigate to your project folder:
```bash
cd "e:\Repos\AI-check-n-scrape\tise-AI-check-n-scrape"
```

### 2. Create Virtual Environment
```bash
python -m venv tise_scraper_env
```
This creates a folder called `tise_scraper_env` with your isolated Python environment.

### 3. Activate the Environment
```bash
tise_scraper_env\Scripts\activate
```
You should see `(tise_scraper_env)` appear at the beginning of your command prompt.

### 4. Install Requirements
```bash
pip install -r requirements.txt
```
This installs all the packages needed for your scraper.

### 5. Verify Installation
```bash
python -c "import requests, bs4, selenium; print('✅ All packages installed successfully!')"
```

## Daily Usage

### To Start Working:
```bash
cd "e:\Repos\AI-check-n-scrape\tise-AI-check-n-scrape"
tise_scraper_env\Scripts\activate
```

### To Run Your Scraper:
```bash
python main.py
```

### To Stop Working:
```bash
deactivate
```

## Troubleshooting

### If Python Command Not Found:
1. Make sure Python is installed
2. Add Python to your PATH
3. Try `py` instead of `python`

### If pip install fails:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### If Selenium Issues:
Make sure Chrome browser is installed - Selenium needs it to work.

## Files Created:
- `tise_scraper_env/` folder (don't commit this to git)
- Your project will use packages from this isolated environment

**✅ Once this is set up, you're ready to test the scraper!**
