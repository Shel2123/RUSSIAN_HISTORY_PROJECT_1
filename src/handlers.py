from aiogram import types, Dispatcher
from aiogram.filters import Command
import logging
from keyboards import get_main_keyboard, get_months_keyboard
from data_handlers import get_events, get_main_dates, get_sources


last_messages = {}

def register_handlers(dp: Dispatcher, bot):
    async def send_message_with_deletion(user_id: int, text: str, reply_markup=None):
        """Отправляет сообщение и удаляет предыдущее, если оно есть."""
        if user_id in last_messages:
            try:
                await bot.delete_message(chat_id=user_id, message_id=last_messages[user_id])
            except Exception as e:
                logging.warning(f"Не удалось удалить сообщение: {e}")

        # Отправляем новое сообщение
        msg = await bot.send_message(user_id, text, reply_markup=reply_markup)
        last_messages[user_id] = msg.message_id
    
    # Обработчик команды /start и /help
    async def send_welcome(message: types.Message):
        user = message.from_user
        logging.info(f"User {user.id} ({user.full_name}) started the bot.")
        keyboard = get_main_keyboard()
        welcome_text = (
            f"Hi, {message.from_user.full_name}, I am a telegram bot for studying the chronology of the Great Patriotic War."
        )
        await send_message_with_deletion(user.id, welcome_text, reply_markup=keyboard)

    dp.message.register(send_welcome, Command(commands=["start", "help"]))

    # Обработчик выбора года (Year 1941 ... Year 1945)
    async def process_year(callback: types.CallbackQuery):
        mapping = {
            "command_1": 1941,
            "command_2": 1942,
            "command_3": 1943,
            "command_4": 1944,
            "command_5": 1945
        }
        year = mapping.get(callback.data)
        logging.info(f"User {callback.from_user.id} ({callback.from_user.full_name}) selected year {year}.")
        months_keyboard = get_months_keyboard(year)
        await send_message_with_deletion(callback.from_user.id, f"Select month for {year}:", reply_markup=months_keyboard)
        await callback.answer()

    dp.callback_query.register(
        process_year,
        lambda c: c.data in ["command_1", "command_2", "command_3", "command_4", "command_5"]
    )

    # Обработчик выбора месяца (например, month:1941:6)
    async def process_month(callback: types.CallbackQuery):
        user = callback.from_user
        try:
            _, year_str, month_str = callback.data.split(":")
        except ValueError:
            await callback.answer("Invalid callback data.")
            return
        year = int(year_str)
        month = int(month_str)
        logging.info(f"User {user.id} ({user.full_name}) requested events for {month:02d}.{year}.")
        events = get_events(year, month)
        month_names = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]
        if events:
            event_lines = [f"{day} {month_names[month-1]} {year} — {description}" for day, description in events]
            header = f"Events for {month_names[month-1]} {year}:\n"
            reply_text = header + "\n".join(event_lines)
        else:
            reply_text = f"No events for {month_names[month-1]} {year} in the database."
        back_btn = types.InlineKeyboardButton(text="Back", callback_data=f"back:{year}")
        back_kb = types.InlineKeyboardMarkup(inline_keyboard=[[back_btn]])
        await send_message_with_deletion(user.id, reply_text, reply_markup=back_kb)
        await callback.answer()

    dp.callback_query.register(
        process_month,
        lambda c: c.data and c.data.startswith("month:")
    )

    # Обработчик кнопки "Main Dates"
    async def process_main_dates(callback: types.CallbackQuery):
        user = callback.from_user
        logging.info(f"User {user.id} ({user.full_name}) requested main dates list.")
        main_dates = get_main_dates()
        if main_dates:
            lines = [f"{date} — {short_desc}" for date, short_desc in main_dates]
            text = "Main Dates of the Great Patriotic War:\n" + "\n".join(lines)
        else:
            text = "Main dates list is currently unavailable."
        back_btn = types.InlineKeyboardButton(text="Back", callback_data="back_main")
        back_kb = types.InlineKeyboardMarkup(inline_keyboard=[[back_btn]])
        await send_message_with_deletion(user.id, text, reply_markup=back_kb)
        await callback.answer()

    dp.callback_query.register(process_main_dates, lambda c: c.data == "command_6")

    # Обработчик кнопки "Sources"
    async def process_sources(callback: types.CallbackQuery):
        user = callback.from_user
        logging.info(f"User {user.id} ({user.full_name}) requested sources list.")
        sources = get_sources()
        if sources:
            lines = [f"{idx+1}. {src}" for idx, src in enumerate(sources)]
            text = "Sources:\n" + "\n".join(lines)
        else:
            text = "Sources list is currently unavailable."
        back_btn = types.InlineKeyboardButton(text="Back", callback_data="back_main")
        back_kb = types.InlineKeyboardMarkup(inline_keyboard=[[back_btn]])
        await send_message_with_deletion(user.id, text, reply_markup=back_kb)
        await callback.answer()

    dp.callback_query.register(process_sources, lambda c: c.data == "command_7")

    # Обработчик кнопки "Back" (в главное меню)
    async def process_back_main(callback: types.CallbackQuery):
        user = callback.from_user
        logging.info(f"User {user.id} ({user.full_name}) returned to main menu.")
        await send_message_with_deletion(user.id, "Main Menu:", reply_markup=get_main_keyboard())
        await callback.answer()

    dp.callback_query.register(process_back_main, lambda c: c.data == "back_main")

    # Обработчик кнопки "Back" для возврата к выбору месяца конкретного года
    async def process_back_year(callback: types.CallbackQuery):
        user = callback.from_user
        try:
            _, year_str = callback.data.split(":")
        except ValueError:
            await callback.answer("Invalid callback data.")
            return
        year = int(year_str)
        logging.info(f"User {user.id} ({user.full_name}) went back to month selection for year {year}.")
        months_keyboard = get_months_keyboard(year)
        await send_message_with_deletion(user.id, f"Select month for {year}:", reply_markup=months_keyboard)
        await callback.answer()

    dp.callback_query.register(
        process_back_year,
        lambda c: c.data and c.data.startswith("back:") and c.data != "back_main"
    )

    # Обработчик неизвестных сообщений – вывод главного меню
    async def echo_unknown(message: types.Message):
        user = message.from_user
        logging.info(f"User {user.id} ({user.full_name}) sent unknown message: {message.text}")
        await send_message_with_deletion(user.id, "Please use the buttons below to navigate.", reply_markup=get_main_keyboard())

    dp.message.register(echo_unknown)
