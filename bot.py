import logging
import os
import tempfile
import requests
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
from config import BOT_TOKEN, ADMIN_IDS, GROUP_IDS
from kand import extract_urls as extract_urls_kand, validate_and_check_url as validate_viralkand
from database import connect_mongodb, get_admins, add_admin, is_admin as db_is_admin, get_bot_stats

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    """Check if user is an admin"""
    return db_is_admin(user_id)


def is_allowed_group(chat_id: int) -> bool:
    """Check if the chat is in allowed groups"""
    if not GROUP_IDS:  # If empty, allow all groups
        return True
    return chat_id in GROUP_IDS


async def download_and_upload_video(video_url: str, update: Update, caption: str = None) -> None:
    """Download video from URL and upload to Telegram"""
    temp_path = None
    status_msg = None
    chat_id = update.effective_chat.id
    
    try:
        # Send processing message (use chat.send_message since original message is deleted)
        status_msg = await update.effective_chat.send_message("⬇️ Downloading video...")
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        temp_path = temp_file.name
        temp_file.close()
        
        # Download video
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(video_url, headers=headers, stream=True, timeout=300)
        response.raise_for_status()
        
        # Save video to temp file
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Check file size (Telegram limit is 50MB for bots)
        file_size = os.path.getsize(temp_path)
        file_size_mb = file_size / (1024 * 1024)
        
        if file_size > 50 * 1024 * 1024:  # 50MB
            if status_msg:
                await status_msg.edit_text(f"❌ Video file is too large ({file_size_mb:.2f}MB). Max size: 50MB")
            return
        
        # Log file size for debugging
        logger.info(f"Video file size: {file_size_mb:.2f}MB")
        
        # Update status
        if status_msg:
            await status_msg.edit_text("⬆️ Uploading video...")
        
        # Upload video to Telegram (timeouts handled at application level)
        # Use InputFile to ensure proper video format with audio preserved
        with open(temp_path, 'rb') as video_file:
            video_input = InputFile(
                video_file,
                filename='video.mp4'
            )
            await update.effective_chat.send_video(
                video=video_input,
                caption=caption,
                supports_streaming=True
            )
        
        # Delete status message
        if status_msg:
            await status_msg.delete()
        logger.info(f"Video uploaded successfully: {video_url}")
        
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Error downloading video: {str(e)}"
        if status_msg:
            await status_msg.edit_text(error_msg)
        else:
            await update.effective_chat.send_message(error_msg)
        logger.error(f"Error downloading video: {str(e)}")
    except Exception as e:
        error_type = type(e).__name__
        error_msg = f"❌ Error uploading video: {error_type}: {str(e)}"
        if status_msg:
            await status_msg.edit_text(error_msg)
        else:
            await update.effective_chat.send_message(error_msg)
        logger.error(f"Error uploading video: {error_type}: {str(e)}", exc_info=True)
    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /status command - shows bot status"""
    # Check if message is from allowed group
    chat_id = update.effective_chat.id
    if not is_allowed_group(chat_id):
        return
    
    stats = get_bot_stats()
    if stats:
        response = f"🤖 **Bot Status**\n\n"
        response += f"👥 Total Admins: {stats['total_admins']}\n"
        response += f"✅ MongoDB: Connected\n"
        response += f"🔄 Bot: Active"
    else:
        response = f"🤖 **Bot Status**\n\n"
        response += f"❌ MongoDB: Not Connected\n"
        response += f"🔄 Bot: Active"
    
    await update.message.reply_text(response, parse_mode='Markdown')


async def randi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /randi command - promotes user to admin"""
    # Check if message is from allowed group
    chat_id = update.effective_chat.id
    if not is_allowed_group(chat_id):
        return
    
    # Check if command has reply (to promote another user)
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        target_user_id = target_user.id
        
        # Check if current user is admin
        current_user_id = update.effective_user.id
        if not is_admin(current_user_id):
            await update.message.reply_text("❌ Only admins can promote users.")
            return
        
        # Add admin
        if add_admin(target_user_id):
            await update.message.reply_text(f"✅ {target_user.first_name} has been promoted to admin!")
        else:
            await update.message.reply_text("❌ Failed to promote user. Check MongoDB connection.")
    else:
        # Promote the user who sent the command
        current_user_id = update.effective_user.id
        
        # Check if current user is already admin
        if is_admin(current_user_id):
            await update.message.reply_text("✅ You are already an admin!")
            return
        
        # Check if any admin exists to authorize
        admins = get_admins()
        if not admins:
            # First user becomes admin
            if add_admin(current_user_id):
                await update.message.reply_text("✅ You have been promoted to admin!")
            else:
                await update.message.reply_text("❌ Failed to promote. Check MongoDB connection.")
        else:
            await update.message.reply_text("❌ Only existing admins can promote new admins. Reply to this message with /randi to promote someone.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for text messages - extracts video and uploads when link is dropped"""
    # Check if message is from allowed group
    chat_id = update.effective_chat.id
    if not is_allowed_group(chat_id):
        return
    
    if not update.message or not update.message.text:
        return
    
    # Check if user is admin
    user_id = update.effective_user.id
    if not is_admin(user_id):
        # Delete user's message first
        try:
            await update.message.delete()
        except Exception as e:
            logger.warning(f"Could not delete user message: {str(e)}")
        # Send error message
        await update.effective_chat.send_message("❌ Only admins can upload videos.")
        return
    
    text = update.message.text
    
    # Extract URLs
    urls = extract_urls_kand(text)
    
    # If no URLs found, ignore
    if not urls:
        return
    
    # Delete user's message first
    try:
        await update.message.delete()
    except Exception as e:
        logger.warning(f"Could not delete user message: {str(e)}")
    
    # Check each URL found in the message
    for url in urls:
        # Only process viralkand.com URLs
        if 'viralkand.com' in url.lower():
            result = validate_viralkand(url)
        else:
            # Unknown domain
            await update.effective_chat.send_message("invalid")
            logger.info(f"Unknown domain: {url}")
            break
        
        # Log result for debugging
        logger.info(f"URL validation result for {url}: valid={result.get('valid')}, exists={result.get('exists')}, video_url={result.get('metadata', {}).get('video_url')}")
        
        # Check if URL is valid and exists
        if result['valid'] and result['exists']:
            metadata = result.get('metadata', {})
            video_url = metadata.get('video_url')
            
            if video_url:
                # Build caption from metadata
                caption_parts = []
                if metadata.get('title'):
                    caption_parts.append(f"📌 {metadata['title']}")
                
                caption = "\n".join(caption_parts) if caption_parts else None
                
                # Download and upload video
                await download_and_upload_video(video_url, update, caption)
                logger.info(f"Video URL extracted and uploaded: {video_url}")
            else:
                # No video URL found
                await update.effective_chat.send_message("invalid")
                logger.warning(f"Valid URL but no video found: {url}. Metadata: {metadata}")
            break  # Only process first valid URL
        else:
            # Invalid URL or doesn't exist
            await update.effective_chat.send_message("invalid")
            logger.warning(f"Invalid URL or not accessible: {url}. valid={result.get('valid')}, exists={result.get('exists')}, message={result.get('message')}")
            break


def main() -> None:
    """Start the bot"""
    # Connect to MongoDB
    if not connect_mongodb():
        logger.warning("MongoDB connection failed. Using config file for admins.")
    
    # Create application with increased timeouts
    request = HTTPXRequest(
        connection_pool_size=8,
        read_timeout=600,
        write_timeout=600,
        connect_timeout=60,
        pool_timeout=60
    )
    application = Application.builder().token(BOT_TOKEN).request(request).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("randi", randi))
    
    # Register message handler for direct link drops (should be after command handlers)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

