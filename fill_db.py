import re, sqlite3
from datetime import datetime
from pathlib import Path
from docx import Document

DB = "events.db"
DOCX = "Dates, History project.docx"

month_to_num = {
    m: i for i, m in enumerate(
        ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"], start=1)
}

def iter_events(docx_path: str):
    doc = Document(docx_path)
    current_year = current_month = None

    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue

        m = re.match(r"^([A-Za-z]+)\s+(\d{4}):?$", text)
        if m and m.group(1) in month_to_num:
            current_month = month_to_num[m.group(1)]
            current_year = int(m.group(2))
            continue

        if current_year and current_month:
            d = re.search(r"\b(\d{1,2})\b", text)
            day = int(d.group(1)) if d else 1
            yield current_year, current_month, day, text

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("DELETE FROM events")   # если нужно «перезалить»
    cur.executemany(
        "INSERT INTO events (year, month, day, description) VALUES (?, ?, ?, ?)",
        iter_events(DOCX)
    )
    conn.commit()
    conn.close()
    print("✅  events заполнена")

if __name__ == "__main__":
    main()
