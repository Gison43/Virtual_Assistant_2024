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

#programmatically edit the default voice file for pitch
#pitch num1 num2 : num1 = from 100 to 425 num2 = 150 to 475

filename = "/usr/lib/arm-linux-gnueabihf/espeak-data/voices/default"

#instantiate the filesClass class with filename and address
fc = filesClass(filename)

lines = fc.readFile()

#after doing the above we can see that the pitch line we are in 
#is on line E in th efile
#we can print out line 5 just to be sure and check our work
print (lines[5])

#modify line 5 with new pitch number

lines[5] = "pitch 100 150 \n"
print (lines[5])

#call the writefile method to update the file with new pitch numbers
fc.writeFile(lines)
