import sqlite3
from datetime import datetime
from datetime import timedelta
from GreyMatter.SenseCells.tts_engine import tts
from user_input import get_user_input

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
  conn = sqlite3.connect('memory.db')
  cursor = conn.cursor()

  if date is None:
    tts("Are you sure you want to delete all notes?")
    confirmation = input("Type 'yes' to confirm: ")
    if confirmation.lower() != "yes":
      tts("Cancelled")
      conn.close()
      return
    cursor.execute("DELETE FROM notes")
  else:
    cursor.execute("DELETE FROM notes WHERE notes_date = ?", (date,))
    tts(f"Notes for {date} deleted.")

  conn.commit()
  conn.close()
  print(f"Notes for {date if date else 'ALL dates'} deleted.")
  tts(f"Notes for  {date if date else 'ALL dates'} deleted.")

def read_notes(date="today"):
    conn = sqlite3.connect("memory.db")
    cursor = conn.cursor()

    if date == "today":
        date = datetime.now().strftime("%d-%m-%Y")
    elif date == "yesterday":
        date = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")
    elif date == "tomorrow":
        date = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")

    cursor.execute("SELECT notes FROM notes WHERE notes_date = ?", (date,))
    notes = cursor.fetchall()

    conn.close()

    if notes:
        print(f"Notes for {date}:")
        for note in notes:
            print(f"- {note[0]}")
            tts(note[0])
    else:
        print(f"No notes found for {date}.")

def show_all_notes():
  conn = sqlite3.connect('memory.db')
  tts('Your notes are as follows:')
  
  cursor = conn.execute("SELECT notes, notes_date FROM notes")

  for row in cursor:
    tts(f"On {row[1]}: {row[0]}")

  conn.close()
