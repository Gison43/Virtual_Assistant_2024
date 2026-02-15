import speech_recognition as sr
from GreyMatter.SenseCells.tts_engine import tts
import time

def get_user_input():
   r = sr.Recognizer()
   # Give the main brain 0.8 seconds to release the ReSpeaker hardware
   time.sleep(0.8) 
   
   try:
       # We must use device_index=2 to match your ReSpeaker
       with sr.Microphone(device_index=2, sample_rate=16000) as source:
          print("Listening for your follow-up...")
          r.pause_threshold = 0.5
          audio = r.listen(source, phrase_time_limit=5)
          
       speech_text = r.recognize_google(audio, language='en-US').lower().replace("'","")
       return speech_text
   except Exception as e:
       print(f"Follow-up Error: {e}")
       return None
