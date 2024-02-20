 #this code is to retrieve the current date and time

from datetime import datetime as dt, date

from  SenseCells.tts_engine import tts

def what_is_time():
  tts("The time is " + dt.strftime(dt.now(), '%H:%M:%S'))

def what_is_day():
  current_day = dt.now().date()
  tts("It is " + current_day.strftime('%A'))

def what_is_date():
  current_date = dt.now()date()
  tts("It is " + current_date.strftime('%B %d %Y'))
