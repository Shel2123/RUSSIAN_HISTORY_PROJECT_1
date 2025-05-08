"""
Lightweight Data Access Layer with simple in‑memory caching.
Caches are automatically invalidated on process restart.
"""
import sqlite3
from functools import lru_cache
from typing import List, Tuple

from .config import DB_PATH

@lru_cache(maxsize=32)
def _fetch_events(year: int, month: int) -> Tuple[Tuple[int, str], ...]:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT day, description FROM events WHERE year=? AND month=? ORDER BY day",
            (year, month),
        )
        return tuple(cur.fetchall())

def get_events(year: int, month: int) -> List[Tuple[int, str]]:
    return list(_fetch_events(year, month))

@lru_cache(maxsize=1)
def get_main_dates() -> Tuple[Tuple[str, str], ...]:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT date, short_description FROM main_dates ORDER BY date"
        )
        return tuple(cur.fetchall())

@lru_cache(maxsize=1)
def get_sources() -> Tuple[str, ...]:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT source FROM sources")
        return tuple(row[0] for row in cur.fetchall())
