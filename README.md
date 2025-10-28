# YouTube Telegram Bot

A Telegram bot that downloads YouTube videos and audio.

## Features

- Download YouTube videos as MP4
- Download YouTube audio as MP3
- User-friendly interface
- Progress updates
- Temporary file cleanup

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your bot token
4. Run the bot: `python run.py`

## Usage

1. Start the bot with `/start`
2. Send a YouTube URL
3. Choose audio or video format
4. Wait for download to complete

## Configuration

Edit `config/settings.py` to customize:
- File size limits
- Video qualities
- Temporary directory