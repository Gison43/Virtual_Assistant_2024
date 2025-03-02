#!/usr/bin/env python3

import datetime
import aiml
import re

from GreyMatter import tell_time, general_conversations, spanish_translator, weather, define_subject, timer, sleep, play_music, area, notes
from GreyMatter.list import List
from GreyMatter.SenseCells.tts_engine import tts
from GreyMatter.spanish_translator import language_selection
from GreyMatter.stopwatch import Stopwatch
#from swpy import Timer
from user_input import get_user_input

#from GreyMatter import french_translator

#stopwatch_instance = Stopwatch()

kernel = aiml.Kernel()

#load AIML files
kernel.bootstrap(learnFiles = "GreyMatter/yak.aiml")

my_list = List()  #create an instance of the list class

ELAPSED_PHRASES = {
   'elapsed stopwatch',
   'time elapsed on stopwatch',
   'current stopwatch time',
   'what is the time on the stopwatch',
   'how much time has passed on the stopwatch',
   'what time is on the stopwatch',
   'whats the time elapsed on the stopwatch',
   'what is the current time on the stopwatch'
   }
   
def process_command(speech_text, stopwatch_instance):
   print(stopwatch_instance.is_running)
   pass


def neural_network(name, speech_text, city_name, city_code, stopwatch_instance, music_path):
   print(f"[DEBUG] Entering neural_network() - stopwatch_instance.is_running = {stopwatch_instance.is_running}")
   print(f"[DEBUG] Received speech_text: '{speech_text}'")
   """
   this function compares check vs speech_text to see if they are equal.  Also
   checks if the items in the list (specified in the argument are present in 
   the user's speech.
   """

   def check_message(check):
      words_of_message = speech_text.split()
      if set(check).issubset(set(words_of_message)):
         print(f"Detected command: {check}")
         return True
      else:
         return False

   def is_stopwatch_command(command):
      stopwatch_commands = ['start stopwatch', 'stop stopwatch', 'elapsed stopwatch', 'exit stopwatch', 'split stopwatch', 'reset stopwatch',
                           'list splits', 'show splits', 'what are the splits'] + list(ELAPSED_PHRASES)
      return any(stopwatch_command in command for stopwatch_command in stopwatch_commands)

   if is_stopwatch_command(speech_text):
      print(f"[DEBUG] Detected stopwatch command: {speech_text}")
      print(f"[DEBUG] Pre-command - stopwatch_instance.is_running = {stopwatch_instance.is_running}")
      if 'start stopwatch' in speech_text:
         if not stopwatch_instance.is_running:
            stopwatch_instance.start()
            tts("We are starting the stopwatch. Let's go.")
            print(f"[DEBUG] After start - stopwatch_instance.is_running = {stopwatch_instance.is_running}")
            print("The stopwatch is running.",stopwatch_instance.is_running)
         else:
            tts("The stopwatch is already running.")

      elif 'stop stopwatch' in speech_text:
         print(f"[DEBUG] Stop requested - stopwatch_instance.is_running = {stopwatch_instance.is_running}")
         if stopwatch_instance.is_running:
             stopwatch_instance.stop()
             stopwatch_instance.is_running = False
         else:
             tts("The stopwatch is not running.")

      elif any(phrase in speech_text for phrase in ELAPSED_PHRASES):
         print(f"[DEBUG] Matched command: elapsed stopwatch (phrase = '{speech_text}')")
               
         if stopwatch_instance.is_running:
             current_time_delta, formatted_elapsed_time = stopwatch_instance.elapsed()  # Get the current elapsed time on the stopwatch
             tts(f"The current time elapsed on the stopwatch is {formatted_elapsed_time}.")
             print("The stopwatch elapsed time is ", current_time_delta)
         elif stopwatch_instance.start_time is None:
             tts("The stopwatch has not been started")
         else:
             total_time_delta, formatted_total_time = stopwatch_instance.elapsed() #Get the total elpased time when the stopwatch is stopped
             tts(f"The stopwatch is stopped.  The total elapsed time is {formatted_total_time}.")
             print("The stopwatch is stopped.  The total elapsed time is ", total_time_delta)

         splits = stopwatch_instance.get_splits()

         if splits:
            tts("Here are the split times.")
            for split_entry in splits:
               tts(f"{split_entry['title']}: {split_entry['formatted']}")

      elif 'reset stopwatch' in speech_text:
         if stopwatch_instance.start_time is None:
            tts("Please start the stopwatch.")
         else:
            try:
               stopwatch_instance.reset()
               tts("I have reset the stopwatch.")
            except Exception as e:
               tts("An error occured while resetting the stopwatch.")
               print("Error resetting the stopwatch:", e)

      elif any(phrase in speech_text for phrase in ['list splits', 'show splits', 'what are the splits']):
         splits = stopwatch_instance.get_splits()
         if not splits:
            tts("There are no splits recorded")
         else:
            split_messages = []
            for index, split in enumerate(splits, start=1):
               split_messages.append(f"Split {index}: {split['formatted']}")
               tts("Here are the splits. " + " ".join(split_messages))
         
      elif 'split stopwatch' in speech_text:
         print(f"[DEBUG] Split requested - stopwatch_instance.is_running = {stopwatch_instance.is_running}")
         if stopwatch_instance.is_running:
            stopwatch_instance.split()
            tts("The stopwatch has been split.")
         else:
            tts("The stopwatch is not running.  Start it first.")

      elif 'list splits' in speech_text:
         splits = stopwatch_instance.get_splits()
         
         if splits:
            tts("Here are the current splits.")
            for i, split_entry in enumerate(stopwatch_instance.get_splits(), start=1):
               tts(f"{split_entry['title']} - {split_entry['formatted']}")
         else:
            tts("There are no splits recorded.")

      elif 'exit stopwatch' in speech_text:
         if stopwatch_instance.is_running:
            total_time = stopwatch_instance.stop()
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

   elif check_message(['create', 'list']) or check_message(['start', 'list']):
       tts("Sure. Let's create a new list. What would you like to name your new list.")
       list_name = get_user_input()
       my_list.create_list(list_name) #call the create_list method and pass the list name to it
       tts(f"Ok. I've created a list called {list_name}")

   elif check_message(['add','to', 'list']):
       tts("What is the name of the list?")
       list_name = get_user_input()
       tts("What item or items would you like to add to the list?")
       items = get_user_input().split()
       for item in items:
           my_list.add_item(item, list_name) #provide the list_name argument and add each item to the list
           tts(f"{', '.join(items)} now added to the list called {list_name}")

   elif check_message(['how', 'old', 'am', 'i']):
       tell_time.how_old()

   elif check_message(['calculate', 'area', 'rectangle']):
       area.calculate_rectangle_area()

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

   elif check_message(['how', 'weather']) or check_message(['how', 'is', 'weather']) or check_message(['what', 'is', 'the', 'weather', 'like', 'outside']):
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

   elif check_message(['time']) and not check_message(['stopwatch']) or check_message(['what', 'time', 'is', 'it']) and not check_message(['stopwatch']):
      tell_time.what_is_time()

   elif check_message(['what', 'day', 'number']):
      tell_time.day_number()

   elif check_message(['what','day','is','it']) or check_message(['what', 'day', 'of', 'the', 'week', 'is','it']):
      tell_time.what_is_day()

   elif check_message(['what','month']):
      tell_time.what_month()

   elif check_message(['what', 'are', 'you']):
      general_conversations.what_are_you()

   elif check_message(['what', 'your', 'name']):
      general_conversations.what_is_your_name()

   elif check_message(['sleep']):
      sleep.go_to_sleep()

   elif check_message(['what', 'is', 'the', 'date', 'today']) or check_message(['current', 'date']):
      tell_time.what_is_date()

   elif check_message(['play', 'music']) or check_message(['music']):
      play_music.play_random(music_path)

   elif check_message(['play']):
      play_music.play_specific_music(speech_text, music_path)

   elif check_message(['define']):
      define_subject.define_subject(speech_text)

   elif check_message(['note']):
      notes.note_something(speech_text)

   elif check_message(['all', 'notes']) or check_message(['notes']):
      notes.show_all_notes()

   elif check_message(['read', 'notes']) or check_message(['notes']):
      notes.handle_notes(speec_text)

   elif check_message(['delete', 'notes']) or check_message(['delete', 'note']):
      notes.handle_notes(speech_text)

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
