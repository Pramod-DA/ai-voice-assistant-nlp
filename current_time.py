import tts
import datetime

def current_time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    return str(time)
    #print("The current time is",time)
    #text = f"the current time is {time}"
    #tts.say(text)