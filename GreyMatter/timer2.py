import timer
from SenseCells.tts_engine import tts

stopwatch_started = False  # Track if the stopwatch is currently running

while True:
    speech_text = get_user_input()  # Get user input

    if check_message(['start', 'stopwatch']):
        if not stopwatch_started:
            timer.start()  # Start the stopwatch if it's not already running
            stopwatch_started = True
            tts("Let's go.")  # Inform the user that the stopwatch has started
        else:
            tts("The stopwatch is already running.")

    elif check_message(['stop', 'stopwatch']):
        if stopwatch_started:
            total_time = timer.stop()  # Stop the stopwatch and get the total time elapsed
            tts(f"The stopwatch has been stopped and the total time is {total_time} minutes.")
            stopwatch_started = False
        else:
            tts("The stopwatch is not running.")

    elif check_message(['time', 'elapsed', 'stopwatch']):
        if stopwatch_started:
            current_time = timer.elapsed()  # Get the current elapsed time on the stopwatch
            tts(f"The current time elapsed on the stopwatch is {current_time} minutes.")
        else:
            tts("The stopwatch is not running.")

    elif check_message(['exit']):
        if stopwatch_started:
            total_time = timer.stop()  # Stop the stopwatch and get the total time elapsed
            tts(f"The stopwatch has been stopped and the total time is {total_time} minutes.")
        tts("Exiting stopwatch program.")
        break  # Exit the loop and end the program

    else:
        tts("Command not recognized. Please try again.")  # Inform the user of unrecognized commands
