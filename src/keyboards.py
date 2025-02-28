from aiogram import types

def get_main_keyboard():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Year 1941", callback_data="command_1"),
            types.InlineKeyboardButton(text="Year 1942", callback_data="command_2")
        ],
        [
            types.InlineKeyboardButton(text="Year 1943", callback_data="command_3"),
            types.InlineKeyboardButton(text="Year 1944", callback_data="command_4"),
            types.InlineKeyboardButton(text="Year 1945", callback_data="command_5")
        ],
        [
            types.InlineKeyboardButton(text="Main Dates", callback_data="command_6")
        ],
        [
            types.InlineKeyboardButton(text="Sources", callback_data="command_7")
        ]
    ])

def get_months_keyboard(year: int):
    month_names = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    for m in range(1, 13):
        btn = types.InlineKeyboardButton(text=month_names[m-1], callback_data=f"month:{year}:{m}")
        keyboard.inline_keyboard.append([btn])
    back_btn = types.InlineKeyboardButton(text="Back", callback_data="back_main")
    keyboard.inline_keyboard.append([back_btn])
    return keyboard
