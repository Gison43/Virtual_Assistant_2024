import sqlite3
from datetime import datetime

from GreyMatter.SenseCells.tts_engine import tts

def note_something(speech_text):
  conn = sqlite3.connect('memory.db')
  words_of_message = speech_text.split ()
  words_of_message.remove ('note')
  cleaned_message = ' '.join (words_of_message)
  
  conn.execute ("INSERT INTO notes (notes, notes_date) VALUES (?, ? )", (cleaned_message, datetime.strftime(datetime.now(), '%d-%m%-Y')))
  conn.commit()
  conn.close()
  tts('your note has been saved.')
