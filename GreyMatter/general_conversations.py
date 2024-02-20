import random
from GreyMatter.SenseCells.tts_engine import tts

def who_are_you():
   messages = ['I am computer, your dedicated and intelligent assistant.', 'Computer, god damn it did I not tell you before?', 'You keep asking me that! I am Computer.']
   tts(random.choice(messages))

def how_are_you():
   tts('I am doing well, and you?')

def i_am_doing_well_thank_you():
   tts('That is nice')

def when_were_you_born():
   tts('I was created on February 15 2024')

def tell_me_a_joke():
   jokes = ['what do you call a magical dog? A labracadabrador.', 'What do you call a pony with a cough? A little horse', 'Why was six scared of seven? Because seven ate nine.', 'What do you call a woman with one leg? Eileen',
   'What did the pirate say when he turned 80? Aye matey.']
   tts(random.choice(jokes))

def when_birthday():
   tts('Your birthday is July 15.  You were born in 1978.')
       
def when_were_you_created():
   tts('I was created on February 12 2024')

def who_am_i(name):
   tts('Well, you are ' + name + ', of course! A brilliant, chemistry technologist working for environment and climate change canada.')

def undefined():
   tts("I don't know what that means!")
