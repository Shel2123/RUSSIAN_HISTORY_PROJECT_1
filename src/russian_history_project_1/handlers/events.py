from aiogram import types, Dispatcher
import logging

from ..db import get_events, get_main_dates, get_sources
from ..utils.messaging import send_and_replace

_MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"
]

def register(dp: Dispatcher) -> None:
    async def month(callback: types.CallbackQuery) -> None:
        try:
            _, year_str, month_str = callback.data.split(":")
            year, month = int(year_str), int(month_str)
        except ValueError:
            await callback.answer("Invalid callback data")
            return

        events = get_events(year, month)
        if events:
            header = f"Events for {_MONTH_NAMES[month - 1]} {year}:\n"
            lines = [
                f"{day:02d} {_MONTH_NAMES[month - 1]} {year} — {desc}"
                for day, desc in events
            ]
            text = header + "\n".join(lines)
        else:
            text = f"No events found for {_MONTH_NAMES[month - 1]} {year}."

        back_btn = types.InlineKeyboardButton(text="Back", callback_data=f"back:{year}")
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[back_btn]])
        await send_and_replace(callback.bot, callback.from_user.id, text, reply_markup=markup)
        await callback.answer()

    async def main_dates(callback: types.CallbackQuery) -> None:
        dates = get_main_dates()
        if dates:
            lines = [f"{date} — {desc}" for date, desc in dates]
            text = "Main Dates of the Great Patriotic War:\n" + "\n".join(lines)
        else:
            text = "Main dates list is empty."
        back_btn = types.InlineKeyboardButton(text="Back", callback_data="back:main")
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[back_btn]])
        await send_and_replace(callback.bot, callback.from_user.id, text, reply_markup=markup)
        await callback.answer()

    async def sources(callback: types.CallbackQuery) -> None:
        src = get_sources()
        text = (
            "Sources:\n" + "\n".join(f"{idx + 1}. {s}" for idx, s in enumerate(src))
            if src else "Sources list is empty."
        )
        back_btn = types.InlineKeyboardButton(text="Back", callback_data="back:main")
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[back_btn]])
        await send_and_replace(callback.bot, callback.from_user.id, text, reply_markup=markup)
        await callback.answer()

    dp.callback_query.register(month, lambda c: c.data.startswith("month:"))
    dp.callback_query.register(main_dates, lambda c: c.data == "main_dates")
    dp.callback_query.register(sources, lambda c: c.data == "sources")
