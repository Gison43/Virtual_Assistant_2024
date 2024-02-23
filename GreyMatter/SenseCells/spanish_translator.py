#This is from 'Make Python Talk: Build apps with voice control and speech recognition' chapter 16

from io import BytesIO

import speech_recognition as sr
from tts_engine import tts
from translate import Translator
from pydub import AudioSegment #need to download with sudo install pydub
from pydub.playback import play

#Initiate speech recognition
speech = sr.Recognizer()

#Specify the input and output languages
translator = Translator(from_lang="en", to_lang="es")

lang_abbr = {"english":"en",
          "spanish": "es",
          "french": "fr"}

tts("What language do you want to use? You can choose english, spanish or french.")
#specify the input/output languages
   if check_message(['spanish']):
      translator = Translator(from_lang="en", to_lang="es")
      spanish_translator.spanish()
      tts("Ok, we'll practice spanish.")
         #if the message is true then call the function

   elif check_message(['french']):
      translator = Translator(from_lang="en", to_lang="fr")
      spanish_translator.french()
      tts("Ok, we'll practice french.")

tts("Say something in english")

#capture the spoken english
with sr.Microphone() as source:
   speech.adjust_for_ambien_noise(source)
      try:
         audio = speech.listen(source)
         my_input = speech.recognize_google(audio, language="en")
         print(f"You said {my_input}")
      except sr.UnknownValueError:
         print("Could not understand audio.")
#do the actual translation
translation = translator.translate(my_input)
print(translation)
#convert text to speech in Spanish
tts_spanish = tts(text=translation, lang='es')
#create a temporary file
voice = BytesIO()
#save the voice output as an audio file
tts_spanish.write_to_fp(voice)
#play the audio file
voice.seek(0)
play(AudioSegment.from_mp3(voice))

#Prompt you to say something in Spanish
tts("Say something in spanish")
#capture spoken spanish
with sr.Microphone() as source:
          speech.adjust_for_ambient_noise(source)
          try:
             audio = speech.listen(source)
             my_input = speech.recognize_google(audio, language='es')
             print(f"You said {my_input}")
          except sr.UnknownValueError:
             pass
Translator = Translator(from_lang='es', to_lang='en')
translation = translator.translate(my_input)
print(translation)
#convert text to speech in Spanish
tts_english = tts(text=translation, lang='en')
#create temp file
voice = BytesIO()
#save voice output as an audio file
tts_english.write_to_fp(voice)
#play audio file
voice.seek(0)
play(AudioSegment.from_mp3(voice))

