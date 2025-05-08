"""
Registers all sub‑handlers with the dispatcher.
Each sub‑module exposes a `register(dp: Dispatcher)` function.
"""
from aiogram import Dispatcher
from . import start, navigation, events, fallback

def register_handlers(dp: Dispatcher) -> None:
    for module in (start, navigation, events, fallback):
        module.register(dp)
