from GreyMatter import tell_time, general_conversations

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

   if check_message(['who',' are', 'you']):
      general_conversations.who_are_you()
         #if the message is true then call the function

   elif check_message(['tell', 'joke']):
      general_conversations.tell_me_a_joke()

   elif check_message(['when', 'created']):
      general_conversations.when_were_you_created()

   elif check_message(['when', 'born']):
      general_conversations.when_where_you_born()

   elif check_message(['how','are','you','doing']):
      general_conversations.how_are_you()

   elif check_message(['i am', 'doing', 'well', 'fine', 'good']):
      general_conversations.i_am_doing_well_thank_you()

   elif check_message(['who am', 'i']) or check_message([('what','is','my', 'name']) or check_message(['what\'s my name']):
      general_conversations.who_am_i()
    
   elif check_message(['time']) or check_message(['what', 'time', 'is', 'it']):
      tell_time.what_is_time()

   elif check_message(['what','day','is','it']) or check_message(['what', 'day', 'of', 'the', 'week', 'is','it']):
      tell_time.what_is_day()

   elif check_message(['what', 'is', 'the', 'date', 'today']) or check_message(['current', 'date']))
      tell_time.what_is_date()

   elif check_message(['how', 'many', 'days', 'remaining', 'until']):
      #find the index of the word "until"
      #note that the speaker must ask for the date in the format of MM:DD:YYYY, in that order
      until_index = words.index('until')

   #extract the date provided by the speaker
      date_words = words[until_index + 1:]

   #convert the date words into numbers (assuming the sdate is proveddided i the format "MM-DD-YYYY"   
         month = int(date_words[0])
         day = int(date_words[1])   
         year = int(date_words[2])
         tell_time.days_from_now(year, month, day)
      
   else:
      #if not, then call the function 'i don't understand
      general_conversations.undefined()
