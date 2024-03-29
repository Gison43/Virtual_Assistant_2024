#!/usr/bin/env python3

from user_input import get_user_input
from GreyMatter import tell_time, general_conversations, spanish_translator
from GreyMatter.SenseCells.tts_engine import tts
from GreyMatter.spanish_translator import language_selection
#from GreyMatter import french_translator

def brain(name, speech_text):
   """
   this function compares check vs speech_text to see if they are equal.  Also
   checks if the items in the list (specificed in the argument are present in 
   the user's speech.
   """
def check_message(check):
    words_of_message = speech_text.split()
    if set(check).issubset(set(words_of_message)):
        return True
    else:
        return False
    match check:
        case_check_message(['who' , 'are','you']):
            general_conversations.who_are_you()
            #if the message is true then call the function

    case _ if check_message(['tell','joke']):
        general_conversations.tell_me_a_joke()

    case _ if check_message(['how','long','until','my','birthday'] | check_message(['how', 'many', 'days', 'until', 'my', 'birthday']):
        tell_time.when_birthday()
   
    case _ if check_message(['what'| 'year','is it'] | check_message(['what', 'current', 'year']):
        tell_time.current_year()

    case _ if check_message(['how'| 'old'| 'am'| 'i']):
        tell_time.how_old()

    case _ if check_message(['calculate','area'| 'rectangle']):
        area()

    case _ if check_message(['when','my'| 'birthday']):
        general_conversations.when_birthday()

    case _ if check_message(['want','practice', 'language']):
        tts("What language would you like to practice? Spanish or French?")
      #listen for the user's response
        user_response = get_user_input()

      #check if the user wants to practic Spanish
        if 'spanish' in user_response:
            tts("Ok, we will practice Spanish.")
            language_selection('spanish')
        elif 'french' in user_response:
            tts("Ok, we will practice french.")
            language_selection('french')
        else:
            tts("Sorry, only spanish and french are currently supported.")

    case _ if check_message(['when'| 'new years']):
        tell_time.new_years_eve()

    case _ if check_message(['when'| 'created']):
        general_conversations.when_were_you_created()

    case _ if check_message(['when','born']):
        general_conversations.when_where_you_born()

    case _ if check_message(['how','are','you','doing']):
        general_conversations.how_are_you()

    case _ if check_message(['i am', 'doing', 'well', 'fine', 'good']):
        general_conversations.i_am_doing_well_thank_you()

    case _ if check_message(['who', 'am', 'i'] | check_message(['what','is','my', 'name']) | check_message(['what\'s my name']):
        general_conversations.who_am_i()

    case _ if check_message(['time'] | check_message(['what', 'time', 'is', 'it']):
        tell_time.what_is_time()

    case _ if check_message(['what','day','number']):
        tell_time.day_number()

    case _ if check_message(['what','day','is','it'] | check_message(['what', 'day', 'of', 'the', 'week', 'is','it']):
        tell_time.what_is_day()

    case _ if check_message(['what','month']):
        tell_time.what_month()

    case _ if check_message(['what', 'is', 'the', 'date','today'] | check_message(['current', 'date']):
        tell_time.what_is_date()

    case _ if check_message(['how', 'many', 'days', 'remaining', 'until']):
       #find the index of the word "until"
       #note that the speaker must ask for the date in the format of MM:DD:YYYY, in that order
        if all(word in words for word in ['how', 'many', 'days', 'remaining', 'until']):
            until_index = words.index('until')

   #extract the date provided by the speaker
            date_words = words[until_index + 1:]

   #convert the date words into numbers (assuming the date is provided in the format "MM-DD-YYYY"   
            month = int(date_words[0])
            day = int(date_words[1])
            year = int(date_words[2])

            tell_time.days_from_now(year, month, day)

    case _:
      #if not, then call the function 'i don't understand
        general_conversations.undefined()
