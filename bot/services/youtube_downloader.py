import os
import asyncio
import tempfile
import yt_dlp
from telegram import Update
from telegram.ext import ContextTypes
from config.settings import MAX_FILE_SIZE

class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts_audio = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(tempfile.gettempdir(), 'audio_%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        self.ydl_opts_video = {
            'format': 'best[filesize<50M]',
            'outtmpl': os.path.join(tempfile.gettempdir(), 'video_%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

    async def download_audio(self, url: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Download YouTube video as audio (MP3) using yt-dlp."""
        try:
            query = update.callback_query
            await query.edit_message_text("⏳ Starting audio download...")
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self._download_audio_sync, url)
            return result
            
        except Exception as e:
            return {'error': f'Audio download failed: {str(e)}'}

    def _download_audio_sync(self, url: str):
        """Synchronous audio download function."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts_audio) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                # Change extension to .mp3 for audio files
                if '.webm' in file_path or '.m4a' in file_path:
                    file_path = file_path.replace('.webm', '.mp3').replace('.m4a', '.mp3')
                
                # Get file size
                file_size = os.path.getsize(file_path)
                
                if file_size > MAX_FILE_SIZE:
                    os.unlink(file_path)
                    raise Exception(f"File too large ({file_size / 1024 / 1024:.1f}MB). Max allowed: {MAX_FILE_SIZE / 1024 / 1024}MB")
                
                return {
                    'file_path': file_path,
                    'title': info.get('title', 'Unknown Title'),
                    'duration': info.get('duration', 0),
                    'file_size': file_size
                }
                
        except Exception as e:
            return {'error': str(e)}

    async def download_video(self, url: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Download YouTube video as video (MP4) using yt-dlp."""
        try:
            query = update.callback_query
            await query.edit_message_text("⏳ Starting video download...")
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self._download_video_sync, url)
            return result
            
        except Exception as e:
            return {'error': f'Video download failed: {str(e)}'}

    def _download_video_sync(self, url: str):
        """Synchronous video download function."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts_video) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                file_size = os.path.getsize(file_path)
                
                if file_size > MAX_FILE_SIZE:
                    os.unlink(file_path)
                    raise Exception(f"File too large ({file_size / 1024 / 1024:.1f}MB). Max allowed: {MAX_FILE_SIZE / 1024 / 1024}MB")
                
                return {
                    'file_path': file_path,
                    'title': info.get('title', 'Unknown Title'),
                    'duration': info.get('duration', 0),
                    'quality': info.get('format_note', 'Unknown'),
                    'file_size': file_size
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    async def send_file_to_user(self, result: dict, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send downloaded file to user."""
        try:
            query = update.callback_query
            file_path = result['file_path']
            
            await query.edit_message_text("📤 Uploading to Telegram...")
            
            # Determine file type and send accordingly
            if file_path.endswith('.mp3'):
                await context.bot.send_audio(
                    chat_id=query.message.chat_id,
                    audio=open(file_path, 'rb'),
                    title=result.get('title', 'Audio File')[:64],  # Telegram title limit
                    duration=result.get('duration'),
                    caption=f"✅ {result.get('title', 'Audio file')}\n🎵 Downloaded via YouTube Bot"
                )
            else:
                await context.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=open(file_path, 'rb'),
                    caption=f"✅ {result.get('title', 'Video file')}\n📹 Quality: {result.get('quality', 'Unknown')}\n🎬 Downloaded via YouTube Bot"
                )
            
            # Clean up file
            if os.path.exists(file_path):
                os.unlink(file_path)
            await query.edit_message_text("✅ Download completed!")
            
        except Exception as e:
            await query.edit_message_text(f"❌ Failed to send file: {str(e)}")
            # Clean up file even if sending fails
            if 'file_path' in result and os.path.exists(result['file_path']):
                os.unlink(result['file_path'])