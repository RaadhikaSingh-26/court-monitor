from flask import Flask, render_template, abort
import sqlite3
import requests
import os

app = Flask(__name__)

DB_NAME = "cases.db"
API_KEY = os.getenv("COURTLISTENER_API_KEY")

@app.route("/")
def index():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""
        SELECT case_name, court, date_filed, opinion_id
        FROM protective_orders
        ORDER BY date_filed DESC
    """)

    rows = c.fetchall()
    conn.close()

    cases = []
    for row in rows:
        cases.append({
            "case_name": row["case_name"] or "Unnamed Case",
            "court": row["court"] or "Unknown Court",
            "date_filed": row["date_filed"] or "Unknown Date",
            "opinion_id": row["opinion_id"]
        })

    return render_template("index.html", cases=cases)

@app.route("/opinion/<int:opinion_id>")
def opinion_detail(opinion_id):
    url = f"https://www.courtlistener.com/api/rest/v3/opinions/{opinion_id}/"
    headers = {"Authorization": f"Token {API_KEY}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        abort(404)

    opinion = response.json()
    return render_template("opinion.html", opinion=opinion)

if __name__ == "__main__":
    app.run(debug=True)
