import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database - Use PostgreSQL in production, SQLite locally
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # Fallback to SQLite for local development
    DATA_DIR = BASE_DIR / "data"
    DATA_DIR.mkdir(exist_ok=True)
    DATABASE_URL = f"sqlite:///{DATA_DIR / 'workreport.db'}"

# Application
APP_NAME = "Annotation Daily HQ"
APP_DESCRIPTION = "Daily work logging for annotation teams"

# Task types
TASK_TYPES = [
    "Bounding Boxes",
    "Segmentation",
    "Classification",
    "QA / Review",
    "Other"
]

# Status options
STATUS_OPTIONS = [
    "Completed",
    "Partially completed",
    "Blocked"
]

# Slack Integration
# Set your webhook URL here or via environment variable
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")

# You can also store it in a .env file or config.json
# For now, you can set it directly here:
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

