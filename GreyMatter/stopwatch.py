#!/usr/bin/env python3
"""
Created on Sat Mar  9 10:46:43 2024

@author: Phyco

currently only the start, stop, elapsed time, reset, format time functions are working.

split times are not working well. It can split time, but if I say stop, it brings up errors.

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
      if self.is_running:
          raise RuntimeError("Stopwatch is already running.")
          tts("The stopwatch is already running")
      self.start_time = datetime.datetime.now()
      self.is_running = True
      self.splits = []
      return self.start_time

   def stop(self):
      #Stops the timer.  Returns the time elapsed
      if self.start_time is None:
         raise RuntimeError("Stopwatch not started.")

      stop_time = datetime.datetime.now()
      self.is_running = False
      elapsed_time  = stop_time - self.start_time
      print("Type of elpased_time", type(elapsed_time))
      self.total_time += elapsed_time #accumulate total time

      total_seconds = elapsed_time.total_seconds()

      #convert start_time to a timedelta object
      start_timedelta = stop_time - self.start_time

      #calculate the split times relative to start_time
      split_seconds = [split.total_seconds() for split in self.splits]
      print("Split times:", split_seconds)

      self.total_time += elapsed_time #accumulate the elapsed time
      #print("Type of elapsed_time:", type(elapsed_time))
      self.splits = [] #reset splits after stopping

      tts(f"The stopwatch has stopped.  Total time: {self.format_time(elapsed_time)}")

      if split_seconds:
         split_messages = []
         for index, split in enumerate(split_seconds, 1):
            formatted_split = self.format_time(datetime.timedelta(seconds=split))
            split_messages.append(f"Split{index}: {formatted_split}")
            tts(" ".join(split_messages))
            
      return total_seconds, split_seconds

   def reset(self):
      """Resets the stopwatch to zero time """
      print("Resetting the stopwatch")
      print("Current total time before reset:", self.total_time)
      self.start_time = None
      self.total_time = datetime.timedelta()
      self.is_running = False #stop the stopwatch
      print("Total time after reset:", self.total_time)

   def elapsed(self, start_time=None):
      """Time elapsed since start was called"""
      if self.start_time is None:
         raise RuntimeError("The stopwatch has not started")
         tts("The stopwatch has not started")
      if self.is_running:
         time_elapsed = (datetime.datetime.now() - self.start_time)
      else:
         time_elapsed = self.total_time
      time_string = self.format_time(time_elapsed)
      return time_elapsed, time_string

   def split(self, title=None):
      if self.is_running:
         #split_start_time = datetime.datetime.now()
         if len(self.splits) >=5:
            tts("Maximum of 5 splits reached.")
            print("Maximum of 5 splits reached.")
            return
            
         current_time = datetime.datetime.now()
         
         if self.splits:
              split_time = current_time - self.splits[-1]['time'] #time since last split
         else:
              split_time = current_time - self.start_time #time since stopwatch started
            
         format_split = self.format_time(split_time)
         print("Formatted split time:", format_split)
         
         split_entry = {
            'time': current_time,
            'split_time': split_time,
            'formatted': format_split,
            'title':title or f"Split {len(self.splits) + 1}"
         }
         
         self.splits.append(split_entry)
         
         print(f"{split_entry['title']} - Time: {format_split}")
         tts(f"{split_entry['title']} recoreded at: {format_split}")
         
      else:
         tts("The stopwatch is not running.")
      #return split_start_time

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

   def get_splits(self):
      #returns the list of split times
      return self.splits

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
