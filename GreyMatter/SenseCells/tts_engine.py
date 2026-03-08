#!/usr/bin/env python3

import subprocess
import sys
import time

def tts(message, lang='en-US'):
   #Converts message to speech using PicoTTS for better pronunciation and targest ReSpeaker 2-Mics HAT
   tts_engine = []
   """
   Converts message to speech using subprocess.  Popen to prevent blocking.
   """

   if sys.platform == 'darwin':
      #Keep Mac support for testing
      subprocess.call(['say', message])

   elif sys.platform.startswith('linux'):
    # We use 'plughw:2' to handle resampling and '-c 2' to force stereo
    # This removes the need for the slow 'sox' middleman
      device = "plughw:2,0"
      temp_wav = "tts_output.wav"
        
        try:
            # 1. Generate the high-quality wav file
            # PicoTTS handles the language phonetics much better than eSpeak
            subprocess.run(['pico2wave', '-l', lang, '-w', temp_wav, message], check=True)
            
            # 2. Play it directly to the ReSpeaker
            # We don't need shell=True here, which is safer and faster
            subprocess.run(['aplay', '-D', device, temp_wav], check=True)
            
        except Exception as e:
            print(f"TTS Error: {e}")
            # Fallback to a basic aplay if pico fails
            os.system(f'espeak "{message}" | aplay -D {device}')
            
        finally:
            # Cleanup to keep your project folder tidy
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
