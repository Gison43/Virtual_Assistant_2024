#!/usr/bin/env python

from datetime  import datetime as dt, date
import random
import os
import threading

from GreyMatter import tell_time, general_conversations, spanish_translator, weather, define_subject, timer, sleep, play_music, area, notes
from GreyMatter.list import List
from GreyMatter.spanish_translator import language_selection
from user_input import get_user_input
from ear_test import check_ncf_email
from GreyMatter.SenseCells.tts_engine import tts

my_list = List()

ELAPSED_PHRASES = [
    'elapsed stopwatch',
    'time elapsed on stopwatch',
    'elapsed time on stopwatch',
    'current stopwatch time',
    'what is the time on the stopwatch',
    'how much time has passed on the stopwatch',
    'what time is on the stopwatch',
    'what is the current time on the stopwatch',
    'whats the time elapsed on the stopwatch',
    'stopwatch status',
    'stop watch status',
    'check stopwatch',
    'what is the status on the stopwatch',
    'whats the status on the stopwatch',    
]

today = dt.now().date()
now = dt.now()

def neural_network(name, speech_text, city_name, city_code, stopwatch_instance, music_path):
    speech_text = speech_text.lower().replace("?", "").strip()

    def get_joke():
        return random.choice([
            "what do you call a magical dog? A labracadabrador.",
            "What do you call a pony with a cough? A little horse",
            "Why was six scared of seven? Because seven ate nine.",
            "What do you call a woman with one leg? Eileen",
            "what did the pirate say when he turned 80? Aye matey."
        ])

    def get_intro():
        return random.choice([
            "I am computer, your dedicated and intelligent assistant.",
            "computer, God dammit did I not tell you before",
            "you keep asking me that, I am computer."
        ])

    def language_practice():
        tts("What language would you like to practice? Spanish or French?")

      #listen for the user's response
        user_response = get_user_input()
        if 'spanish' in user_response:
            return language_selection('spanish')
        elif 'french' in user_response:
            return language_selection('french')
        else:
            return "Sorry, only spanish and french are currently supported."

    def create_list():
        tts("Sure. What would you like to name the new list?")
        # CHANGE 1: actually capture the variable returned by the microphone
        list_name = get_user_input()

        if list_name:
            # Create the list in the database
            my_list.create_list(list_name)
            
            # CHANGE 2: Chain the next question immediately
            tts(f"I've created the {list_name} list. What would you like to add to it?")
            
            # CHANGE 3: Listen again for the items
            items_input = get_user_input()
            if items_input:
                # Add the items immediately
                my_list.add_item(items_input.split(" and "), list_name)
            else:
                tts("I didn't hear any items, but the empty list is saved.")
        else:
            # CHANGE 4: Handle silence (if you didn't say a name)
            tts("I didn't hear a name, so I cancelled the list creation.")
       
    def add_to_list():
        tts("What is the name of the list?")
        list_name = get_user_input()

        if list_name:
            finished = False
            while not finished:
                tts(f"What would you like to add to {list_name}?")
                user_speech = get_user_input().lower()
            
                # Send to list.py to save
                my_list.add_item(user_speech, list_name)

                # The Follow-up Question
                tts("Is there anything else?")
                response = get_user_input().lower()

                # LOGIC: 
                # If you say "NO", we are DONE.
                # If you say "YES", we stay in the loop.
                if 'no' in response or 'done' in response or 'that is all' in response:
                    tts(f"Okay, I've updated your {list_name} list.")
                    finished = True
                elif 'yes' in response:
                    # We don't need to do anything here, 
                    # the loop will naturally start over.
                    continue 
                else:
                    # If it didn't hear a clear yes/no
                    tts("I'm sorry, did you want to add more?")
                    confirm = get_user_input().lower()
                    if 'no' in confirm:
                        finished = True

    def read_specific_list():
        #this is so that lists and notes don't get confused
        if "notes" in speech_text:
            return None
            
        filter_words = ["read", "me", "my", "what", "is", "on", "the", "list", "check"]
        words = speech_text.split()
        name_parts = [w for w in words if w not in filter_words]

        found_name = " ".join(name_parts)

        if found_name:
            print(f"DEBUG: Looking for list name: {found_name}")
            return my_list.read_list(found_name)
        else:
            tts("Which list would you like me to read?")
            list_name = get_user_input().lower()  # e.g., "grocery"
            if list_name:
            # Talk directly to list.py, which now talks to the DB
                return my_list.read_list(list_name)
   
    def show_lists():
        # This will list the names of all lists (e.g., "Grocery", "Todo")
       my_list.view_list()

    def start_stopwatch():
         if not stopwatch_instance.is_running:
            stopwatch_instance.start()
            tts("We are starting the stopwatch. Let's go.")
            print(f"[DEBUG] After start - stopwatch_instance.is_running = {stopwatch_instance.is_running}")
            print("The stopwatch is running.",stopwatch_instance.is_running)
         else:
            tts("The stopwatch is already running.")

    def stop_stopwatch():
         print(f"[DEBUG] Stop requested - stopwatch_instance.is_running = {stopwatch_instance.is_running}")
         if stopwatch_instance.is_running:
             stopwatch_instance.stop()
             stopwatch_instance.is_running = False
         else:
             tts("The stopwatch is not running.")

    def status_stopwatch():
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

    def reset_stopwatch():
         if stopwatch_instance.start_time is None:
            tts("Please start the stopwatch.")
         else:
            try:
               stopwatch_instance.reset()
               tts("I have reset the stopwatch.")
            except Exception as e:
               tts("An error occured while resetting the stopwatch.")
               print("Error resetting the stopwatch:", e)

    def split_stopwatch():
         print(f"[DEBUG] Split requested - stopwatch_instance.is_running = {stopwatch_instance.is_running}")
         if stopwatch_instance.is_running:
            stopwatch_instance.split()
            tts("The stopwatch has been split.")
         else:
            tts("The stopwatch is not running.  Start it first.")

    def list_splits():
         splits = stopwatch_instance.get_splits()

         if splits:
            tts("Here are the current splits.")
            for i, split_entry in enumerate(stopwatch_instance.get_splits(), start=1):
               tts(f"{split_entry['title']} - {split_entry['formatted']}")
         else:
            tts("There are no splits recorded.")

    def exit_stopwatch():
         if stopwatch_instance.is_running:
            total_time = stopwatch_instance.stop()
            formatted_time = stopwatch_instance.format_time(total_time)
            tts(f"The stopwatch has been stopped and the total time is {formatted_time}.  Exiting the stopwatch program.")
         else:
            tts("Exiting the stopwatch program.")
         stopwatch_instance.reset_splits()

    def days_until_event():
        # speech_text is already lowercased and cleaned in neural_network
        words = speech_text.split()
        
        if 'until' in words:
            until_index = words.index('until')
            # Look at everything after the word "until"
            date_parts = words[until_index + 1:]
            
            if len(date_parts) >= 3:
                try:
                    # Expects input like "until 12 25 2026"
                    month = int(date_parts[0])
                    day = int(date_parts[1])
                    year = int(date_parts[2])
                    
                    # This calls your existing function in tell_time.py
                    tell_time.days_from_now(year, month, day)
                except (ValueError, IndexError):
                    tts("I'm sorry, I need the date in month, day, and year numbers to calculate that.")
            else:
                tts("Please provide the date as month, day, and year after the word until.")
        else:
            tts("I didn't hear a date. Try saying how many days until 12 25 2026.")

    knowledge_base = {

        #STOPWATCH COMMANDS
        "start stopwatch":start_stopwatch,
        "start the stopwatch":start_stopwatch,
        "stopwatch time":status_stopwatch,
        "stop stopwatch":stop_stopwatch,
        "stop the stopwatch":stop_stopwatch,
        "reset stopwatch":reset_stopwatch,
        "split stopwatch":split_stopwatch,
        "what are the splits on the stopwatch":list_splits,
        "list splits on stopwatch": list_splits,
        "show splits": list_splits,
        "how many splits on the stopwatch":list_splits,
        "exit stopwatch": exit_stopwatch,
        "cancel stopwatch": exit_stopwatch,
        
        "go to sleep":sleep.go_to_sleep,
        "what time is it": lambda: f"It's {dt.now().strftime('%I:%M %p')}", # General match last
        "what is the current time": lambda: f"It's {dt.now().strftime('%I:%M %p')}",
        "goodbye":sleep.go_to_sleep,
        "sleep":sleep.go_to_sleep,
        "what day is it":tell_time.what_is_day,
        "what day is it today":tell_time.what_is_day,
        "what month is it":tell_time.what_month,
        "how many days until": days_until_event,
        "days remaining until": days_until_event,
        "countdown to":days_until_event,
        "what are you":general_conversations.what_are_you,
        "what is your name":general_conversations.what_is_your_name,
        "what is the date today":tell_time.what_is_date,
        "what is the current date":tell_time.what_is_date,
        "who am i": f"You are {name}, my creator.",
        "who are you": get_intro,
        "tell me a joke": get_joke,
        "when is my birthday": "Your birthday is July 15.  You were born in 1978.",
        "when were you created": "I was created on February 12 2024",
        "how are you": "I am doing well, and you",
        "what are you": "I am a fully functional, artificially intelligent, state of the art virtual assistant, and I am all yours, baby.",
        "how old am i": tell_time.how_old,
        "calculate the area of a rectangle":area.calculate_rectangle_area,
        "when is new years":tell_time.new_years_eve,
        "when is new years eve":tell_time.new_years_eve,
        "whens new years eve":tell_time.new_years_eve,
        "how is the weather":weather.weather,
        "what is the weather like today":weather.weather,
        "when were you born":"I was created on February 12 2024",
        #NOTE TAKING
        "read notes":lambda: notes.handle_notes(speech_text),
        "delete all notes":lambda:notes.delete_notes(None),
        "delete notes":lambda: notes.handle_notes(speech_text),
        "delete note":lambda:notes.handle_notes(speech_text),
        "take a note":lambda: notes.note_something(speech_text),
        "save a note":lambda: notes.note_something(speech_text),
        "take note":lambda:notes.note_something(speech_text),
        "note":lambda:notes.note_something(speech_text),
        #LANGUAGE PRACTICE
        "practice a language": language_practice,
        "language practice": language_practice,
        "let's practice a language": language_practice,
        #LISTS
        "read me my lists":read_specific_list,
        "tell me my lists":read_specific_list,
        "read my":read_specific_list,
        "check my": read_specific_list,
        "create a new list": create_list,
        "create a list": create_list,
        "create list":create_list,
        "start a new list": create_list,
        "start a list": create_list,
        "what is on my list":read_specific_list,
        "what's on my list": read_specific_list,
        "what is on my":read_specific_list,
        "list my lists": show_lists,
        "add to my list": add_to_list,
        "add to the list": add_to_list,
        "add to list": add_to_list,
        "view lists": show_lists,
        "view my lists": show_lists,
                          
    }
    for phrase in ELAPSED_PHRASES:
        knowledge_base[phrase.lower()] = status_stopwatch
    #this is the loop
    for key, response in knowledge_base.items():
         if key in speech_text:
             if callable(response):
                 try:
                     return response(name)
                 except TypeError:
                     return response()
             return response

    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(dir_path, "missing_commands.txt")
    
    with open(log_path, "a") as f:
        #get the current timestamp so you know when you asked it.
        timestamp = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] Unknown command: {speech_text}\n")

    print(f"DEBUG: Unknown command logged: {speech_text}")
    return "i'm sorry, I haven't learned how to respond to that yet, but I'll save it for later."
