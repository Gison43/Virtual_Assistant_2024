#!/usr/bin/env python3
"""
Created on Sat Mar  9 10:46:43 2024

@author: Phyco
"""
import datetime

class Stopwatch:
   def __init__(self):
      self.start_time = None
      self.is_running = False
      self.split_start_time = None
      self.total_time = datetime.timedelta()

   def start(self):
      """Starts the timer"""
      self.start_time = datetime.datetime.now()
      self.is_running = True
      return self.start_time

   def stop(self, start_time):
      """Stops the timer.  Returns the time elapsed"""
      if self.start_time is None:
         raise RuntimeError("Stopwatch not started.")
      stop_time = datetime.datetime.now()
      elapsed_time  = (stop_time - self.start_time)
      self.total_time += elapsed_time #accumulate the elapsed time
      #tts(f"The stopwatch has been stopped and the total time is {total_time} minutes.")
      print("Type of elapsed_time:", type(elapsed_time))
      self.is_running = False
      return elapsed_time

   def now(self):
      """Returns the current time with a message"""
      current_time = (datetime.datetime.now())
      tts("The stopwatch is at {current_time}")
      return current_time

   def reset(self):
      """Resets the stopwatch to zero time """
      self.total_time = datetime.timedelta()

   def elapsed(self, start_time):
      """Time elapsed since start was called"""
      if self.start_time is None:
         raise RuntimeError("Stopwatch not started.")
         tts("The stopwatch has not started")
      time_elapsed = (datetime.datetime.now() - self.start_time)
      time_string = self.format_time(time_elapsed)
      tts("Time elapsed since the start is {time_string}")
      return time_elapsed


   def split(self):
      self.split_start_time = datetime.datetime.now()
      tts(f"Split started at: {split_start_time}")
      return self.split_start_time

   def unsplit(self):
      """Stops a split. Returns the time elapsed since split was called"""
      if self.split_start_time is None:
         raise RuntimeError("Split not started")
         tts("Split not started")
      split_end = datetime.datetime.now()
      split_time = split_end - self.split_start_time
      time_string = self.format_time(split_time)
      tts(f"Split stopped.  Time elapsed since the split started is {time_string}.")

   def format_time(self, time_delta):
      """Formats the time delta into hours, minutes, and seconds"""
      print("Time delta:", time_delta)
      hours, remainder = divmod(time_delta.total_seconds(), 3600)
      minutes, seconds = divmod(remainder, 60)
      time_string = ""

      if hours > 0:
         time_string += f"{int(hours)} {'hour' if hours == 1 else 'hours'} "
      if minutes > 0:
         time_string += f"{int(minutes)} {'minute' if minutes == 1 else 'minutes'} "
      if seconds > 0 or time_string == "":
         time_string += f"{int(seconds)} {'second' if seconds == 1 else 'seconds'}"
      return time_string.strip()
