 #this code is to retrieve the current date and time

from datetime import datetime as dt, date

from GreyMatter.SenseCells.tts_engine import tts

today = dt.now().date()
now = dt.now()

def what_is_time():
    time_string = now.strftime("%H:%M %p")
    tts(f"The time is {time_string}")

def what_is_day():
  current_day = dt.now().date()
  tts(f"It is {current_day:%A}")
  #try changing line 15 to tts(f"It is {current_day:%A}")

def day_number():
   day_number = dt.now().date()
   tts(f"It is day number {day_number:%j} of the year {day_number:%Y}")

def when_birthday():
    today = date.today()
    birthdate = date(today.year, 7, 15)  # Assuming birthday is July 15th
    if today > birthdate:
       next_birthday = date(today.year + 1, 7, 15)  # Next year's birthday
    else:
       next_birthday = birthdate  # This year's birthday

    days_until_birthday = (next_birthday - today).days
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
    current_year = dt.now().year
    new_years = dt(target_year, 12, 31, 23, 59)
    time_until_new_years = new_years - dt.now()
    target_year = current_year + 1
    days_until_new_years = time_until_new_years.days
    hours_until_new_years, remainder = divmod(time_until_new_years.seconds, 3600)
    minutes_until_new_years, _ = divmod(remainder, 60)
    tts(f"It is {days_until_new_years} days, {hours_until_new_years} hours, and {minutes_until_new_years}minutes, until New Years Eve in the year {target_year}.")

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
