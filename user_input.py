import speech_recognition as sr
from GreyMatter.SenseCells.tts_engine import tts
import time

def get_user_input():
   r = sr.Recognizer()
   # Wait for main.py to fully release the hardware
   time.sleep(1.0) 
   
   # Try 3 times to grab the mic
   for attempt in range(3):
       try:
           # Match device_index=2 from your main.py
           with sr.Microphone(device_index=2, sample_rate=16000) as source:
              print(f"Listening for follow-up (Attempt {attempt+1})...")
              r.pause_threshold = 0.5
              # Increased timeout slightly for better usability
              audio = r.listen(source, phrase_time_limit=5)
              
           speech_text = r.recognize_google(audio, language='en-US').lower().replace("'","")
           return speech_text
           
       except Exception as e:
           print(f"Follow-up Error (Attempt {attempt+1}): {e}")
           time.sleep(1.0) # Wait a second before trying again
           
   return None
