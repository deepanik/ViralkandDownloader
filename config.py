import os
import json

# Telegram Bot Configuration
# Reads from environment variables first, falls back to hardcoded values for local development
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Telegram API Credentials (Get from https://my.telegram.org/apps)
API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")

# Admin User IDs (Array of user IDs who have admin privileges)
# Can be set as JSON array string in env: "[6254260120]" or comma-separated: "6254260120"
admin_ids_str = os.getenv("ADMIN_IDS", "[]")
try:
    ADMIN_IDS = json.loads(admin_ids_str) if isinstance(admin_ids_str, str) else admin_ids_str
except:
    # Fallback: try comma-separated
    ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(",")] if admin_ids_str else []

# Group IDs where the bot will work (Array of group/chat IDs)
# Can be set as JSON array string in env: "[-1003328022346]" or comma-separated: "-1003328022346"
group_ids_str = os.getenv("GROUP_IDS", "[-12345]")
try:
    GROUP_IDS = json.loads(group_ids_str) if isinstance(group_ids_str, str) else group_ids_str
except:
    # Fallback: try comma-separated
    GROUP_IDS = [int(x.strip()) for x in group_ids_str.split(",")] if group_ids_str else [-12345]

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://#")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "viralkand_bot")
