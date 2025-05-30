import sqlite3
import os

db_path = os.path.join('shared', 'database.db')

os.makedirs('shared', exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    tg_username TEXT,
    manifest TEXT
)
''')

conn.commit()
conn.close()

print("База данных успешно создана!")
