import timer
from SenseCells.tts_engine import tts
import sys
sys.path.append("/home/pi/Virtual_Assistant_2024")
from brain import check_message
import speech_recognition as sr



stopwatch_started = False  # Track if the stopwatch is currently running

def check_message(check):
      words_of_message = speech_text.split()
      if set(check).issubset(set(words_of_message)):
         return True
      else:
         return False

def get_user_input():
    # Implement your code to get user input here
    speech = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speech.adjust_for_ambient_noise(source)
        try:
            audio = speech.listen(source, phrase_time_limit = 3.5)
            my_input = speech.recognize_google(audio, language='en')
            print(f"You said {my_input}")
            return my_input
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an error in retrieving speech recognition results.")
            return ""

while True:
    speech_text = get_user_input()  # Get user input

    if check_message(['start', 'stopwatch']):
        if not stopwatch_started:
            timer.start()  # Start the stopwatch if it's not already running
            stopwatch_started = True
            tts("Let's go.")  # Inform the user that the stopwatch has started
        else:
            tts("The stopwatch is already running.")

    elif check_message(['stop', 'stopwatch']):
        if stopwatch_started:
            total_time = timer.stop()  # Stop the stopwatch and get the total time elapsed
            tts(f"The stopwatch has been stopped and the total time is {total_time} minutes.")
            stopwatch_started = False
        else:
            tts("The stopwatch is not running.")

    elif check_message(['time', 'elapsed', 'stopwatch']):
        if stopwatch_started:
            current_time = timer.elapsed()  # Get the current elapsed time on the stopwatch
            tts(f"The current time elapsed on the stopwatch is {current_time} minutes.")
        else:
            tts("The stopwatch is not running.")

    elif check_message(['exit']):
        if stopwatch_started:
            total_time = timer.stop()  # Stop the stopwatch and get the total time elapsed
            tts(f"The stopwatch has been stopped and the total time is {total_time} minutes.")
        tts("Exiting stopwatch program.")
        break  # Exit the loop and end the program

    else:
        tts("Command not recognized. Please try again.")  # Inform the user of unrecognized commands

get_user_input()
