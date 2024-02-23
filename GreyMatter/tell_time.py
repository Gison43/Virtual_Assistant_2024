 #this code is to retrieve the current date and time

from datetime import datetime as dt, date

from GreyMatter.SenseCells.tts_engine import tts

today=dt.now()

def what_is_time():
  tts(f"The time is {today:%H %M %p}")
 # I think you'll need to change this, test it. 

def what_is_day():
  current_day = dt.now().date()
  tts(f"It is {current_day:%A}")
  #try changing line 15 to tts(f"It is {current_day:%A}")

def day_number():
   day_number = dt.now().date()
   tts(f"It is day number {day_number:%j} of the year {day_number:%Y}")

def when_birthday():
   tooday = dt.date.today()
   birthdate = dt.date(tooday.year, 7, 15)  # Assuming birthday is July 15th
   if tooday > birthdate:
      next_birthday = dt.date(tooday.year + 1, 7, 15)  # Next year's birthday
   else:
      next_birthday = birthdate  # This year's birthday

   days_until_birthday = (next_birthday - tooday).days
   tts(f"Your birthday is in {days_until_birthday}days.")

def current_year():
   current_year = dt.now().date()
   tts(f"It is the year {current_year:%Y}")

def how_old():
   now = dt.now()
   birthdatetime = dt(1978, 7, 15)
   age_days = (now - birthdatetime).days
   years_old = age_days // 365
   tts(f"You are {years_old}years old.")

def new_years_eve():
   current_year = dt.datetime.now().year
   new_years = dt.datetime(current_year, 12, 31, 23, 49)
   tts(f"It is at twenty-three fifty nine o'clock in the year {current_year}")

def what_is_date():
   current_date = dt.now().date()
   tts(f"It is {current_date:%B %d %Y}")

def what_month():
   current_month = dt.now().date()
   tts(f"It is {current_month: %B}")

def days_from_now(year, month, day):
 #get the current date
   current_date = dt.now().date()

#create a date time object for the futgure date
   future_date = dt(year, month, day).date()

#calculate the difference in days between the furtre date and the curent date
   difference = (future_date - current_date).days
   tts(f"There are {difference}days remaining until {future_date:%M %D %Y}")
