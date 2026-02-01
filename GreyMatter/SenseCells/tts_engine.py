#!/usr/bin/env python3

import subprocess
import sys

def tts(message, lang=None):
   #Initialize the variable as an empty list so it is always 'defined'
   tts_engine = []
   """
   Converts message to speech using subprocess.  Popen to prevent blocking.
   """

   if sys.platform == 'darwin':
      tts_engine = ['say', message]
   elif sys.platform == 'linux2' or sys.platform == 'linux':
      #for Raspberry Pi / Linux
      if lang == 'es':
         tts_engine = ['espeak', '-v', 'es', message]
      else:
         tts_engine = ['espeak', message]
   else:
      return

#Popen starts the process in the background
subprocess.Popen(tts_engine)
