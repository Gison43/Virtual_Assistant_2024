from flask import Flask, request, jsonify, render_template_string
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
@app.route('/')
def index():
    # This fetches all your lists from the database to show on the website
    with sqlite3.connect("va_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, items FROM lists")
        all_lists = cursor.fetchall()

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>VA Control Center</title>
        <style>
            body { font-family: sans-serif; background: #121212; color: #e0e0e0; text-align: center; }
            .container { max-width: 600px; margin: auto; padding: 20px; }
            .list-card { background: #1e1e1e; border: 1px solid #333; padding: 15px; margin: 10px; border-radius: 8px; text-align: left; }
            h1 { color: #bb86fc; }
            .status { color: #03dac6; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Assistant Dashboard</h1>
            <p>System Status: <span class="status">Online</span></p>
            <hr>
            <h2>My Saved Lists</h2>
            {% for name, items in lists %}
                <div class="list-card">
                    <strong>{{ name }}:</strong> {{ items }}
                </div>
            {% else %}
                <p>No lists found in database.</p>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, lists=all_lists)

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
