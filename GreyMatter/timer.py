# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 10:46:43 2024

@author: Phyco
"""

from GreyMatter.SenseCells.tts_engine import tts

import datetime

def stopwatch():
    start_time = None
    split_start_time = None
    
    
    def start():
        """Starts the timer"""
        nonlocal start_time
        start_time = datetime.datetime.now()
        tts("Let's go.")
        return start_time

    def stop():
        """Stops the timer.  Returns the time elapsed"""
        stop_time = datetime.datetime.now()
        total_time = (stop_time - start_time)
        tts(f"The stopwatch has been stopped and the total time is" {total_time} "minutes.")
        return stop_time

    def now():
        """Returns the current time with a message"""
        current_time = (datetime.datetime.now())
        tts("The stopwatch is at" {current_time})
        return current_time

    def elapsed():
        """Time elapsed since start was called"""
        time_elapsed = (datetime.datetime.now() - start_time)
        hours, remainder = divmod(time_elapsed.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_string = ""
        if hours > 0:
            time_string += f"{int(hours)} {'hour' if hours == 1 else 'hours'}"
        if minutes > 0:
            time_string += f"{int(minutes)} {'minutes' if minutes == 1 else 'minutes'}"
        if seconds > 0:
            time_string += f"{int(seconds)} {'second' if seconds == 1 else 'seconds'}"
        tts("Time elapsed since the start is" {time_string})
        return time_elapsed
    
    def split():
        nonlocal split_start_time
        split_start_time = datetime.datetime.now()
        tts(f"Split started at: {split_start_time})
        return split_start_time
    
    def unsplit():
        """Stops a split. Returns the time elapsed since split was called"""
        split_started = (datetime.datetime.now() - split_start_time)
        return split_started
        tts("Unsplitting the timer")
