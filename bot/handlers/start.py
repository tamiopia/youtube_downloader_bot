from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when the command /start is issued."""
    user = update.effective_user
    welcome_text = f"""
👋 Hello {user.first_name}!

I'm YouTube Downloader Bot! 🎵📹

Send me a YouTube link and I'll download it for you in your preferred format.

Supported formats:
• 🎵 Audio (MP3)
• 📹 Video (MP4)

Just paste a YouTube URL and choose your preferred format!
    """
    await update.message.reply_text(welcome_text)

def setup_start_handlers(application):
    application.add_handler(CommandHandler("start", start))