#!/usr/bin/env python3
#This is Google Speech Recognition python file from 
#the book Building a Virtual Assistant  with RPi" year 2016

import sys
import os

import yaml
import speech_recognition as sr
import datetime
import brain
import argparse
import subprocess

from os import path
from speech_recognition.recognizers import google

from GreyMatter import play_music
from GreyMatter.SenseCells.tts_engine import tts
from GreyMatter.stopwatch import Stopwatch

profile = open('profile.yaml')
profile_data = yaml.safe_load(profile)
profile.close()

#this is to initialize text commands to the VA
parser = argparse.ArgumentParser(description="Virtual Assistant with text and voice input.")
parser.add_argument("-t", "--text", help = "Enable text input mode.", action = "store_true")

#Parse the command-line arguments
args = parser.parse_args()

#Functioning Variables
name = profile_data['name']
city_name = profile_data['city_name']
city_code = profile_data['city_code']
current_hour = datetime.datetime.now().hour
music_path = profile_data['music_path']

play_music.mp3gen(music_path)

if 5 <= current_hour < 12:
    tts('Good morning ' + name + ' systems are now ready to run.  what is your command.')
elif 12 <= current_hour < 18:
    tts('Good afternoon ' + name + 'systems are now ready to run.  what is your command.')
else:
    tts('Good evening ' + name + 'systems are now ready to run.  what is your command.')
"""
def process_command(speech_text):
   global stopwatch_instance
   pass
"""

import subprocess

def fix_audio_logic():
    # Use your SoundBlaster's long name here
    SB_NAME = "alsa_output.usb-Creative_Technology_Ltd_Sound_Blaster_Play__3_00311390-00.analog-stereo"

    try:
        # Force PulseAudio to switch to the SoundBlaster
        subprocess.run(["pactl", "set-default-sink", SB_NAME], check=True)
        # Ensure it's not muted and volume is audible
        subprocess.run(["pactl", "set-sink-mute", SB_NAME, "0"], check=True)
        subprocess.run(["pactl", "set-sink-volume", SB_NAME, "85%"], check=True)

        return "Audio routing fixed. I am now using the SoundBlaster."
    except Exception as e:
        return f"I couldn't fix the audio. Is the device plugged in? Error: {e}"


def main():

   stopwatch_instance = Stopwatch() #create a stopwatch instance so that we can use the Stopwatch class

   if args.text: #text input mode
      while True:
         keyboard_input = input("Enter you command: ")
         if keyboard_input.lower() == "exit":
            break #exit loop when the user types 'exit'
         brain.neural_network(name, keyboard_input, city_name, city_code, stopwatch_instance, music_path) #process text-based commands

   else: #speech input mode
      r = sr.Recognizer()

      #suppress ALSA/JACK noise during audio capture
      stderr_backup = sys.stderr
      sys.stderr = open(os.devnull, 'w')
      try:
          m = sr.Microphone(device_index=2)
      finally:
          sys.stderr.close()
          sys.stderr = stderr_backup

      with m as source:
          print("Adjusting for ambient noise...Please be quiet.")
          r.adjust_for_ambient_noise(source, duration=1)
          print("Set minimum energy threshold to {}".format(r.energy_threshold))

          while True:
              print("Listening...") #print("stopwatch instance ", stopwatch_instance.is_running)
              r.pause_threshold = 1
              #suppress ALSA/JACK noise during microphone setup
              stderr_backup = sys.stderr
              sys.stderr = open(os.devnull, 'w')
              try:
                  audio = r.listen(source, phrase_time_limit = 10.0)
              finally:
                  sys.stderr.close()
                  sys.stderr = stderr_backup
              speech_text = "" #Initialize the speech_text to prevent crashes if no speech.

              try:
                  speech_text = r.recognize_google(audio, language='en-US').lower().replace("'","")
                  print("Recognizing and transcribing what you said...")
                  print(f"Computer thinks you said: '{speech_text}'")

                  if "fix audio" in speech_text:
                      print("Executing manual audio override...")
                      result_message = fix_audio_logic()
                      tts(result_message)
                      continue  # Jump back to the start of the loop

                  brain.process_command(speech_text, stopwatch_instance)
                  import time
                  time.sleep(1)

                  print("stopwatch instance ", stopwatch_instance.is_running)
              except sr.UnknownValueError:
                  print("Computer didn't understand.")
                  #tts("I do not understand")

              except sr.RequestError as e:
                  print("Could not request results from Google Speech Recognition service; {0}".format(e))

              if speech_text.strip(): #only process if something is actually said
                  brain.neural_network(name, speech_text, city_name, city_code, stopwatch_instance, music_path)
                  time.sleep(1)
              else:
                  print("No speech detected. Waiting for next command.")
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] Uncaught exception in main(): {e}")
        tts("A critical error occurred. Restarting required.")

