import os
import time
import tempfile
import glob

async def cleanup_temp_files(max_age_hours=1):
    """Clean up temporary files older than specified hours."""
    try:
        temp_dir = tempfile.gettempdir()
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        # Pattern for our temporary files
        patterns = [
            os.path.join(temp_dir, "audio_*"),
            os.path.join(temp_dir, "video_*")
        ]
        
        deleted_files = 0
        for pattern in patterns:
            for file_path in glob.glob(pattern):
                try:
                    # Check file age
                    file_age = current_time - os.path.getctime(file_path)
                    if file_age > max_age_seconds:
                        os.unlink(file_path)
                        deleted_files += 1
                except (OSError, Exception):
                    continue
        
        return deleted_files
        
    except Exception as e:
        print(f"Cleanup error: {e}")
        return 0

async def cleanup_specific_file(file_path: str):
    """Clean up a specific file if it exists."""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
            return True
    except Exception:
        pass
    return False