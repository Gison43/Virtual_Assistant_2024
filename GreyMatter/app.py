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
    
    # FIXED: Changed list_name -> name AND item -> items to match list.py
    conn.execute('''CREATE TABLE IF NOT EXISTS lists
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, 
                  items TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # 1. FETCH LISTS
    lists_data = {}
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # FIXED: Select 'name' and 'items' (plural)
            cursor.execute("SELECT name, items FROM lists ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            
            # FIXED: Logic to handle comma-separated strings from list.py
            for name, items_string in rows:
                if name:
                    # Split "milk, eggs" back into ['milk', 'eggs'] for the dashboard
                    val = items_string if items_string else ""
                    # This creates the list structure your HTML expects
                    lists_data[name] = [i.strip() for i in val.split(',') if i.strip()]
                    
    except Exception as e:
        print(f"DB Error (Lists): {e}")

    # 2. FETCH NOTES
    notes_data = []
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT content, timestamp FROM notes ORDER BY id DESC LIMIT 10")
            notes_data = cursor.fetchall()
    except Exception as e:
        print(f"DB Error (Notes): {e}")

    # YOUR ORIGINAL HTML TEMPLATE (Unchanged)
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
    
    # FIXED: Clean and Join items into a single string for storage
    items_list = [i.strip() for i in items_str.split(',') if i.strip()]
    items_final = ", ".join(items_list)

    with sqlite3.connect(db_path) as conn:
        # Check if exists first (Upsert logic)
        cursor = conn.cursor()
        cursor.execute("SELECT items FROM lists WHERE name = ?", (list_name,))
        result = cursor.fetchone()
        
        if result:
            new_items = result[0] + ", " + items_final
            cursor.execute("UPDATE lists SET items = ? WHERE name = ?", (new_items, list_name))
        else:
            cursor.execute("INSERT INTO lists (name, items) VALUES (?, ?)", (list_name, items_final))
            
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
