# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 18:01:05 2024

@author: Phyco
"""

import subprocess as cmdLine
cmdLine.call("clear")
#import the espeak class from espeak.py
from espeakng import ESpeakNG
from filesClass import filesClass
#from GreyMatter.SenseCells.tts_engine import tts

#programmatically edit the default voice file for pitch
#pitch num1 num2 : num1 = from 100 to 425 num2 = 150 to 475

#voices in espeak-ng are found in the espeak-ng-data folder
filename = "/usr/lib/arm-linux-gnueabihf/espeak-ng-data/voices/default"

#instantiate the filesClass class with filename and address
fc = filesClass(filename)

try:
    lines = fc.readFile()
    for pitch in range(100, 400, 25):
        lines = fc.readFile()
        print (lines[5])

        #modify lines[5] here with new pitch numbers
        lines[5] = "pitch " + str(pitch) + " " + str(pitch + 25) + "\n" 
        print (lines[5])

        fc.writeFile(lines)

        voice1 = "default"
        esng = ESpeakNG(voice1)
        speech = "the pitch has been set to " + str(pitch)
        esng.say(speech)

        cmdLine.run("clear")

        #check if espeak voice output occured
        if esng.last_exit_code !=0:
            print("No audio output from espeak.")

except FileNotFoundError:
    print("File not found.  Unable to access the specified file.")
except PermissionError:
    print("Permission denied.  You do not have sufficient permissions to access this file.")
except NoAudioOutputError:
    print("No audio output detected. Please check your audio settings.")
#the next one prints the actual exception error if it doesn't match the other 3.
except Exception as e:
    print("f"An unexpected error occurred: {e}")
        #modify line 5 with new pitch number

#lines[5] = "pitch 100 150 \n"
print (lines[5])

#call the writefile method to update the file with new pitch numbers
fc.writeFile(lines)