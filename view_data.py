import sqlite3

conn = sqlite3.connect("cases.db")
cursor = conn.cursor()

cursor.execute("SELECT case_name, court FROM protective_orders")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
