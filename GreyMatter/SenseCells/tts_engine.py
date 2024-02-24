import os
import sys

def tts(message, lang=None):
   """
   this function takes a message as an argument and converts it to speech depending on the OS.
   Optionally, a language code can be provided to specify the language of the speech
   """

   if sys.platform == 'darwin':
      tts_engine = 'say'
      return os.system(tts_engine + ' ' + message)
   elif sys.platform == 'linux2' or sys.platform == 'linux':
      if lang == 'es':
         tts_engine = 'espeak -v es'
      else:
         tts_engine = 'espeak'
   return os.system(tts_engine + ' "' + message + '"')

#tts("Hi handsome, this is computer.")
