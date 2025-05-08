import sqlite3
from pathlib import Path

DB_PATH = Path("events.db")

rows = [
    ("1941-06-22", "Operation Barbarossa: Nazi Germany and its Axis partners invade the Soviet Union along a 2,900 km front, initiating the largest land campaign in history."),
    ("1941-09-08", "Siege of Leningrad begins: German and Finnish forces complete the blockade, starting an 872-day siege that would cost over a million civilian lives."),
    ("1941-12-06", "Moscow counter-offensive: The Red Army launches a major winter counterattack, pushing German forces back from the Moscow suburbs."),
    ("1942-07-17/1943-02-02", "Battle of Stalingrad: One of the bloodiest battles ever, ending with the encirclement and surrender of the German 6th Army."),
    ("1943-07-05/1943-07-12", "Battle of Kursk: The largest tank battle in history, where Soviet defenses blunted Germany’s last major eastern offensive."),
    ("1944-06-22", "Operation Bagration: Massive Soviet summer offensive that shattered Army Group Center and liberated much of Belorussia."),
    ("1945-01-12", "Vistula–Oder Offensive: Rapid Soviet advance from the Vistula to the Oder, bringing them within sight of Berlin."),
    ("1945-04-16", "Battle of Berlin begins: The final major offensive in Europe, leading to the fall of Berlin and the end of Nazi Germany."),
    ("1945-05-09", "Soviet Victory Day: Celebrated the day after Germany’s unconditional surrender took effect, marking the end of the Great Patriotic War."),
]

def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS main_dates(
            date TEXT NOT NULL,
            short_description TEXT NOT NULL
        )
    """)

    cur.execute("DELETE FROM main_dates")
    cur.executemany(
        "INSERT INTO main_dates(date, short_description) VALUES (?, ?)",
        rows,
    )
    conn.commit()
    conn.close()
    print("✅  main_dates заполнена")

if __name__ == "__main__":
    main()
