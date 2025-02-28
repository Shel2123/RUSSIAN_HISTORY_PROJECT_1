import sqlite3

# Кэш для запросов к базе данных
events_cache = {}       # ключ: (year, month) -> список событий [(day, description), ...]
main_dates_cache = None  # кэш для списка главных дат
sources_cache = None     # кэш для списка источников

def get_events(year: int, month: int):
    """Получить список событий (дата и описание) для заданного года и месяца с кэшированием."""
    global events_cache
    key = (year, month)
    if key in events_cache:
        return events_cache[key]
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()
    cur.execute("SELECT day, description FROM events WHERE year=? AND month=? ORDER BY day", (year, month))
    rows = cur.fetchall()
    conn.close()
    events_cache[key] = rows
    return rows

def get_main_dates():
    """Получить список главных дат (дата и краткое описание) с кэшированием."""
    global main_dates_cache
    if main_dates_cache is not None:
        return main_dates_cache
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()
    cur.execute("SELECT date, short_description FROM main_dates ORDER BY date")
    rows = cur.fetchall()
    conn.close()
    main_dates_cache = rows
    return rows

def get_sources():
    """Получить список источников с кэшированием."""
    global sources_cache
    if sources_cache is not None:
        return sources_cache
    conn = sqlite3.connect("events.db")
    cur = conn.cursor()
    cur.execute("SELECT source FROM sources")
    rows = [row[0] for row in cur.fetchall()]
    conn.close()
    sources_cache = rows
    return rows
