import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '')

# Download settings
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB Telegram limit
TEMP_DIR = "temp"
SUPPORTED_FORMATS = ['mp3', 'mp4']
MAX_VIDEO_DURATION = 3600  # 1 hour in seconds

# YouTube settings
VIDEO_QUALITIES = ['144p', '240p', '360p', '480p', '720p', '1080p']
AUDIO_QUALITIES = ['64kbps', '128kbps', '192kbps']

# Bot behavior settings
CLEANUP_INTERVAL_HOURS = 1
SHOW_PROGRESS = True
ALLOW_LARGE_FILES = False

# Messages
WELCOME_MESSAGE = """
👋 Hello {user_name}!

I'm YouTube Downloader Bot! 🎵📹

Send me a YouTube link and I'll download it for you in your preferred format.

Supported formats:
• 🎵 Audio (MP3)
• 📹 Video (MP4)

Just paste a YouTube URL and choose your preferred format!
"""

HELP_MESSAGE = """
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
- Maximum duration: 1 hour
"""
