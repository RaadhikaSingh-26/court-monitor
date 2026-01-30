print("Running daily protective order fetch...")

import requests
import sqlite3

API_KEY = "ceb5359bc7d09f2e1a5e7be98216e73a10873190"

url = "https://www.courtlistener.com/api/rest/v3/search/?q=protective+order"

headers = {
    "Authorization": f"Token {API_KEY}",
    "User-Agent": "court-monitor-learning-project (contact: test@example.com)"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Error fetching data")
    exit()

data = response.json()

conn = sqlite3.connect("cases.db")
cursor = conn.cursor()

for result in data["results"]:
    case_name = result.get("caseName")
    court = result.get("court")
    snippet = result.get("snippet")

    cursor.execute("""
    INSERT INTO protective_orders (case_name, court, snippet)
    VALUES (?, ?, ?)
    """, (case_name, court, snippet))

conn.commit()
conn.close()

print("Protective order cases saved to database")
