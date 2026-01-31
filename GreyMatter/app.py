from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

LIST_DIR = "GreyMatter/Lists"

def init_db():
    with sqlite3.connect("va_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS lists (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE NOT NULL,
                            items TEXT NOT NULL)''')
        conn.commit()

@app.route('/add_list', methods=['POST'])
def add_list():
    data = request.json
    name = data.get('name')
    items = ",".join(data.get('items', []))

    with sqlite3.connect("va_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO lists (name, items) VALUES (?, ?)", (name, items))
        conn.commit()

    return jsonify({"message": "List added successfully!"})

@app.route('/get_list/<name>', methods=['GET'])
def get_list(name):
    with sqlite3.connect("va_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT items FROM lists WHERE name = ?", (name,))
        row = cursor.fetchone()

    if row:
        return jsonify({"name": name, "items": row[0].split(",")})
    else:
        return jsonify({"message": "List not found!"}), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
