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
        if lang == 'es':
            # Generate speech and pipe it directly to hardware card 2
            command = f'espeak -v es "{message}" --stdout | aplay -D hw:2'
        else:
            # Default voice piped directly to hardware card 2
            command = f'espeak "{message}" --stdout | aplay -D hw:2'
        
        # Use shell=True because we are using a pipe (|)
        subprocess.Popen(command, shell=True)
