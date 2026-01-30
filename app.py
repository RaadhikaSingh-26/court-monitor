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
    app.run(debug=True)
