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
        SELECT id, case_name, court, date_filed, opinion_id
        FROM protective_orders
        ORDER BY date_filed DESC
    """)

    rows = c.fetchall()
    conn.close()

    cases = []
    for row in rows:
        cases.append({
            "id": row["id"],
            "case_name": row["case_name"],
            "court": row["court"],
            "date_filed": row["date_filed"],
            "opinion_id": row["opinion_id"]
        })

    return render_template("index.html", cases=cases)

@app.route("/case/<int:case_id>")
def case_detail(case_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""
        SELECT case_name, court, date_filed, opinion_id
        FROM protective_orders
        WHERE id = ?
    """, (case_id,))

    case = c.fetchone()
    conn.close()

    if not case:
        abort(404)

    opinion = None

    if case["opinion_id"]:
        url = f"https://www.courtlistener.com/api/rest/v3/opinions/{case['opinion_id']}/"
        headers = {"Authorization": f"Token {API_KEY}"}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            opinion = r.json()

    return render_template(
        "case_detail.html",
        case=case,
        opinion=opinion
    )

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
