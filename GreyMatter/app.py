from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Standardized path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "memory.db")

def init_db():
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  content TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS lists
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, 
                  items TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    lists_data = {}
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # UPDATED: Using 'name' and 'items' to match list.py
            cursor.execute("SELECT name, items FROM lists ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            
            for list_name, items_string in rows:
                if list_name:
                    # If items_string is None or empty, provide an empty list
                    val = items_string if items_string else ""
                    lists_data[list_name] = [i.strip() for i in val.split(',') if i.strip()]
    except Exception as e:
        print(f"DB Error (Lists): {e}")

    notes_data = []
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT content, timestamp FROM notes ORDER BY timestamp DESC")
            notes_data = cursor.fetchall()
    except Exception as e:
        print(f"DB Error (Notes): {e}")

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>VA Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: sans-serif; background: #121212; color: #e0e0e0; padding: 20px; }
            .card { background: #1e1e1e; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #bb86fc; }
            .tag { background: #3700b3; color: white; padding: 3px 8px; border-radius: 5px; font-size: 0.8em; margin-right: 5px; display: inline-block; margin-top: 5px; }
            h2 { color: #03dac6; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Active Lists</h2>
            {% for name, items in lists.items() %}
                <div class="card">
                    <strong style="color:#bb86fc; text-transform: capitalize;">{{ name }}</strong>
                    <br>
                    {% for item in items %}
                        <span class="tag">{{ item }}</span>
                    {% else %}
                        <span style="color: #666;">(Empty list)</span>
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

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
