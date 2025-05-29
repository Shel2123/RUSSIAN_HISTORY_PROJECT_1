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
        text = (
            "Sources:\n"
            "1. Stahel, D. (2009). Operation Barbarossa and Germany's defeat in the East. Cambridge University Press.\n"
            "2. Overy, R. J. (1998). Russia's War: A History of the Soviet Effort: 1941-1945. Penguin UK.\n"
            "3. Erickson, J. (2019). The Road to Stalingrad: Stalin's War with Germany. Routledge.\n"
            "4. Erickson, J. (1984). Threat identification and strategic appraisal by the Soviet Union, 1930-1941. Knowing One’s Enemies: Intelligence Assessment before the Two World Wars, 375-423.\n"
            "5. Glantz, D. M., & House, J. M. (2015). When titans clashed: how the Red Army stopped Hitler. University Press of Kansas.\n"
            "6. Druzhinina, A. (2020). Огонь войны: 1418 дней. thefireofthewar.ru"
        )
        back_btn = types.InlineKeyboardButton(text="Back", callback_data="back:main")
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[back_btn]])
        await send_and_replace(callback.bot, callback.from_user.id, text, reply_markup=markup)
        await callback.answer()

    dp.callback_query.register(month, lambda c: c.data.startswith("month:"))
    dp.callback_query.register(main_dates, lambda c: c.data == "main_dates")
    dp.callback_query.register(sources, lambda c: c.data == "sources")
