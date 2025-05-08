import sqlite3
from pathlib import Path

DB_PATH = Path("events.db")

rows = [
    "David Stahel, Operation Barbarossa and Germany’s Defeat in the East (Cambridge University Press, 2010). A detailed academic study of the invasion and its strategic failures — Wikipedia.",
    "Richard Overy, Russia’s War: A History of the Soviet Effort: 1941–1945 (Penguin Books, 1995; revised ed. 2015). A concise, accessible overview of the Soviet war effort and key battles — Amazon / PenguinRandomHouse.com.",
    "John Erickson, The Road to Stalingrad: Stalin’s War with Germany, Volume 1 (Yale University Press, 1975; reprint 1999). The first volume of a seminal two-part history covering Barbarossa through Stalingrad — Yale University Press.",
    "John Erickson, The Road to Berlin: Stalin’s War with Germany, Volume 2 (Yale University Press, 1975). Continues the narrative from Stalingrad to the fall of Berlin — Yale University Press.",
    "David M. Glantz & Jonathan M. House, When Titans Clashed: How the Red Army Stopped Hitler (University Press of Kansas, 1995; rev. ed. 2015). A comprehensive operational history of the Eastern Front’s major engagements — kansaspress.ku.edu.",
]

def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            source TEXT NOT NULL
        )
    """)

    cur.execute("DELETE FROM sources")
    cur.executemany("INSERT INTO sources(source) VALUES (?)",
                    [(r,) for r in rows])

    conn.commit()
    conn.close()
    print("✅  sources заполнена")

if __name__ == "__main__":
    main()
