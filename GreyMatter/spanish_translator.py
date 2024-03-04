#!/usr/bin/env python3
#This is from 'Make Python Talk: Build apps with voice control and speech recognition' chapter 16

#You will need to install pip install translate for this code to work
#current bugs: the VA repeats 'ok we will practice spanish' and it only runs thru the code once.

from io import BytesIO

import speech_recognition as sr
import translate
from translate import Translator
from GreyMatter.SenseCells.tts_engine import tts
#instead of from gtts import gTTS
from pydub import AudioSegment #need to download with sudo install pydub
from pydub.playback import play

#Initiate speech recognition
speech = sr.Recognizer()

#Specify the input and output languages
#translator = Translator(from_lang = "en", to_lang = "es")

lang_abbr = {"english":"en",
    "spanish": "es",
    "french": "fr"
}

#tts("What language do you want to practice? You can choose spanish or french.")


def language_selection(language):
    translator = Translator(from_lang='en', to_lang=lang_abbr[language])
    #tts(f"Ok, we'll practice {language}.")
    if language == 'spanish':
        spanish_practice(translator)
    elif language == 'french':
        french_practice(translator)
    else:
        tts("Sorry, only spanish and french are currently supported.")

#capture the spoken english


def spanish_practice():
    while True:
        tts("Say something in english")
        print("Listening....")

        with sr.Microphone() as source:
            speech.adjust_for_ambient_noise(source)

            try:
                audio = speech.listen(source, phrase_time_limit = 3.5)
                my_input = speech.recognize_google(audio, language="en")
                print(f"You said {my_input}")
            except sr.UnknownValueError:
                print("Could not understand audio.")
                my_input = "" #Set default value if audio not understood
            #check if the user wants to stop
            if my_input.lower() == "stop":
                break  #break out of the loop

#do the actual translation
            if my_input:
                translator = Translator(from_lang = 'en', to_lang = 'es')
                translation = translator.translate(my_input)
                print(f"The translation is: {translation}")
                tts(translation)
            else:
                tts("Please try again.")

        tts("Say something in spanish")
        print("Listening...")

#capture spoken spanish
        with sr.Microphone() as source:
            speech.adjust_for_ambient_noise(source)
            try:
                audio = speech.listen(source, phrase_time_limit = 3.5)
                my_input = speech.recognize_google(audio, language='es')
                print(f"You said {my_input}")
            except sr.UnknownValueError:
                pass

        #check if user wants to stop
            if my_input.lower() == "stop":
                break

            if my_input:
                translator = Translator(from_lang = 'es', to_lang = 'en')
                translation = translator.translate(my_input)
                print(f"The translation is {translation}")
                tts_english = tts(translation, lang = 'en')
                tts(translation, lang = 'en')
            else:
                tts("Please try again.")
