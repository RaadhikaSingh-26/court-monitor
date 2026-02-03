import requests
import sqlite3
import os

DB_NAME = "cases.db"
API_KEY = os.getenv("COURTLISTENER_API_KEY")

SEARCH_URL = "https://www.courtlistener.com/api/rest/v3/search/"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS protective_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_name TEXT,
            court TEXT,
            date_filed TEXT,
            opinion_id INTEGER UNIQUE,
            UNIQUE(case_name, court, date_filed)
        )
    """)

    conn.commit()
    conn.close()


def fetch_cases():
    if not API_KEY:
        print("API key not set. Skipping fetch.")
        return

    headers = {
        "Authorization": f"Token {API_KEY}"
    }

    params = {
        "q": "protective order",
        "page_size": 50
    }

    response = requests.get(SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    inserted = 0

    for item in results:
        case_name = item.get("caseName")
        court = item.get("court")
        date_filed = item.get("dateFiled")
        opinion_id = item.get("opinion_id")

        if not case_name:
            continue

        # clean date (YYYY-MM-DD)
        if date_filed and "T" in date_filed:
            date_filed = date_filed.split("T")[0]

        c.execute("""
            INSERT OR IGNORE INTO protective_orders
            (case_name, court, date_filed, opinion_id)
            VALUES (?, ?, ?, ?)
        """, (case_name, court, date_filed, opinion_id))

        inserted += 1

    conn.commit()
    conn.close()

    print(f"Inserted {inserted} cases")


if __name__ == "__main__":
    init_db()
    fetch_cases()
