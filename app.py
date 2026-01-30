from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_cases():
    conn = sqlite3.connect("cases.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT case_name, court, snippet, created_at
        FROM protective_orders
        ORDER BY created_at DESC
        LIMIT 50
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route("/")
def home():
    cases = get_cases()
    return render_template("index.html", cases=cases)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

