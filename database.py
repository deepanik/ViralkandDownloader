import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import MONGODB_URI, MONGODB_DB_NAME, ADMIN_IDS

logger = logging.getLogger(__name__)

# Global MongoDB client
client = None
db = None


def connect_mongodb():
    """Connect to MongoDB and initialize database"""
    global client, db
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        db = client[MONGODB_DB_NAME]
        
        # Initialize admins collection with default admin IDs
        admins_collection = db['admins']
        for admin_id in ADMIN_IDS:
            admins_collection.update_one(
                {'user_id': admin_id},
                {'$set': {'user_id': admin_id, 'is_admin': True}},
                upsert=True
            )
        
        logger.info(f"Connected to MongoDB: {MONGODB_DB_NAME}")
        return True
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {str(e)}")
        return False


def get_admins():
    """Get list of admin user IDs from MongoDB"""
    global db
    if db is None:
        # Fallback to config if MongoDB not connected
        return ADMIN_IDS
    
    try:
        admins_collection = db['admins']
        admins = admins_collection.find({'is_admin': True})
        admin_ids = [admin['user_id'] for admin in admins]
        # Merge with config admins to ensure they're included
        all_admins = list(set(admin_ids + ADMIN_IDS))
        return all_admins
    except Exception as e:
        logger.error(f"Error getting admins from MongoDB: {str(e)}")
        return ADMIN_IDS


def add_admin(user_id: int) -> bool:
    """Add a user as admin in MongoDB"""
    global db
    if db is None:
        logger.error("MongoDB not connected")
        return False
    
    try:
        admins_collection = db['admins']
        result = admins_collection.update_one(
            {'user_id': user_id},
            {'$set': {'user_id': user_id, 'is_admin': True}},
            upsert=True
        )
        logger.info(f"Admin added: {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error adding admin: {str(e)}")
        return False


def remove_admin(user_id: int) -> bool:
    """Remove a user from admin in MongoDB"""
    global db
    if db is None:
        logger.error("MongoDB not connected")
        return False
    
    try:
        admins_collection = db['admins']
        result = admins_collection.update_one(
            {'user_id': user_id},
            {'$set': {'is_admin': False}}
        )
        logger.info(f"Admin removed: {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error removing admin: {str(e)}")
        return False


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    admins = get_admins()
    return user_id in admins


def get_bot_stats():
    """Get bot statistics from MongoDB"""
    global db
    if db is None:
        return None
    
    try:
        admins_collection = db['admins']
        total_admins = admins_collection.count_documents({'is_admin': True})
        return {
            'total_admins': total_admins
        }
    except Exception as e:
        logger.error(f"Error getting bot stats: {str(e)}")
        return None

