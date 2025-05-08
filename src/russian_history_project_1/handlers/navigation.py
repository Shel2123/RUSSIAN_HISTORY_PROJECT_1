from aiogram import types, Dispatcher
import logging

from ..keyboards.common import months_keyboard, main_keyboard
from ..utils.messaging import send_and_replace

def register(dp: Dispatcher) -> None:
    async def year(callback: types.CallbackQuery) -> None:
        try:
            _, year_str = callback.data.split(":")
            year = int(year_str)
        except ValueError:
            await callback.answer("Incorrect command")
            return
        logging.info("User %s selected year %s", callback.from_user.id, year)
        kb = months_keyboard(year)
        await send_and_replace(
            callback.bot, callback.from_user.id,
            f"Select month for {year}:", reply_markup=kb
        )
        await callback.answer()

    async def back_main(callback: types.CallbackQuery) -> None:
        await send_and_replace(
            callback.bot, callback.from_user.id,
            "Main Menu:", reply_markup=main_keyboard()
        )
        await callback.answer()

    async def back_year(callback: types.CallbackQuery) -> None:
        try:
            _, year_str = callback.data.split(":")
            year = int(year_str)
        except ValueError:
            await callback.answer("Invalid back data")
            return
        kb = months_keyboard(year)
        await send_and_replace(
            callback.bot, callback.from_user.id,
            f"Select month for {year}:", reply_markup=kb
        )
        await callback.answer()

    dp.callback_query.register(year, lambda c: c.data.startswith("year:"))
    dp.callback_query.register(back_year, lambda c: c.data.startswith("back:") and c.data != "back:main")
    dp.callback_query.register(back_main, lambda c: c.data == "back:main")
