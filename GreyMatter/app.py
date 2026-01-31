from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import sqlite3
import subprocess
from datetime import datetime

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

# Helper to connect to the notes database
def get_notes():
    try:
        with sqlite3.connect('memory.db') as conn:
            cursor = conn.cursor()
            # Grabbing the last 10 notes so the page isn't too long
            cursor.execute("SELECT notes, notes_date FROM notes ORDER BY id DESC LIMIT 10")
            return cursor.fetchall()
    except Exception as e:
        print(f"Database error: {e}")
        return []

@app.route('/')
def index():
    # This fetches all your lists from the database to show on the website
    with sqlite3.connect("va_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, items FROM lists")
        all_lists = cursor.fetchall()

    #fetch notes (memory.db)
    all_notes = get_notes()

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
            button { background: #cf6679; color: black; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; }
            button:hover { background: #b00020; color: white; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Assistant Dashboard</h1>
            <p>System Status: <span class="status">Online</span></p>

            <p><a href="/fix_audio_web"><button>Fix Audio Issue</button></a><p>
            
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
    return render_template_string(html_template, lists=all_lists, notes=all_notes)

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

@app.route('/add_note_web', methods=['POST'])
def add_note_web():
    note_text = request.form.get('note_text')
    date_str = datetime.now().strftime('%d-%m-%Y')
    
    with sqlite3.connect('memory.db') as conn:
        conn.execute("INSERT INTO notes (notes, notes_date) VALUES (?, ?)", (note_text, date_str))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/fix_audio_web')
def fix_audio_web():
    import subprocess
    SB_NAME = "alsa_output.usb-Creative_Technology_Ltd_Sound_Blaster_Play__3_00311390-00.analog-stereo"
    try:
        subprocess.run(["pactl", "set-default-sink", SB_NAME], check=True)
        subprocess.run(["pactl", "set-sink-mute", SB_NAME, "0"], check=True)
        subprocess.run(["pactl", "set-sink-volume", SB_NAME, "85%"], check=True)
        print("Audio fixed via Web Dashboard")
    except Exception as e:
        print(f"Web Audio Fix Failed: {e}")
    
    return redirect(url_for('index')) # This sends you back to the dashboard immediately

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
