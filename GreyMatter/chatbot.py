import aiml
import speech_recognition as sr
from SenseCells.tts_engine import tts

# Initialize the AIML interpreter
kernel = aiml.Kernel()
kernel.learn("yak_test.aiml")

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Function to capture user speech input
def get_audio():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        speech_text = recognizer.recognize_google(audio).lower()
        print("User said:", speech_text)
        return speech_text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""

# Main loop for interaction
while True:
    # Get user input through speech
    user_input = get_audio()

    # Respond based on user input using AIML
    if user_input:
        response = kernel.respond(user_input)
        print("Bot:", response)
        tts(response)  # Speak the response using text-to-speech
