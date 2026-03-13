import sqlite3


conn = sqlite3.connect('railsense.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    code TEXT,
    category TEXT,
    avg_footfall INTEGER,
    booked_seats INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT UNIQUE,
    name TEXT,
    impact_type TEXT,
    multiplier REAL
)
''')


stations_data = [
    ("Mathura Junction", "MTJ", "RELIGIOUS", 50000, 15),
    ("Kota Junction", "KOTA", "EDUCATION", 30000, 50),
    ("Varanasi Cantt", "BSB", "RELIGIOUS", 60000, 20),
    ("New Delhi", "NDLS", "CAPITAL", 200000, 100),
    ("Mumbai Central", "MMCT", "BUSINESS", 150000, 80)
]

events_data = [
    ("2026-03-04", "Holi", "RELIGIOUS", 8.0),
    ("2026-09-04", "Janmashtami", "RELIGIOUS", 10.0),
    ("2026-05-01", "Exam Season", "EDUCATION", 3.5),
    ("2026-01-26", "Republic Day", "CAPITAL", 5.0)
]

cursor.execute('DELETE FROM stations')
cursor.execute('DELETE FROM events')

cursor.executemany('INSERT INTO stations (name, code, category, avg_footfall, booked_seats) VALUES (?,?,?,?,?)', stations_data)
cursor.executemany('INSERT INTO events (date, name, impact_type, multiplier) VALUES (?,?,?,?)', events_data)

conn.commit()
print("✅ Database 'railsense.db' successfully created with 5 Stations & 4 Events!")
conn.close()