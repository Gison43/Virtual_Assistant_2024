# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 10:46:43 2024

@author: Phyco

currently only the start, stop, elapsed time, reset, format time functions are working.

split times are not working well. It can spit time, but if I say stop, it brings up errors.

"""
import datetime

from .SenseCells.tts_engine import tts

class Stopwatch:
   def __init__(self):
      self.start_time = None
      self.is_running = False
      self.split_start_time = None
      self.splits = []
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
      self.is_running = False
      elapsed_time  = stop_time - self.start_time

      total_seconds = elapsed_time.total_seconds()

      #calculate the split times relative to start_time
      split_times = [split - self.start_time for split in self.splits]

      self.total_time += elapsed_time #accumulate the elapsed time
      #print("Type of elapsed_time:", type(elapsed_time))
      self.splits = [] #reset splits after stopping
      return total_seconds, [split.total_seconds() for split in split_times]

   def reset(self):
      """Resets the stopwatch to zero time """
      print("resetting the stopwatch")
      print("current total time before reset:", self.total_time)
      self.total_time = datetime.timedelta()
      self.is_running = False #stop the stopwatch
      print("Total time after reset:", self.total_time)

   def elapsed(self, start_time):
      """Time elapsed since start was called"""
      if self.start_time is None:
         raise RuntimeError("Stopwatch not started.")
         tts("The stopwatch has not started")
      time_elapsed = (datetime.datetime.now() - self.start_time)
      time_string = self.format_time(time_elapsed)
      return time_elapsed


   def split(self):
      if self.is_running:
         split_start_time = datetime.datetime.now()
         split_time = split_start_time - self.start_time  #should get a timedelta object here
         format_split = self.format_time(split_time)
         self.splits.append(split_time)
         tts(f"Split started at: {format_split}")
#      return split_start_time

   def unsplit(self):
      """Stops a split. Returns the time elapsed since split was called"""
      if self.is_running:
         tts("The stopwatch is running. Stop it first.")
      elif not self.splits:
         tts("No splits recorded.")
      else:
         split_time = self.splits.pop() #remove the last split time from the list
         time_string = self.format_time(split_time)
         tts(f"Split stopped.  Time elapsed since the split started is {time_string}.")

   def stop_split(self, split_index):
      if 0 <= split_index < len(self.splits):
         split_time = self.splits.pop(split_index)
         return split_time - self.start_time
      else:
         raise IndexError("Invalid split index")


   def reset_splits(self):
      #resets the split list
      self.splits = []

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
