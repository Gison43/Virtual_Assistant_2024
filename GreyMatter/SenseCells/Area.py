from GreyMather import tts_engine

#This code has the VA calculate the area of a rectangle or volume of a cube

#Ask the length of the rectangle
tts('What is the length of the rectangle in centimeters')

#convert the voice input to a variable inp1
inp1 = voice_to_text()
tts('You just said {inp1}.')
#ask the width of the rectangle

tts('What is the width of the rectangle')
#convert the voice input to a variable inp2
inp2 = voice_to_text()
tts('You just said {inp2}.')
#Calculate the area
area = float(inp1)*float(inp2)
#speak the results
tts('The area of the rectange is {area} centimeters squared')
