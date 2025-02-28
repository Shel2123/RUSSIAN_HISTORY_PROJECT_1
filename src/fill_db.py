import sqlite3
import csv

# Создаем подключение к базе данных (файл events.db)
conn = sqlite3.connect('events.db')
cur = conn.cursor()

# Создаем таблицу events, если она не существует
cur.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    description TEXT
)
''')

# Открываем CSV-файл с данными (убедитесь, что файл находится в той же директории или укажите полный путь)
with open('events.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Вставляем данные в таблицу
        cur.execute('''
            INSERT INTO events (year, month, day, description)
            VALUES (?, ?, ?, ?)
        ''', (int(row['year']), int(row['month']), int(row['day']), row['description']))

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
