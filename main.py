#This is Google Speech Recognition python file from 
#the book Building a Virtual Assistant  with RPi" year 2016

import sys

import yaml
import speech_recognition as sr

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

tts('Welcome ' + name + ', systems are now ready to run.  How can I help you?')

def main():
   r = sr.Recognizer()
   with sr.Microphone() as source:
      print("Listening...")
      r.pause_threshold = 1
      audio = r.listen(source)

   try:
      speech_text = r.recognize_google(audio, language='en-US').lower().replace("'","")
      print("Recognizing and transcribing what you said...")
      print('Computer thinks you said: ' + speech_text + "'")
   except sr.UnknownValueError:
     print("Computer didn't understand.")
   except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

   brain(name,speech_text)

main()
