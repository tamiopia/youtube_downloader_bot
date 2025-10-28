import re

def is_youtube_url(url: str) -> bool:
    """Check if the given URL is a valid YouTube URL."""
    youtube_patterns = [
        r'^https?://(www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'^https?://youtu\.be/([a-zA-Z0-9_-]+)',
        r'^https?://(www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]+)',
        r'^https?://(www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)'
    ]
    
    return any(re.match(pattern, url) for pattern in youtube_patterns)

def format_file_size(size_bytes):
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB']
    unit_index = 0
    
    while size_bytes >= 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1
    
    return f"{size_bytes:.2f} {units[unit_index]}"

def format_duration(seconds):
    """Format duration in seconds to HH:MM:SS or MM:SS."""
    if seconds < 0:
        return "Unknown"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def sanitize_filename(filename):
    """Remove invalid characters from filename."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename[:100]  # Limit filename length