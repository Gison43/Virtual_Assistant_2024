import os
from playsound import playsound
import time
import speech_recognition as sr
from gtts import gTTS

def speak(text):
   tts = gTTS(text=text, lang='en')
   filename = "voice.wav"
   tts.save(filename)


speak("hello Luke")

playsound("voice.wav")
