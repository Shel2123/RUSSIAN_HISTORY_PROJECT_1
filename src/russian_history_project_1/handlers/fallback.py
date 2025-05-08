from aiogram import types, Dispatcher
import logging

from ..keyboards.common import main_keyboard
from ..utils.messaging import send_and_replace

def register(dp: Dispatcher) -> None:
    async def unknown(message: types.Message) -> None:
        logging.info("Unknown message from %s: %s", message.from_user.id, message.text)
        await send_and_replace(
            message.bot, message.chat.id,
            "Please use the buttons below to navigate.", reply_markup=main_keyboard()
        )

    dp.message.register(unknown)
