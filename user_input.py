import speech_recognition as sr
from GreyMatter.SenseCells.tts_engine import tts

def get_user_input():
   r = sr.Recognizer()
   import time
   # Give the main loop half a second to release the hardware
   time.sleep(0.5) #prevents microphone lockup
   
   try:
       # Match device_index=2 and sample_rate=16000 from your main.py
       with sr.Microphone(device_index=2, sample_rate=16000) as source:
          print("Listening for follow-up...")
          r.pause_threshold = 0.5
          audio = r.listen(source, phrase_time_limit=5)

       speech_text = r.recognize_google(audio, language='en-US').lower().replace("'","")
       return speech_text
   except Exception as e:
       print(f"Follow-up Mic Error: {e}")
       return None
