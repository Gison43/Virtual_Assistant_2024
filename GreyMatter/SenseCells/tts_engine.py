#!/usr/bin/env python3

import subprocess
import sys
import os

def tts(message, lang='en-US'):
    """
    Converts message to speech using PicoTTS and targets ReSpeaker 2-Mics HAT.
    """
    if sys.platform == 'darwin':
        subprocess.call(['say', message])

    elif sys.platform.startswith('linux'):
        # We use 'plughw:2,0' because the 'plug' part tells ALSA to 
        # automatically resample 16kHz to 44kHz, which reduces static.
        device = "plughw:2,0"
        temp_wav = "tts_output.wav"

        try:
            # 1. Generate the wav file
            subprocess.run(['pico2wave', '-l', lang, '-w', temp_wav, message], check=True)
            
            # 2. Play using aplay. 
            # Passing as a list is the cleanest way for subprocess.
            command = ['aplay', '-D', device, temp_wav]
            subprocess.run(command, check=True)

        except Exception as e:
            print(f"TTS Error: {e}")
        finally:
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
