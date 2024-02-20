#this code is to retrieve the current date and time

from datetime import datetime as dt

from  SenseCells.tts import tts

def what_is_time():
  tts("The time is " + dt.strftime(dt.now(), '%H:%M:%S'))
  
