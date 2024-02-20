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

def days_from_now(year, month, day):
 #get the current date
    current_date = dt.now().date()

#create a date time object for the futgure date
   future_date = dt(year, month, day).date()

#calculate the difference in days between the furtre date and the curent date
   difference = (future_date - current_date).days
   tts("There are " + str(difference) + " days remaining")
