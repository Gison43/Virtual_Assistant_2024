#!/usr/bin/env python3

"""
Module for calculating the area of a rectangle.
This is designed to be called from brain.py when the user asks the VA to calculate area.
"""

from GreyMatter.SenseCells.tts_engine import tts
from user_input import get_user_input  # Uses the same input function your VA already uses

def extract_numerical_value(input_text):
    """
    Extracts the first valid number from the input text.
    If no valid number is found, returns None.
    """
    words = input_text.split()
    for word in words:
        try:
            return float(word)
        except ValueError:
            continue
    return None

def calculate_rectangle_area():
    """
    Guides the user through providing the length and width of a rectangle,
    calculates the area, and announces the result.
    """

    tts('What is the length of the rectangle in centimeters?')
    inp1 = get_user_input()  # Voice or text input (depends if you're in speech or text mode)

    length = extract_numerical_value(inp1)
    if length is None:
        tts("I didn't catch a valid length. Please try again.")
        return

    tts(f"You said {length} centimeters.")

    tts('What is the width of the rectangle?')
    inp2 = get_user_input()

    width = extract_numerical_value(inp2)
    if width is None:
        tts("I didn't catch a valid width. Please try again.")
        return

    tts(f"You said {width} centimeters.")

    area = length * width
    tts(f"The area of the rectangle is {area} square centimeters.")
