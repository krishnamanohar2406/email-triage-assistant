"""
Configuration - API Keys and Settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys (loaded from .env file - hidden from users)
SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Email Settings
GMAIL_IMAP_SERVER = "imap.gmail.com"
GMAIL_IMAP_PORT = 993

# AI Settings
MAX_EMAIL_BODY_LENGTH = 2000  # Characters to analyze
ANALYSIS_TEMPERATURE = 0.3    # Lower = more consistent
MAX_TOKENS_ANALYSIS = 800     # Token limit for analysis

# Date Range Options
DATE_RANGES = {
    "latest7": "Latest 7 emails",
    "today": "Today's new emails",
    "yesterday": "Yesterday's emails",
    "7days": "Last 7 days",
    "15days": "Last 15 days (maximum)"
}

def check_api_keys():
    """Verify API keys are configured"""
    if not SCALEDOWN_API_KEY or SCALEDOWN_API_KEY == "your_scaledown_api_key_here":
        print()
        print("SCALEDOWN_API_KEY not configured in .env file")
        print()
        return False
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        print()
        print("GEMINI_API_KEY not configured in .env file")
        print()
        return False
    
    return True
