import sqlite3
import os
from datetime import datetime, timedelta
from GreyMatter.SenseCells.tts_engine import tts
from user_input import get_user_input

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "memory.db")

def note_something(speech_text):
  conn = sqlite3.connect(db_path)
  words_of_message = speech_text.split ()
  if 'note' in words_of_message: words_of_message.remove ('note')
  cleaned_message = ' '.join (words_of_message)
  
  conn.execute("INSERT INTO notes (content, timestamp) VALUES (?, ?)", 
               (cleaned_message, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
  conn.commit()
  conn.close()
  tts('your note has been saved.')

def handle_notes(speech_text):
    """
    Handles reading and deleting notes based on user's command.
    This centralizes all note management logic in notes.py.
    """
    action = None
  
    if 'read' in speech_text:
      action = 'read'
    elif 'delete' in speech_text:
      action = 'delete'
    
    if not action:
      tts("I did not understand if you want to read or delete notes.")

    date = None
    
    if 'today' in speech_text:
      date = datetime.now().strftime("%d-%m-%Y")

    elif 'yesterday' in speech_text:
      date = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")

    elif 'tomorrow' in speech_text:
      date = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")

    elif any(keyword in speech_text for keyword in ['all', 'everything']) and action == 'delete':
      #special case: delete all notes
      date = None

    if date is None and action == 'read':
      #ask for a date if none was specified
      tts("What date would you like to work with?")
      date = get_user_input()

    if date is None and action == 'delete':
      tts("Are you sure you want to delete all notes?  Yes or no.")
      confirmation = get_user_input().strip().lower()
      if confirmation != 'yes':
        tts("Ok, I won't delete anything.")
        return

    if action == 'read':
      read_notes(date)
    elif action == 'delete':
      delete_notes(date)

def delete_notes(date=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if date == "today":
        search_date = datetime.now().strftime("%Y-%m-%d")
    elif date == "yesterday":
        search_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    elif date == "tomorrow":
        search_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        search_date = date

    if date is None:
        tts("Deleting all notes from the database.")
        cursor.execute("DELETE FROM notes")
    else:
        cursor.execute("DELETE FROM notes WHERE timestamp LIKE ?", (f"{search_date}%",))
        tts(f"Notes for {date} deleted.")

    conn.commit()
    conn.close()

def read_notes(date=None):
    tts("Let me check your notes. One moment please.")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Handle keywords for lab convenience
    if date == "today" or not date:
        search_date = datetime.now().strftime("%Y-%m-%d")
    elif date == "yesterday":
        search_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    elif date == "tomorrow":
        search_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        # If a specific date like "15-02-2026" was passed, convert it to "2026-02-15"
        try:
            search_date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
        except:
            search_date = date

    # Query using 'content' and 'timestamp' to match the website
    cursor.execute("SELECT content FROM notes WHERE timestamp LIKE ?", (f"{search_date}%",))
    notes = cursor.fetchall()
    conn.close()

    if notes:
        tts(f"Here are your notes for {date if date else 'today'}:")
        for note in notes:
            print(f"- {note[0]}")
            tts(note[0])
    else:
        tts(f"I found no notes for {date if date else 'today'}.")

def show_all_notes():
    tts("Checking all saved notes.")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # We use 'content' here to match the website's database structure
        cursor.execute("SELECT content FROM notes ORDER BY timestamp DESC")
        notes = cursor.fetchall()
        conn.close()

        if notes:
            tts(f"You have {len(notes)} notes saved.")
            for note in notes:
                print(f"- {note[0]}")
                tts(note[0])
        else:
            tts("Your notebook is currently empty.")
            
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        tts("I encountered a problem reading the database.")
