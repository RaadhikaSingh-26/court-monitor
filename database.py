import sqlite3

conn = sqlite3.connect("cases.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS protective_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_name TEXT,
    court TEXT,
    snippet TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database initialized")
