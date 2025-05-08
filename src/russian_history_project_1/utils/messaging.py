from aiogram import Bot, types
from typing import Dict, Optional
import logging

_last_messages: Dict[int, int] = {}

async def send_and_replace(
    bot: Bot,
    chat_id: int,
    text: str,
    reply_markup: Optional[types.InlineKeyboardMarkup] = None,
) -> types.Message:
    """
    Sends a message and removes the previous bot message in the chat (if any).
    This keeps the chat tidy and behaves like a "single‑message interface".
    """
    if chat_id in _last_messages:
        try:
            await bot.delete_message(chat_id, _last_messages[chat_id])
        except Exception as exc:
            logging.warning("Failed to delete message %s in chat %s: %s",
                            _last_messages[chat_id], chat_id, exc)

    msg = await bot.send_message(chat_id, text, reply_markup=reply_markup)
    _last_messages[chat_id] = msg.message_id
    return msg
