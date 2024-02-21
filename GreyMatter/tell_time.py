 #this code is to retrieve the current date and time

from datetime import datetime as dt, date

from  SenseCells.tts_engine import tts

today=dt.now()

def what_is_time():
  tts("The time is " + (f"{today:%H:%M:%S}))

def what_is_day():
  current_day = dt.now().date()
  tts("It is " + (f"{current_day:%A}))

def day_number():
   day_number = dt.now().date()
   tts("It is day number " + (f"{day_number:%j}) + "of the year " + (f"{day_number:%Y}))

def current_year():
   current_year = dt.now().date()
   tts("It is the year " + (f"{current_year:%Y}))

def what_is_date():
  current_date = dt.now()date()
  tts("It is " + (f"{current_date: %B %d %Y}))

def what_month():
   current_month = dt.now()date()
   tts("It is " + (f"{current_month: %B}))

def days_from_now(year, month, day):
 #get the current date
    current_date = dt.now().date()

#create a date time object for the futgure date
   future_date = dt(year, month, day).date()

#calculate the difference in days between the furtre date and the curent date
   difference = (future_date - current_date).days
   tts("There are " + str(difference) + " days remaining")
