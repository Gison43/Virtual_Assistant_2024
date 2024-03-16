#!/usr/bin/env python3

import datetime

from GreyMatter import tell_time, general_conversations, spanish_translator, weather, define_subject, timer
from GreyMatter.SenseCells.tts_engine import tts
from GreyMatter.spanish_translator import language_selection
from GreyMatter.stopwatch import Stopwatch

#from GreyMatter import french_translator

#stopwatch_instance = Stopwatch()


def process_command(speech_text, stopwatch_instance):
   print(stopwatch_instance.is_running)
   pass


def neural_network(name, speech_text, city_name, city_code, stopwatch_instance):
   """
   this function compares check vs speech_text to see if they are equal.  Also
   checks if the items in the list (specificed in the argument are present in 
   the user's speech.
   """

   def check_message(check):
      words_of_message = speech_text.split()
      if set(check).issubset(set(words_of_message)):
         print(f"Detected command: {check}")
         return True
      else:
         return False

   start_time = None
#   stopwatch_instance = Stopwatch() #create an instance of the Stopwatch class


   def is_stopwatch_command(command):
      stopwatch_commands = ['start stopwatch', 'stop stopwatch', 'elapsed stopwatch', 'exit stopwatch', 'split stopwatch', 'reset stopwatch']
      return any(stopwatch_command in command for stopwatch_command in stopwatch_commands)


   if is_stopwatch_command(speech_text):
      if 'start stopwatch' in speech_text:
         if not stopwatch_instance.is_running:
            start_time = stopwatch_instance.start() #start the stopwatch if it's not started
            stopwatch_instance.is_running = True
            tts("We are starting the stopwatch. Let's go.")
            print("The stopwatch is running.",stopwatch_instance.is_running)
         else:
            tts("The stopwatch is already running.")

      elif 'stop stopwatch' in speech_text:
         if stopwatch_instance.is_running:
             total_time, split_times  = stopwatch_instance.stop(start_time) #stop the stopwatch and get the total time elapsed and unpack the tuple
             total_time_delta = datetime.timedelta(seconds = total_time) #convert total_time to timedelta object
             formatted_total_time = stopwatch_instance.format_time(total_time_delta)
             formatted_split_times = [stopwatch_instance.format_time(split) for split in split_times] #format each split time
             stopwatch_instance.is_running = False
             tts(f"The stopwatch has been stopped and the total time is {formatted_total_time}.")
             print("The stopwatch has been stopped and the total time is", total_time)
             for i, split_time in enumerate(formatted_split_times, start = 1):
                tts(f"Split {i} time is {split_time}.")
         else:
             tts("The stopwatch is not running.")
             print("The stopwatch is not running.", stopwatch_instance.is_running)

      elif 'elapsed stopwatch' in speech_text:
         if stopwatch_instance.is_running:
             current_time = stopwatch_instance.elapsed(start_time)  # Get the current elapsed time on the stopwatch
             formatted_elapsed_time = stopwatch_instance.format_time(current_time)
             tts(f"The current time elapsed on the stopwatch is {formatted_elapsed_time}.")
             print("The stopwatch elapsed time is ", current_time)
         else:
             tts("The stopwatch is not running.")
         for i, split_time in enumerate(stopwatch_instance.splits, start = 1):
             split_time_str = stopwatch_instance.format_time(split_time)
             tts(f"Split {i}: {split_time_str}")


      elif 'reset stopwatch' in speech_text:
         if stopwatch_instance.is_running:
            stopwatch_instance.reset()
            tts("The stopwatch has been reset to zero time.")

      elif 'split stopwatch' in speech_text:
         if stopwatch_instance.is_running:
            stopwatch_instance.split()
            tts("The stopwatch has been split.")
         else:
            tts("The stopwatch is not running.  Start it first.")

      elif 'stop split' in speech_text:
         try:
            split_index = int(re.search(r'\d+', speech_text).group())
         except ValueError:
            tts("Please specify a valid split index.")
            return
         #check if the stopwatch is running
         if stopwatch_instance.is_running:
            try:
               split_time = stopwatch_instance.stop_split(split_index - 1) #adjust the index
               formatted_split_time = stopwatch_instance.format_time(split_time)
               tts(f"Stopping split {split_index} at {formatted_split_time}.")
            except IndexError:
               tts(f"Invalid split index. Please try again.")
         else:
            tts("The stopwatch is not running.")


      elif 'exit stopwatch' in speech_text:
         if stopwatch_instance.is_running:
            total_time = stopwatch_instance.stop(start_time)
            formatted_time = stopwatch_instance.format_time(total_time)
            tts(f"The stopwatch has been stopped and the total time is {formatted_time}.  Exiting the stopwatch program.")
         else:
            tts("Exiting the stopwatch program.")
         stopwatch_instance.reset_splits()

      return

   if check_message(['who',' are', 'you']):
      general_conversations.who_are_you()
      #if the message is true then call the function

   elif check_message(['tell', 'joke']):
      general_conversations.tell_me_a_joke()

   elif check_message(['how', 'long', 'until', 'my', 'birthday']) or check_message(['how', 'many', 'days', 'until', 'my', 'birthday']):
       tell_time.when_birthday()

   elif check_message(['what', 'year', 'is','it']) or check_message(['what', 'current', 'year']):
       tell_time.current_year()

   elif check_message(['how', 'old', 'am', 'i']):
       tell_time.how_old()

   elif check_message(['calculate', 'area', 'rectangle']):  #not currently working right now
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
      #if not, then call the function 'i don't understand'
      general_conversations.undefined()

if __name__ == "__main__":
   main()
