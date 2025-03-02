#!/usr/bin/env python3

from GreyMatter.SenseCells.tts_engine import tts

#This code has the VA calculate the area of a rectangle or volume of a cube

#function to preprocess the input and extract numerical value
def extract_numerical_value(input_text):
    #split the input text by space
    words = input_text.split()
    #initialize the numerical value as none
    numerical_value = None
#Iterate over the words in the input
    for word in words:  #attempt to convert to word to a float
        try:
            numerical_value = float(word)
            break  #exit the loop if a numerical value is found
        except ValueError:
            continue  #continue to the next word if the conversion fails

    return numerical_value

#Ask the length of the rectangle
tts('What is the length of the rectangle in centimeters')

#convert the voice input to a variable inp1
inp1 = voice_to_text()
length = extract_numerical_value(inp1)
tts(f"You just said {inp1}centimeters.")

#ask the width of the rectangle
tts('What is the width of the rectangle')

#convert the voice input to a variable inp2
inp2 = voice_to_text()
width = extract_numerical_value(inp2)
tts(f"You just said {inp2}centimeters")

#Calculate the area
area = length * width
#speak the results
tts(f"The area of the rectange is {area} square centimeters")
