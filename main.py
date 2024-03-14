#!/usr/bin/env python3
#This is Google Speech Recognition python file from 
#the book Building a Virtual Assistant  with RPi" year 2016

import sys

import yaml
import speech_recognition as sr
import datetime

from os import path
from speech_recognition.recognizers import google

from brain import brain
from GreyMatter.SenseCells.tts_engine import tts

profile = open('profile.yaml')
profile_data = yaml.safe_load(profile)
profile.close()

#Functioning Variables
name = profile_data['name']
city_name = profile_data['city_name']
city_code = profile_data['city_code']
current_hour = datetime.datetime.now().hour

if 5 <= current_hour > 12:
    tts('Good morning ' + name + ' systems are now ready to run.  what is your command.')
elif 12 <= current_hour > 18:
    tts('Good afternoon ' + name + 'systems are now ready to run.  what is your command.')
else:
    tts('Good evening ' + name + 'systems are now ready to run.  what is your command.')

def process_command(speech_text):
   global stopwatch_instance
   pass

def main():
   r = sr.Recognizer()
   m = sr.Microphone()
   with m as source:
       print("Adjusting...")
       r.adjust_for_ambient_noise(source)
       print("Set minimum energy threshold to {}".format(r.energy_threshold))
       while True:
          print("Listening...")
          r.pause_threshold = 1
          audio = r.listen(source, phrase_time_limit = 10.0)

          try:
             speech_text = r.recognize_google(audio, language='en-US').lower().replace("'","")
             print("Recognizing and transcribing what you said...")
             print('Computer thinks you said: ' + speech_text + "'")
             process_command(speech_text)
          except sr.UnknownValueError:
             print("Computer didn't understand.")
          except sr.RequestError as e:
             print("Could not request results from Google Speech Recognition service; {0}".format(e))

          brain(name, speech_text, city_name, city_code)

main()
