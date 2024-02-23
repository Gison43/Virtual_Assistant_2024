#This is from 'Make Python Talk: Build apps with voice control and speech recognition' chapter 16

from io import BytesIO

from tts_engine import tts
from pydub import AudioSegment #need to download with sudo install pydub
from pydub.playback import play

lang_abbre = {"english":"en",
          "spanish": "es",
          "french": "fr"}

lang = tts("What language do you want to use? You can choose english, spanish or french.")
   if check_message(['spanish']):
      spanish_translator.spanish()
          tts("Ok, we'll practice spanish.")
         #if the message is true then call the function

   elif check_message(['french']):
      spanish_translator.french()
          tts("Ok, we'll practice french.")

