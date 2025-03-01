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
          tts("The stopwatch is already running")
          raise RuntimeError("Stopwatch is already running.")
          
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
      print("Type of elapsed_time", type(elapsed_time))
      self.total_time += elapsed_time #accumulate total time

      formatted_elapsed_time = self.format_time(elapsed_time)

      message = f"The stopwatch has been stopped.  Total time: {formatted_elapsed_time}."

      if self.splits:
         split_messages = []
         for index, split in enumerate(self.splits, 1):
            formatted_split = split['formatted']
            split_messages.append(f"Split{index}: {formatted_split}")
         message +=" " + " ".join(split_messages)
            
      print(f"[DEBUG] Final message from stopwatch.stop(): {message}")
      tts(message)

      return elapsed_time.total_seconds()
      
   def reset(self):
      """Resets the stopwatch to zero time """
      print("Resetting the stopwatch")
      print("Current total time before reset:", self.total_time)
      self.start_time = None
      self.total_time = datetime.timedelta(0)
      self.is_running = False #stop the stopwatch
      self.splits = []
      print("Total time after reset:", self.total_time)

   def elapsed(self, start_time=None):
      """Time elapsed since start was called"""
      if self.start_time is None:
         tts("The stopwatch has not started")
         raise RuntimeError("The stopwatch has not started")
         
      if self.is_running:
         time_elapsed = (datetime.datetime.now() - self.start_time)
      else:
         time_elapsed = self.total_time
      time_string = self.format_time(time_elapsed)
      return time_elapsed, time_string

   def split(self, title=None):
      if not self.is_running:
         tts("The stopwatch is not running.")
         return
         
      if len(self.splits) >=5:
          tts("Maximum of 5 splits reached.")
          print("Maximum of 5 splits reached.")
          return
      current_time = datetime.datetime.now()
      
      if self.splits:
         last_split_time = self.splits[-1]['time']
         split_time = current_time - last_split_time #time since the last split
      else:
         split_time = current_time - self.start_time #time since stopwatch started
            
      formatted_split = self.format_time(split_time)
                  
      split_entry = {
          'time': current_time,
          'split_time': split_time,
          'formatted': formatted_split,
          'title':title or f"Split {len(self.splits) + 1}"
      }

      self.splits.append(split_entry)
      
      print(f"[DEBUG] Split {len(self.splits)} recorded at {formatted_split}")
      print(f"[DEBUG] All splits so far: {self.splits}")
      tts(f"{split_entry['title']} recorded at {formatted_split}")
      
   def unsplit(self):
      """Stops a split. Returns the time elapsed since split was called"""
      if self.is_running:
         tts("The stopwatch is running. Stop it first.")
      elif not self.splits:
         tts("No splits recorded.")
      else:
         split_time = self.splits.pop() #remove the last split time from the list
         time_string = split_time['formatted']
         tts(f"Split stopped.  Time elapsed since the split started is {time_string}.")

   def stop_split(self, split_index):
      if 0 <= split_index < len(self.splits):
         split_time = self.splits.pop(split_index)
         return split_time['split_time']
      else:
         raise IndexError("Invalid split index")

   def get_splits(self):
      #returns the list of split times
      return self.splits

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
