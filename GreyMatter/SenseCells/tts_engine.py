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
   elif sys.platform.startswith('linux'):
        # This is the 'Force conversion' logic we just verified
        # It converts espeak output to 16kHz Stereo for the ReSpeaker HAT
        aplay_cmd = "sox -t wav - -r 16000 -c 2 -t wav - | aplay -D hw:2"
        
        if lang == 'es':
            command = f'espeak -v es "{message}" --stdout | {aplay_cmd}'
        else:
            command = f'espeak "{message}" --stdout | {aplay_cmd}'
        
        # We use shell=True to allow the piping (|) between espeak, sox, and aplay
        subprocess.Popen(command, shell=True)
