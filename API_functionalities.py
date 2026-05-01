import asyncio
import os
import datetime

import aiohttp
from dotenv import load_dotenv
from newsapi import NewsApiClient
import re
import requests
from wolframalpha import Client

load_dotenv(dotenv_path='Data\\.env')

NEWS = os.getenv('NEWS_API')
WOLFRAMALPHA = os.getenv('WOLFRAMALPHA_API')
OPENWEATHERMAP = os.getenv('OPENWEATHERMAP_API')
TMDB = os.getenv('TMDB_API')
news = NewsApiClient(api_key=NEWS)


async def get_ip(_return=False):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://ip-api.com/json/') as response:
                data = await response.json()
                if _return:
                    return data
                else:
                    return f'Your IP address is {data["query"]}'
    except asyncio.CancelledError:
        return None
    except aiohttp.ClientError:
        return None
async def get_joke():
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get('https://v2.jokeapi.dev/joke/Any?format=txt')
            joke = await response.text()
            return joke
    except asyncio.CancelledError:
        return None
    except aiohttp.ClientError:
        return None
    except KeyboardInterrupt:
        return None

def get_news():
    try:
        top_news = ""
        top_headlines = news.get_top_headlines(language="en", country="in")
        for i in range(10):
             top_news += re.sub(r'[|-] [A-Za-z0-9 |:.]*', '', top_headlines['articles'][i]['title']).replace("’", "'") + '\n'
        return top_news
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None




async def get_weather(city=''):
    try:
        async with aiohttp.ClientSession() as session:
            if city:
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP}&units=metric'
            else:
                ip_info = await get_ip(_return=True)
                city = ip_info.get('city', 'London')  # Default to 'London' if city not available
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP}&units=metric'

            async with session.get(url) as response:
                data = await response.json()
                print(data)
                weather = (f'It\'s {data["main"]["temp"]}° Celsius and {data["weather"][0]["main"]}\n'
                           f'But feels like {data["main"]["feels_like"]}° Celsius\n'
                           f'Wind is blowing at {round(data["wind"]["speed"] * 3.6, 2)}km/h\n'
                           f'Visibility is {int(data["visibility"] / 1000)}km')

                return weather

    except aiohttp.ClientError:
        return None
    except asyncio.CancelledError:
        return None
    except KeyboardInterrupt:
        return None
def get_general_response(query):
    client = Client(app_id=WOLFRAMALPHA)
    try:
        response = client.query(query)
        return next(response.results).text
    except (StopIteration, AttributeError) as e:
        return None
    except KeyboardInterrupt:
        return None

def get_popular_movies():
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB}&region=IN&sort_by=popularity.desc&"
                                f"primary_release_year={datetime.date.today().year}").json()
    except requests.exceptions.RequestException:
        return None
    try:
        print()
        for movie in response["results"]:
            title = movie['title']
            print(title)
    except KeyError:
        return None

def get_popular_tvseries():
    try:
        response = requests.get(f"https://api.themoviedb.org/3/tv/popular?api_key={TMDB}&region=IN&sort_by=popularity.desc&"
                                f"primary_release_year={datetime.date.today().year}").json()
    except requests.exceptions.RequestException:
        return None
    try:
        print()
        for show in response["results"]:
            title = show['name']
            print(title)
    except KeyError:
        return None