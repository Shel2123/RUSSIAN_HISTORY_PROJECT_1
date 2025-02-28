import asyncio
import logging
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import register_handlers

load_dotenv()
API_TOKEN = getenv("BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Регистрация обработчиков
register_handlers(dp, bot)

async def main():
    logging.info("Bot is starting...")
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
