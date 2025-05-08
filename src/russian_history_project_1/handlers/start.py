from aiogram import types, Dispatcher
from aiogram.filters import Command
import logging

from ..keyboards.common import main_keyboard
from ..utils.messaging import send_and_replace

async def _start(message: types.Message) -> None:
    user = message.from_user
    logging.info("User %s (%s) started the bot", user.id, user.full_name)
    text = (
        f"Hi, {user.full_name}! "
        "I am a bot for studying the chronology of the Great Patriotic War."
    )
    await send_and_replace(message.bot, user.id, text, reply_markup=main_keyboard())

def register(dp: Dispatcher) -> None:
    dp.message.register(_start, Command(commands=["start", "help"]))
