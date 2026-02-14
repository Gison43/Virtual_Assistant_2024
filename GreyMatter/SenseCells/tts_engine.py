#!/usr/bin/env python3

import subprocess
import sys
import time

def tts(message, lang=None):
   #Initialize the variable as an empty list so it is always 'defined'
   tts_engine = []
   """
   Converts message to speech using subprocess.  Popen to prevent blocking.
   """

   if sys.platform == 'darwin':
      tts_engine = ['say', message]

   elif sys.platform.startswith('linux'):
    # We use 'plughw:2' to handle resampling and '-c 2' to force stereo
    # This removes the need for the slow 'sox' middleman
    command = f'espeak "{message}" --stdout | aplay -D plug:dmix  -r 44100 -f S16_LE'
    subprocess.call(command, shell=True)

    time.sleep(1)
