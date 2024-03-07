# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 17:51:09 2024

@author: Phyco
"""

class filesClass:
    
    #__init__ defines the file to be used.
    def __init__(self, filename):
        self.filename = filename
        
    def readFile(self):
        #open the file for reading
        with open(self.filename, "r") as voice:
            #Read the lines into a list called lines
            lines = voice.readlines()
            #set a line counter to zero.
            lineNumber = 0
            #print out the lines with line numbers
            for line in lines:
                print(lineNumber, end = "") #end="" prevents an extra line return
                print("", end = "") #printing a space
                print(line, end = "") #now printing the line
                lineNumber += 1 #increments the line number
            print("\n") #add an extra line return when finished
            return lines #return the list of lines from the file
        
    def writeFile(self, lines):
        with open(self.filename, 'w') as outfile:
            for line in lines:
                outfile.write(line)
                