from GreyMatter.SenseCells.tts_engine import tts

def go_to_sleep():
    tts("Goodbye! Have a great rest of your day.")
    time.sleep(5)
    quit()
