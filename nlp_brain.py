#!/usr/bin/env python
# coding: utf-8

# In[27]:


from datetime  import datetime as dt, date
import random

today = dt.now().date()
now = dt.now()

def brain(text):
    text = text.lower()
    
    knowledge_base = {
         
         "who are you": random.choice (["I am computer, your dedicated and intelligent assistant.", "computer, God dammit did I not tell you before", "you keeping methat, I am computer."]),
         "tell me a joke": random.choice([ "what do you call a magical dog? A labracadabrador.", "What do you call a pony with a cough? A little horse", "Why was six scared of seven? Because seven ate nine.", "What do you call a woman with one leg? Eileen",
   "what did the pirate say when he turned 80? Aye matey."]),
         "how long until my birthday": "Your birthday is July 15.  You were born in 1978.",
         "when were you created": "I was created on February 12 2024",
         "how are you": "I am doing well, and you?",
         "what is your name": "I dont have a name yet",
         "what are you": "I am a fully functional, artificially intelligent, state of the art virtual assistant, and I am all yours, baby."
    }

    for key, response in knowledge_base.items():
         if key in text:
              return response

    if "time" in text:
       return f"it's {dt.now().strftime('%I:%M %p')}"
        
    return None
             
                     

   

     


# In[28]:


test_questions = [
    "who am i",
    "what are you",
    "tell me a joke",
    "what is the time",
    "something random i haven't taught you"
]

print("--- GreyMatter Brain Test ---")
for query in test_questions:
    # Call the brain function you defined in Cell 1
    response = brain(query) 
    
    print(f"YOU: {query}")
    print(f"GREYMATTER: {response}")
    print("-" * 30)


# In[ ]:




