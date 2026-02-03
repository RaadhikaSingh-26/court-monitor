import os
import requests
import sqlite3

API_KEY = os.getenv("COURTLISTENER_API_KEY")
BASE_URL = "https://www.courtlistener.com/api/rest/v3/search/"
DB_NAME = "cases.db"

HEADERS = {
    "Authorization": f"Token {API_KEY}"
}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS protective_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_name TEXT,
            court TEXT,
            date_filed TEXT,
            opinion_id INTEGER,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def normalize_date(date_str):
    if not date_str:
        return None
    return date_str.split("T")[0]

def extract_id(url):
    if not url:
        return None
    try:
        return int(url.rstrip("/").split("/")[-1])
    except Exception:
        return None

def fetch_cases():
    params = {
        "q": "protective order",
        "page_size": 50
    }

    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    results = data.get("results", [])
    print(f"Fetched {len(results)} cases")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    inserted = 0

    for item in results:
        case_name = item.get("caseName")
        court = item.get("court")
        date_filed = normalize_date(item.get("dateFiled"))
        opinion_id = extract_id(item.get("opinion"))

        c.execute("""
            INSERT INTO protective_orders
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
