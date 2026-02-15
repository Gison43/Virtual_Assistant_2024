from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import sqlite3
import subprocess
from datetime import datetime

app = Flask(__name__)

#LIST_DIR = "GreyMatter/Lists"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "memory.db")

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Adding 'id' as the PRIMARY KEY fixes the "no column id" error
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  content TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

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
    with sqlite3.connect("memory.db") as conn:
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
            body { font-family: sans-serif; background: #121212; color: #e0e0e0; text-align: center;font-size:18px; }
            .container { max-width: 600px; margin: auto; padding: 15px; }
            .card { background: #1e1e1e; border: 1px solid #333; padding: 20px; margin: 15px 0; border-radius: 12px; text-align: left;font-size: 1.1rem; }
            h1 { color: #bb86fc; font-size: 2.2rem; }
            h2 { color: #03dac6; font-size: 1.8rem; margin-top: 30px; }
            h3 { margin-top: 0; color: #bb86fc; }

            .status { color: #03dac6; font-weight: bold; }

            button { background: #03dac6; color: black; border: none; padding: 15px 25px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 1rem; width: 100%; margin-top: 10px; }
            .fix-btn { background: #cf6679; margin-bottom: 20px; }
            input[type="text"] { width: 100%; box-sizing: border-box; padding: 15px; margin: 10px 0; border-radius: 8px; border: 1px solid #333; background: #2c2c2c; color: white;font-size: 1rem; }
            hr { border: 0; border-top: 1px solid #333; margin: 40px 0; }
            small { font-size: 0.9rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Assistant Dashboard</h1>
            <p>System Status: <span class="status">Online</span></p>
            <a href="/fix_audio_web"><button class="fix-btn">Fix Audio Issue</button></a>
            
            <div class="card">
                <h3>📝 Create New List</h3>
                <form action="/add_list_web" method="POST">
                    <input type="text" name="list_name" placeholder="List Name (e.g. Groceries)" required><br>
                    <input type="text" name="list_items" placeholder="Items (comma separated)" required><br>
                    <button type="submit">Save List</button>
                </form>
            </div>

            <div class="card">
                <h3>📓 Quick Note</h3>
                <form action="/add_note_web" method="POST">
                    <input type="text" name="note_text" placeholder="Type a note..." required><br>
                    <button type="submit">Save Note</button>
                </form>
            </div>

            <hr>

            <h2>Recent Notes</h2>
            {% for note, date in notes %}
                <div class="card">
                    <small style="color: #888;">{{ date }}</small><br>
                    {{ note }}
                </div>
            {% else %}
                <p>No notes found in memory.db.</p>
            {% endfor %}

            <hr>

            <h2>My Saved Lists</h2>
            {% for name, items in lists %}
                <div class="card">
                    <strong style="color: #03dac6;">{{ name }}:</strong> {{ items }}
                </div>
            {% else %}
                <p>No lists found in memory.db.</p>
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

    with sqlite3.connect("memory.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO lists (name, items) VALUES (?, ?)", (name, items))
        conn.commit()

    return jsonify({"message": "List added successfully!"})

@app.route('/get_list/<name>', methods=['GET'])
def get_list(name):
    search_name = name.lower()
    with sqlite3.connect("memory.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT items FROM lists WHERE LOWER(name) = ?", (search_name,))
        row = cursor.fetchone()
    if row:
        return jsonify({"name": name, "items": row[0].split(",")})
    else:
        return jsonify({"message": "List not found!"}), 404

@app.route('/add_list_web', methods=['POST'])
def add_list_web():
    # This pulls data from the HTML form fields
    name = request.form.get('list_name')
    items = request.form.get('list_items')
    with sqlite3.connect("memory.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO lists (name, items) VALUES (?, ?)", (name, items))
        conn.commit()
    return redirect(url_for('index'))
    
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
    SB_NAME = "alsa_output.platform-bcm2835_audio.analog-stereo"
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
