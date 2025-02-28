import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


class BotCommand:
    def __init__(self):
        load_dotenv()
        self.TOKEN= getenv("BOT_TOKEN")
        self.bot = Bot(token=self.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher()
        self.register_handlers()

    def register_handlers(self):
        @self.dp.message(CommandStart())
        async def command_start_handler(message: Message) -> None:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Year 1941", callback_data="command_1"),
                    InlineKeyboardButton(text="Year 1942", callback_data="command_2")
                ],
                [
                    InlineKeyboardButton(text="Year 1943", callback_data="command_3"),
                    InlineKeyboardButton(text="Year 1944", callback_data="command_4"),
                    InlineKeyboardButton(text="Year 1945", callback_data="command_5")
                ],
                [
                    InlineKeyboardButton(text="Main Dates", callback_data="command_6")
                ],
                [
                    InlineKeyboardButton(text="Sources", callback_data="command_7")
                ]
                ])

            await message.answer(
                f"Hi, {html.bold(message.from_user.full_name)}, I am telegram bot for studying the chronology of the Great Patriotic War.",
                reply_markup=keyboard
                )

        @self.dp.message()
        async def echo_handler(message: Message) -> None:
            try:
                await message.send_copy(chad_id=message.chat.id)
            except TypeError:
                await message.answer("Nice Try!")

    async def start(self) -> None:
        await self.dp.start_polling(self.bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot_instance = BotCommand()
    asyncio.run(bot_instance.start())
