from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message when the command /help is issued."""
    help_text = """
🤖 How to use this bot:

1. Send any YouTube video URL
2. Choose whether you want Audio or Video
3. Wait for the download to complete
4. Receive your file!

Example URLs:
• https://www.youtube.com/watch?v=VIDEO_ID
• https://youtu.be/VIDEO_ID
• YouTube Shorts URLs

📝 Note: 
- Large videos may take longer to download
- Maximum file size: 50MB (Telegram limit)
    """
    await update.message.reply_text(help_text)

def setup_help_handlers(application):
    application.add_handler(CommandHandler("help", help_command))