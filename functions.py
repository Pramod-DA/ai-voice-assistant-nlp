# import tts
# import wiki
# import current_time
# import v2t
# import sqlite3, start
# import os


# def run(do):

#     if 'wikipedia' in do.lower():
#         output = wiki.search(do)
#         return output    

#     if 'current time' in do.lower():
#         time = current_time.current_time()
#         output = "The current time is "+time
#         return output

    

#     if 'sleep' in do.lower():
#         return "sleep" 
    
    
    
            
import asyncio

import tts
import wiki
#import screen_clear
import current_time
import v2t
import sqlite3, start
import os
import os
import logging
import pyttsx3

logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # disabling warnings for gpu requirements
from keras_preprocessing.sequence import pad_sequences
import numpy as np
from keras.models import load_model
from pickle import load
import speech_recognition as sr
import sys

# sys.path.insert(0, os.path.expanduser('~') + "/PycharmProjects/Virtual_Voice_Assistant")
sys.path.insert(0,
                os.path.expanduser('~') + "/Virtual-Voice-Assistant")  # adding voice assistant directory to system path
# importing modules made for assistant
from database import *
from image_generation import generate_image
from gmail import *
from API_functionalities import *
from system_operations import *
from browsing_functionalities import *


def run(do):
    if 'wikipedia' in do.lower():
        output = wiki.search(do)
        return output    

    if 'current time' in do.lower():
        time = current_time.current_time()
        output = "The current time is "+time
        return output


    if 'sleep' in do.lower():
        return "sleep"

model = load_model('Data\\chat_model')
with open('Data\\tokenizer.pickle', 'rb') as handle:
    tokenizer = load(handle)

with open('Data\\label_encoder.pickle', 'rb') as enc:
        lbl_encoder = load(enc)
def chat(text):
    max_len = 20
    while True:
        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([text]),
                                                                          truncating='post', maxlen=max_len), verbose=False)
        print(result)
        intent = lbl_encoder.inverse_transform([np.argmax(result)])[0]
        return intent

def main(query):
        add_data(query)
        intent = chat(query)
        print(query)
        print(intent)
        done = False
        if ("google" in query and "search" in query) or ("google" in query and "how to" in query) or "google" in query:
            googleSearch(query)
            return
        elif ("youtube" in query and "search" in query) or "play" in query or (
                "how to" in query and "youtube" in query):
            youtube(query)
            return
        elif "distance" in query or "map" in query:
            get_map(query)
            return
        if intent == "joke" and "joke" in query:
            joke = asyncio.run(get_joke())
            if joke:
                return joke
        elif intent == "news" and "news" in query:
            news = get_news()
            if news:
                return news
        elif intent == "ip" and "ip" in query:
            ip = asyncio.run( get_ip(_return=True))
            if ip:
                return ip
        elif intent == "movies" and "movies" in query:
            tts.say("Some of the latest popular movies are as follows :")
            get_popular_movies()
            done = True
        elif intent == "tv_series" and "tv series" in query:
            tts.say("Some of the latest popular tv series are as follows :")
            get_popular_tvseries()
            done = True
        elif intent == "weather" and "weather" in query:
            city = re.search(r"(in|of|for) ([a-zA-Z]*)", query)

            if city:
                city = city[2]
                weather = asyncio.run(get_weather(city))
                return weather
            else:
                weather = asyncio.run(get_weather())
                return weather


        elif intent == "internet_speedtest" and "internet" in query:
            tts.say("Getting your internet speed, this may take some time")
            speed = get_speedtest()
            if speed:
                return speed
        elif intent == "system_stats" and "stats" in query:
            stats = system_stats()
            return stats

        elif intent == "system_info" and ("info" in query or "specs" in query or "information" in query):
            info = systemInfo()
            return info
        elif intent == "email" and "email" in query:
            tts.say("Type the receiver id : ")
            receiver_id = input()
            while not check_email(receiver_id):
                tts.say("Invalid email id\nType reciever id again : ")
                receiver_id = input()
            tts.say("Tell the subject of email")
            #subject = record()
            tts.say("tell the body of email")
            #body = record()
            #success = send_email(receiver_id, subject, body)
            #if success:
               # return 'Email sent successfully'
            #else:
                #return "Error occurred while sending email"
            #done = True

        elif intent == "stopwatch":
            pass
        elif intent == "wikipedia" and ("tell" in query or "about" in query):
            description = tell_me_about(query)
            if description:
                return description
            else:
                googleSearch(query)
            done = True
        elif intent == "math":
            answer = get_general_response(query)
            if answer:
                return (answer)
                done = True
        elif intent == "open_website":
            completed = open_specified_website(query)
            if completed:
                done = True
        elif intent == "open_app":
            completed = open_app(query)
            if completed:
                done = True
        elif intent == "note" and "note" in query:
            tts.say("what would you like to take down?")
            #note = record()
            #take_note(note)
            #done = True
        elif intent == "get_data" and "history" in query:
            get_data()
            done = True
        elif intent == "exit" and ("exit" in query or "terminate" in query or "quit" in query):
            exit(0)
        return "Sorry, not able to answer your query"

    
    
    
            
