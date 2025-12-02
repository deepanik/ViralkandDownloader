import os
import json

# Telegram Bot Configuration
# Reads from environment variables first, falls back to hardcoded values for local development
BOT_TOKEN = os.getenv("BOT_TOKEN", "8528138443:AAEmFwE0KAmrA4v0H2zRfZJ_a9l9kratcd8")

# Telegram API Credentials (Get from https://my.telegram.org/apps)
API_ID = os.getenv("API_ID", "36998260")
API_HASH = os.getenv("API_HASH", "db67579e13f426a10f4d8dcff6d2ced2")

# Admin User IDs (Array of user IDs who have admin privileges)
# Can be set as JSON array string in env: "[6254260120]" or comma-separated: "6254260120"
admin_ids_str = os.getenv("ADMIN_IDS", "[6254260120]")
try:
    ADMIN_IDS = json.loads(admin_ids_str) if isinstance(admin_ids_str, str) else admin_ids_str
except:
    # Fallback: try comma-separated
    ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(",")] if admin_ids_str else [6254260120]

# Group IDs where the bot will work (Array of group/chat IDs)
# Can be set as JSON array string in env: "[-1003328022346]" or comma-separated: "-1003328022346"
group_ids_str = os.getenv("GROUP_IDS", "[-1003328022346]")
try:
    GROUP_IDS = json.loads(group_ids_str) if isinstance(group_ids_str, str) else group_ids_str
except:
    # Fallback: try comma-separated
    GROUP_IDS = [int(x.strip()) for x in group_ids_str.split(",")] if group_ids_str else [-1003328022346]

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://dropmail880_db_user:lqXiGLNkEowwcOo9@cluster0.aw9jwfg.mongodb.net/?appName=Cluster0")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "viralkand_bot")
