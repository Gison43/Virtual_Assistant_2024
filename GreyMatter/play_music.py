#usr/bin/python3

import os
import sys
import random

from .SenseCells.tts_engine import tts

def mp3gen(music_path):
    """
    This function finds all the MP3 files in a folder and its subfolders and
    returns a list:
    """
    music_list = []
    for root, dirs, files in os.walk(music_path):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                music_list.append(os.path.join(root, filename.lower()))
    return music_list

def music_player(file_name):
    """
    This function takes the name of a music file as an argument and plays it 
    depending on the OS.
    """
    if sys.platform == 'darwin':
        player = "afplay '" + file_name+ "'"
        return os.system(player)
    elif sys.platform == 'linux2' or sys.platform == 'linux':
        player = "vlc '" + file_name +"'"
        return os.system(player)

def play_random(music_path):
    try:
        music_listing = mp3gen(music_path)
        music_playing = random.choice(music_listing)
        #extract the filename from the full path
        music_filename = os.path.basename(music_playing)
        #remove the file extension ".mp3"
        music_filename = os.path.splitext(music_filename)[0]
        tts("Now playing: " + music_filename)
        music_player(music_playing)
    except IndexError as e:
        tts('No music files found.')
        print("No music files found: {0}".format(e))

def play_specific_music(speech_text, music_path):
    words_of_message = speech_text.split()
    words_of_message.remove('play')
    cleaned_message = ' '.join(words_of_message)
    music_listing = mp3gen(music_path)

    for i in range(0, len(music_listing)):
        if cleaned_message in music_listing[i]:
            music_player(music_listing[i])
