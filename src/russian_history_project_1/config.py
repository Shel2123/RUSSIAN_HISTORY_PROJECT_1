"""
Centralised configuration for the bot.
Loads environment variables declared in a .env file.
"""
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

BOT_TOKEN: Optional[str] = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set.")

DB_PATH: str = os.getenv("DB_PATH", "events.db")
