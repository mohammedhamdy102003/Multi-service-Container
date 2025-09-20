from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

def get_visits():
    conn = psycopg2.connect(
        host="db",
        database="appdb",
        user="appuser",
        password="apppass"
    )
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (count INT);")
    cur.execute("SELECT count(*) FROM visits;")
    rows = cur.fetchone()[0]
    if rows == 0:
        cur.execute("INSERT INTO visits VALUES (1);")
    else:
        cur.execute("UPDATE visits SET count = count + 1;")
    cur.execute("SELECT * FROM visits;")
    visits = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return visits

@app.route("/visits")
def visits():
    count = get_visits()
    return jsonify({"visits": count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

