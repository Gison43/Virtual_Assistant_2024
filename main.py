#!/usr/bin/env python3
#This is Google Speech Recognition python file from 
#the book Building a Virtual Assistant  with RPi" year 2016

import sys
import os
import time

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


"""
def process_command(speech_text):
   global stopwatch_instance
   pass
"""

def fix_audio_logic():
    """Forces pulseAudio to use the ReSpeaker HAT as the default audio device"""
    # Use your SoundBlaster's long name here, but now I changed it to the ReSpeaker
    SB_NAME = "alsa_output.platform-bcm2835_audio.analog-stereo"

    try:
        Force PulseAudio to switch to the SoundBlaster
        subprocess.run(["pactl", "set-default-sink", SB_NAME], check=True)
        Ensure it's not muted and volume is audible
        subprocess.run(["pactl", "set-sink-mute", SB_NAME, "0"], check=True)
        subprocess.run(["pactl", "set-sink-volume", SB_NAME, "60%"], check=True)

        return "Audio routing fixed. I am now using the SoundBlaster."
    except Exception as e:
        return f"I couldn't fix the audio. Is the device plugged in? Error: {e}"


def main():
   print("Initializing main systems...")
   play_music.mp3gen(music_path)
   stopwatch_instance = Stopwatch() #create a stopwatch instance so that we can use the Stopwatch class
    
   if args.text: #text input mode
       while True:
           keyboard_input = input("Enter you command: ")
           if keyboard_input.lower() == "exit":
               break #exit loop when the user types 'exit'
           brain.neural_network(name, keyboard_input, city_name, city_code, stopwatch_instance, music_path) #process text-based commands
   
   else: #speech input mode
       r = sr.Recognizer()
       r.pause_threshold = 0.5
         
       try:
          m = sr.Microphone(device_index=2, sample_rate = 16000)
       except Exception as e:
            print(f"Hardware Error {e}")
            return
   
       with m as source:
             print("Adjusting for ambient noise...Please be quiet.")
             r.adjust_for_ambient_noise(source, duration=1)
             print("Set minimum energy threshold to {}".format(r.energy_threshold))
   
             while True:
                 print("Listening...") #print("stopwatch instance ", stopwatch_instance.is_running)
                 r.pause_threshold = 1
                 
                 try:
                     audio = r.listen(source, phrase_time_limit = 10.0)
                     speech_text =""
                     speech_text = r.recognize_google(audio, language='en-US').lower().replace("'","")
                     print("Recognizing and transcribing what you said...")
                     print(f"Computer thinks you said: '{speech_text}'")
   
                     if "fix audio" in speech_text:
                         print("Executing manual audio override...")
                         result_message = fix_audio_logic()
                         tts(result_message)
                         continue  # Jump back to the start of the loop
   
                     brain.process_command(speech_text, stopwatch_instance)
   
                     print("stopwatch instance ", stopwatch_instance.is_running)
   
                     if speech_text.strip(): #only process if something is actually said
                         brain.neural_network(name, speech_text, city_name, city_code, stopwatch_instance, music_path)
   
                 except sr.UnknownValueError:
                     print("Computer didn't understand.")
                     #tts("I do not understand")
   
                 except sr.RequestError as e:
                     print("Could not request results from Google Speech Recognition service; {0}".format(e))
             
if __name__ == "__main__":
    try:
        # 1. FIX THE AUDIO ROUTING FIRST
        print("[SYSTEM] Initializing audio routing...")
        audio_status = fix_audio_logic()
        print(f"[SYSTEM] {audio_status}")
        
        # 2. WAIT FOR HARDWARE TO SETTLE
        time.sleep(4) 

        # 3. DO THE GREETING (Moved from the top of the script)
        current_hour = datetime.datetime.now().hour
        if 5 <= current_hour < 12:
            greeting = 'Good morning ' + name + ', systems are now ready. What is your command?'
        elif 12 <= current_hour < 18:
            greeting = 'Good afternoon ' + name + ', systems are now ready. What is your command?'
        else:
            greeting = 'Good evening ' + name + ', systems are now ready. What is your command?'
        
        print(f"[SYSTEM] Greet: {greeting}")
        tts(greeting)
        
        # 4. WAIT FOR GREETING TO FINISH BEFORE OPENING MIC
        # If we open the mic while TTS is playing, we get a "Device Busy" error.
        time.sleep(6) 

        # 5. START THE MAIN LOOP
        main()

    except KeyboardInterrupt:
        print("\n[SYSTEM] Manual shutdown detected.")
    except Exception as e:
        print(f"[ERROR] Uncaught exception: {e}")
        tts("A critical error occurred. Restarting required.")

