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
    tts(f"Ok, we'll practice {language}.")
    if language == 'spanish':
        spanish_practice(translator)
    elif language == 'french':
        french_practice(translator)
    else:
        tts("Sorry, only spanish and french are currently supported.")

#capture the spoken english


def spanish_practice(translator):
    tts("Say something in english")

    with sr.Microphone() as source:
        speech.adjust_for_ambient_noise(source)

        try:
            audio = speech.listen(source)
            my_input = speech.recognize_google(audio, language="en")
            print(f"You said {my_input}")
        except sr.UnknownValueError:
             print("Could not understand audio.")
             my_input = "" #Set default value if audio not understood
    #do the actual translation
    if my_input:
        translation = translator.translate(my_input)
        print(f"The translation is: {translation}")
        tts(translation)
    else:
        tts("Please try again.")
        return
    tts("Say something in spanish")

    """#convert text to speech in Spanish
    tts_spanish = tts(translation, lang='es')
    #create a temporary file
    voice = BytesIO()
    #save the voice output as an audio file
    tts_spanish.write_to_fp(voice)
    #play the audio file
    voice.seek(0)
    play(AudioSegment.from_mp3(voice))
    """
#capture spoken spanish
    with sr.Microphone() as source:
        speech.adjust_for_ambient_noise(source)
        try:
            audio = speech.listen(source)
            my_input = speech.recognize_google(audio, language='es')
            print(f"You said {my_input}")
        except sr.UnknownValueError:
            pass

    if my_input:
        translation = translator.translate(my_input)
        print(f"The translation is {translation}")
        tts_english = tts(translation, lang = 'en')
        tts(translation, lang = 'es')
    else:
        tts("Please try again.")
        return
