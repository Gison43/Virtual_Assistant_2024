#!/usr/bin/env python3

from user_input import get_user_input
from GreyMatter import tell_time, general_conversations, spanish_translator, weather, define_subject, timer, stopwatch
from GreyMatter.SenseCells.tts_engine import tts
from GreyMatter.spanish_translator import language_selection
#from GreyMatter import french_translator

def brain(name, speech_text, city_name, city_code):
   """
   this function compares check vs speech_text to see if they are equal.  Also
   checks if the items in the list (specificed in the argument are present in 
   the user's speech.
   """

   def check_message(check):
      words_of_message = speech_text.split()
      if set(check).issubset(set(words_of_message)):
         return True
      else:
         return False

   stopwatch_started = False
   start_time = None

   if check_message(['who',' are', 'you']):
      general_conversations.who_are_you()
         #if the message is true then call the function

   elif check_message(['tell', 'joke']):
      general_conversations.tell_me_a_joke()

   while True:
      if check_message(['start', 'stopwatch']):
         if not stopwatch_started:
            start_time = Stopwatch.start() #start the stopwatich if it's not started
            stopwatch_started = True
            tts("We are starting the stopwatch. Let's go.")
         else:
            tts("The stopwatch is already runnning.")

      elif check_message(['stop', 'stopwatch']):
         if stopwatch_started:
            total_time = Stopwatch.stop(start_time)#Pass the start_time to stop() and stop the stopwatch and get the total time elapsed
            tts(f"The stopwatch has been stopped and the total time is {format_time(total_time)}.")
            stopwatch_started = False
         else:
            tts("The stopwatch is not running.")

      elif check_message(['time', 'elapsed', 'stopwatch']):
         if stopwatch_started:
            current_time = Stopwatch.elapsed()  # Get the current elapsed time on the stopwatch
            tts(f"The current time elapsed on the stopwatch is {current_time} minutes.")
         else:
            tts("The stopwatch is not running.")

      elif check_message(['split']):
         if stopwatch_started:
            Stopwatch.split()
            tts("The stopwatch has been split.")
         else:
            tts("The stopwatch is not running.  Start it first.")

      elif check_message(['exit']):
         if stopwatch_started:
            total_time = Stopwatch.stop()
            tts(f"The stopwatch has been stopped and the total time is {total_time} minutes.  Exiting the stopwatch program.")
            stopwatch_started = False
         else:
            tts("Command not recognized.  Please try again.")

   elif check_message(['how', 'long', 'until', 'my', 'birthday']) or check_message(['how', 'many', 'days', 'until', 'my', 'birthday']):
       tell_time.when_birthday()

   elif check_message(['what', 'year', 'is','it']) or check_message(['what', 'current', 'year']):
       tell_time.current_year()

   elif check_message(['how', 'old', 'am', 'i']):
       tell_time.how_old()

   elif check_message(['calculate', 'area', 'rectangle']):  #not currenlty working right now
       area()

   elif check_message(['when','my', 'birthday']):
      general_conversations.when_birthday()

   elif check_message(['want','to','practice', 'language']):
      tts("What language would you like to practice? Spanish or French?")

      #listen for the user's response
      user_response = get_user_input()

      #check if the user wants to practic Spanish
      if 'spanish' in user_response:
         language_selection('spanish')
      elif 'french' in user_response:
         language_selection('french')
      else:
         tts("Sorry, only spanish and french are currently supported.")

   elif check_message(['when', 'new', 'years']) or check_message(['how', 'long', 'until', 'new', 'years', 'eve']):
      tell_time.new_years_eve()

   elif check_message(['how', 'weather']) or check_message(['how', 'is', 'weather']):
       weather.weather()

   elif check_message(['when', 'created']):
      general_conversations.when_were_you_created()

   elif check_message(['when', 'born']):
      general_conversations.when_were_you_born()

   elif check_message(['how','are','you']):
      general_conversations.how_are_you()

   elif check_message(['i am', 'doing', 'well', 'fine', 'good']):
      general_conversations.i_am_doing_well_thank_you()

   elif check_message(['who', 'am', 'i']) or check_message(['what','is','my', 'name']) or check_message(['whats', 'my', 'name']):
      general_conversations.who_am_i(name)

   elif check_message(['time']) or check_message(['what', 'time', 'is', 'it']):
      tell_time.what_is_time()

   elif check_message(['what', 'day', 'number']):
      tell_time.day_number()

   elif check_message(['what','day','is','it']) or check_message(['what', 'day', 'of', 'the', 'week', 'is','it']):
      tell_time.what_is_day()

   elif check_message(['what','month']):
      tell_time.what_month()

   elif check_message(['what', 'is', 'the', 'date', 'today']) or check_message(['current', 'date']):
      tell_time.what_is_date()

   elif check_message(['define']):
       define_subject.define_subject(speech_text)

   elif check_message(['how', 'weather']) or check_message(['what', 'is','the', 'weather','forecast']):
      weather.weather(city_name = city_name, city_code = city_code)

   elif check_message(['how', 'many', 'days', 'remaining', 'until']):
      #find the index of the word "until"
      #note that the speaker must ask for the date in the format of MM:DD:YYYY, in that order
      if all(word in words for word in ['how', 'many', 'days', 'remaining', 'until']):
         until_index = words.index('until')

   #extract the date provided by the speaker
         date_words = words[until_index + 1:]

   #convert the date words into numbers (assuming the date is provided in the format "MM-DD-YYYY"
         month = int(date_words[0])
         day = int(date_words[1])
         year = int(date_words[2])

      tell_time.days_from_now(year, month, day)

   else:
      #if not, then call the function 'i don't understand
      general_conversations.undefined()
