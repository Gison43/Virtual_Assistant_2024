import sqlite3
from datetime import datetime
from datetime import timedelta

from GreyMatter.SenseCells.tts_engine import tts

def note_something(speech_text):
  conn = sqlite3.connect('memory.db')
  words_of_message = speech_text.split ()
  words_of_message.remove ('note')
  cleaned_message = ' '.join (words_of_message)
  
  conn.execute ("INSERT INTO notes (notes, notes_date) VALUES (?, ? )", (cleaned_message, datetime.strftime(datetime.now(), '%d-%m-%Y')))
  conn.commit()
  conn.close()
  tts('your note has been saved.')

def handle_notes(speech_text):
    """
    Handles reading and deleting notes based on user's command.
    This centralizes all note management logic in notes.py.
    """
    if 'read notes' in speech_text:
        if 'today' in speech_text:
            read_notes('today')
        elif 'yesterday' in speech_text:
            read_notes('yesterday')
        elif 'tomorrow' in speech_text:
            read_notes('tomorrow')
        else:
            tts("What date would you like to read notes for?")
            date = get_user_input()
            read_notes(date)

    elif 'delete notes' in speech_text:
        if 'today' in speech_text:
            delete_notes(datetime.now().strftime("%d-%m-%Y"))
        elif 'all' in speech_text:
            delete_notes(None)
        else:
            tts("What date would you like to delete notes for?")
            date = get_user_input()
            delete_notes(date)

def delete_notes(date=None):
  conn = sqlite3.connect('memory.db')
  cursor = conn.cursor()

  if date is None:
    confirmation = input("Are you sure you want to delete all notes? (yes or no): ")
    if confirmation.lower() != "yes":
      print("Cancelled")
      conn.close()
      return
    cursor.execute("DELETE FROM notes")
  else:
    cursor.execute("DELETE FROM notes WHERE date = ?", (date,))

  conn.commit()
  conn.close()
  print(f"Notes for {date if date else 'ALL dates'} deleted.")

def read_notes(date="today"):
    conn = sqlite3.connect("memory.db")
    cursor = conn.cursor()

    if date == "today":
        date = datetime.now().strftime("%d-%m-%Y")
    elif date == "yesterday":
        date = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")
    elif date == "tomorrow":
        date = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")

    cursor.execute("SELECT notes FROM notes WHERE date = ?", (date,))
    notes = cursor.fetchall()

    conn.close()

    if notes:
        print(f"Notes for {date}:")
        for note in notes:
            print(f"- {note[0]}")
    else:
        print(f"No notes found for {date}.")

def show_all_notes():
  conn = sqlite3.connect('memory.db')
  tts('Your notes are as follows:')
  
  cursor = conn.execute("SELECT notes FROM notes")

  for row in cursor:
    tts(row[0])

  conn.close()
