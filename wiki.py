import tts
import wikipedia
def search(query):
    query = query.lower()
    query.replace("wikipedia"," ")
    try:
        result = wikipedia.summary(query, sentences=3)
        return result
#        tts.say(result)
    except:
        return "No results found, try again"