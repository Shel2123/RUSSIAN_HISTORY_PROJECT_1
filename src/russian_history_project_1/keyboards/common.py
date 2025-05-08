from aiogram import types
from typing import List, Tuple


_ALL_MONTHS: List[Tuple[int, str]] = [
    (1,  "January"), (2,  "February"), (3,  "March"), (4,  "April"),
    (5,  "May"),     (6,  "June"),     (7,  "July"),  (8,  "August"),
    (9,  "September"), (10, "October"), (11, "November"), (12, "December"),
]

YEARS: List[int] = [1941, 1942, 1943, 1944, 1945]

def main_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[])
    year_buttons = [
        types.InlineKeyboardButton(text=f"Year {year}", callback_data=f"year:{year}")
        for year in YEARS
    ]

    kb.inline_keyboard.append(year_buttons[:2])
    kb.inline_keyboard.append(year_buttons[2:])
    kb.inline_keyboard.append([types.InlineKeyboardButton(text="Main Dates", callback_data="main_dates")])
    kb.inline_keyboard.append([types.InlineKeyboardButton(text="Sources", callback_data="sources")])
    return kb

def months_keyboard(year: int) -> types.InlineKeyboardMarkup:
    if year == 1941:
        months = [m for m in _ALL_MONTHS if m[0] >= 6]          # c июня
    elif year == 1945:
        months = [m for m in _ALL_MONTHS if m[0] <= 5]          # по май
    else:
        months = _ALL_MONTHS                                     # весь год

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=name, callback_data=f"month:{year}:{num}")]
        for num, name in months
    ])
    kb.inline_keyboard.append([types.InlineKeyboardButton(text="Back", callback_data="back:main")])
    return kb

