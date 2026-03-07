#!/usr/bin/env python

from datetime  import datetime as dt, date
import random
import os

from GreyMatter import tell_time, general_conversations, spanish_translator, weather, define_subject, timer, sleep, play_music, area, notes
from GreyMatter.list import List
from GreyMatter.spanish_translator import language_selection
from user_input import get_user_input
from ear_test import check_ncf_email
from GreyMatter.SenseCells.tts_engine import tts

my_list = List()

today = dt.now().date()
now = dt.now()

def neural_network(name, text, city_name, city_code, stopwatch_instance, music_path):
    text = text.lower().replace("?", "").strip()

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

    knowledge_base = {

        "who am i": f"You are {name}, my creator.",
        "who are you": get_intro,
        "tell me a joke": get_joke,
        "when is my birthday": "Your birthday is July 15.  You were born in 1978.",
        "when were you created": "I was created on February 12 2024",
        "how are you": "I am doing well, and you",
        "what is your name": "I dont have a name yet",
        "what are you": "I am a fully functional, artificially intelligent, state of the art virtual assistant, and I am all yours, baby.",
        "how old am i": tell_time.how_old,
        "calculate the area of a rectangle":area.calculate_rectangle_area,
        "when is new years":tell_time.new_years_eve,
        "how is the weather":weather.weather,
        "what is the weather like today":weather.weather,
        "when were you born":"I was created on February 12 2024",
        "note":lambda: notes.note_something(speech_text),
        "read notes":lambda:notes.handle_notes(speech_text),
        "delete notes":lambda:notes.handle_notes(speech_text),
        "delete note":lambda:notes.handle_notes(speech_text),
        "delete all notes":lambda:notes.delete_notes(None),
        "take note":lambda:notes.note_something(speech_text),

    }

    for key, response in knowledge_base.items():
         if key in text:
             if callable(response):
                 try:
                     return response(name)
                 except TypeError:
                     return response()
             return response

    if "time" in text:
        response = f"it's {dt.now().strftime('%I:%M %p')}"
        return response
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(dir_path, "missing_commands.txt")
    
    with open(log_path, "a") as f:
        #get the current timestamp so you know when you asked it.
        timestamp = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] Unknown command: {text}\n")

    print(f"DEBUG: Unknown command logged: {text}")
    return "i'm sorry, I haven't learned how to respond to that yet, but I'll save it for later."
