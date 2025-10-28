import logging
import os
from telegram.ext import Application
from config.settings import BOT_TOKEN
from bot.handlers.start import setup_start_handlers
from bot.handlers.help import setup_help_handlers
from bot.handlers.download import setup_download_handlers

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the bot."""
    try:
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Set up handlers
        setup_start_handlers(application)
        setup_help_handlers(application)
        setup_download_handlers(application)
        
        # Start the bot
        logger.info("Bot is starting...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == '__main__':
    main()