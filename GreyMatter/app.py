from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# --- CRITICAL PATH FIX ---
# This ensures app.py ALWAYS looks in GreyMatter/memory.db, no matter where you run it from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "memory.db")

def init_db():
    conn = sqlite3.connect(db_path)
    # Ensure TABLES match the schema used by list.py and notes.py
    conn.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  content TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS lists
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, 
                  item TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # 1. FETCH LISTS (Grouped by List Name)
    lists_data = {}
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Select distinct lists and their items
            cursor.execute("SELECT list_name, item FROM lists ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            
            # Group items: {'grocery': ['apples', 'bananas'], 'lab': ['beakers']}
            for list_name, item in rows:
                if list_name not in lists_data:
                    lists_data[list_name] = []
                lists_data[list_name].append(item)
    except Exception as e:
        print(f"DB Error (Lists): {e}")

    # 2. FETCH NOTES
    notes_data = []
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Use 'content' and 'timestamp' to match notes.py
            cursor.execute("SELECT content, timestamp FROM notes ORDER BY id DESC LIMIT 10")
            notes_data = cursor.fetchall()
    except Exception as e:
        print(f"DB Error (Notes): {e}")

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>VA Control Center</title>
        <meta name="viewport" content="width=device-width, initial_scale=1">
        <style>
            body { font-family: sans-serif; background: #121212; color: #e0e0e0; text-align: center; padding: 10px; }
            .container { max-width: 600px; margin: auto; }
            .card { background: #1e1e1e; border: 1px solid #333; padding: 15px; margin: 15px 0; border-radius: 8px; text-align: left; }
            h2 { color: #03dac6; border-bottom: 1px solid #333; padding-bottom: 5px; }
            .tag { background: #bb86fc; color: black; padding: 2px 6px; border-radius: 4px; font-size: 0.8em; margin-right: 5px; display: inline-block; margin-bottom: 5px;}
            input, button { padding: 10px; width: 100%; margin-top: 5px; box-sizing: border-box; }
            button { background: #03dac6; border: none; font-weight: bold; cursor: pointer; color: #000; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Virtual Assistant</h1>
            
            <div class="card">
                <h3>Create/Add to List</h3>
                <form action="/add_list_web" method="POST">
                    <input type="text" name="list_name" placeholder="List Name (e.g. grocery)" required>
                    <input type="text" name="list_items" placeholder="Items (comma separated)" required>
                    <button type="submit">Save</button>
                </form>
            </div>

            <h2>My Lists</h2>
            {% for name, items in lists.items() %}
                <div class="card">
                    <strong style="color:#bb86fc; text-transform: capitalize;">{{ name }}</strong>
                    <br>
                    {% for item in items %}
                        <span class="tag">{{ item }}</span>
                    {% endfor %}
                </div>
            {% else %}
                <p>No lists found.</p>
            {% endfor %}

            <h2>Recent Notes</h2>
            {% for note, date in notes %}
                <div class="card">
                    <div style="color: #888; font-size: 0.8em;">{{ date }}</div>
                    {{ note }}
                </div>
            {% else %}
                <p>No notes found.</p>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, lists=lists_data, notes=notes_data)

@app.route('/add_list_web', methods=['POST'])
def add_list_web():
    list_name = request.form.get('list_name').lower().strip()
    items_str = request.form.get('list_items')
    
    # Split items by comma and clean them
    items = [i.strip() for i in items_str.split(',') if i.strip()]

    with sqlite3.connect(db_path) as conn:
        for item in items:
            conn.execute("INSERT INTO lists (list_name, item) VALUES (?, ?)", (list_name, item))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
