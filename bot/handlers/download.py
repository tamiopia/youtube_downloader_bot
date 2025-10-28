import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, CallbackQueryHandler, filters
from bot.utils.helpers import is_youtube_url
from bot.services.youtube_downloader import YouTubeDownloader
from bot.services.file_cleanup import cleanup_temp_files

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming YouTube URLs."""
    message_text = update.message.text
    
    if is_youtube_url(message_text):
        try:
            context.user_data['youtube_url'] = message_text
            
            keyboard = [
                [
                    InlineKeyboardButton("🎵 Download Audio (MP3)", callback_data="audio"),
                    InlineKeyboardButton("📹 Download Video (MP4)", callback_data="video")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "Choose your preferred format:",
                reply_markup=reply_markup
            )
            
        except Exception as e:
            await update.message.reply_text("❌ Error processing the URL. Please try again.")
    else:
        await update.message.reply_text("❌ Please send a valid YouTube URL.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    user_choice = query.data
    youtube_url = context.user_data.get('youtube_url')
    
    if not youtube_url:
        await query.edit_message_text("❌ No YouTube URL found. Please send a URL first.")
        return

    try:
        await query.edit_message_text("⏳ Processing your request... Please wait.")
        
        downloader = YouTubeDownloader()
        
        if user_choice == "audio":
            result = await downloader.download_audio(youtube_url, update, context)
        else:
            result = await downloader.download_video(youtube_url, update, context)
        
        if result and 'file_path' in result:
            # Clean up temporary files older than 1 hour
            await cleanup_temp_files()
            
        elif result and 'error' in result:
            await query.edit_message_text(f"❌ {result['error']}")
            
    except Exception as e:
        await query.edit_message_text("❌ An error occurred while processing your request.")

def setup_download_handlers(application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Update the button_handler to use the downloader's send method
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    user_choice = query.data
    youtube_url = context.user_data.get('youtube_url')
    
    if not youtube_url:
        await query.edit_message_text("❌ No YouTube URL found. Please send a URL first.")
        return

    try:
        downloader = YouTubeDownloader()
        
        if user_choice == "audio":
            result = await downloader.download_audio(youtube_url, update, context)
        else:
            result = await downloader.download_video(youtube_url, update, context)
        
        if result and 'file_path' in result:
            # Send file to user
            await downloader.send_file_to_user(result, update, context)
            
            # Clean up temporary files
            await cleanup_temp_files()
            
        elif result and 'error' in result:
            await query.edit_message_text(f"❌ {result['error']}")
            
    except Exception as e:
        await query.edit_message_text("❌ An error occurred while processing your request.")