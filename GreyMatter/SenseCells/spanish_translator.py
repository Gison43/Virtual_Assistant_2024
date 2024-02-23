#This is from 'Make Python Talk: Build apps with voice control and speech recognition' chapter 16

from io import BytesIO

from tts_engine import tts
from pydub import AudioSegment
from pydub.playback import play

lang_abbre = {"english":"en",
          "spanish": "es",
          "french": "fr"}

lang = tts("What language do you want to use? You can choose english, spanish or french.")
