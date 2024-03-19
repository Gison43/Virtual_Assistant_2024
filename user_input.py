import speech_recognition as sr
from GreyMatter.SenseCells.tts_engine import tts

def get_user_input():
   r = sr.Recognizer()
   with sr.Microphone() as source:
      print("Listening...")
      r.pause_threshold = 1
      audio = r.listen(source)

   try:
       speech_text = r.recognize_google(audio, language='en-US').lower().replace("'"," ")
       print("Recognizing and transcribing what you said..")
       print(f"Computer thinks you said {speech_text}")
       return speech_text
   except sr.UnknownValueError:
       print("Computer didn't understand.")
       return None
   except sr.RequestError as e:
       print("Could not request results from Google Speech Recognition service; {0}".format(e))
       return None
