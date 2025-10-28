import asyncio

class ProgressHandler:
    async def update_progress(self, message, percentage, download_type="Download"):
        """Update download progress message."""
        try:
            progress_bar = self.create_progress_bar(percentage)
            text = f"⏳ {download_type}...\n{progress_bar} {percentage:.1f}%"
            await message.edit_text(text)
        except Exception:
            pass  # Ignore edit conflicts

    def create_progress_bar(self, percentage, length=20):
        """Create a visual progress bar."""
        filled_length = int(length * percentage // 100)
        bar = '█' * filled_length + '░' * (length - filled_length)
        return bar

    async def update_upload_progress(self, message, current, total, upload_type="Upload"):
        """Update upload progress message."""
        try:
            if total > 0:
                percentage = (current / total) * 100
                progress_bar = self.create_progress_bar(percentage)
                text = f"📤 {upload_type}...\n{progress_bar} {percentage:.1f}%"
                await message.edit_text(text)
        except Exception:
            pass