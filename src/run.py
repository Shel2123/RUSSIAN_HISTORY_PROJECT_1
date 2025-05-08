"""
Entrypoint for the Telegram war bot.
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from russian_history_project_1.config import BOT_TOKEN
from russian_history_project_1.handlers import register_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
register_handlers(dp)

async def main() -> None:
    logging.info("Bot is starting…")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
