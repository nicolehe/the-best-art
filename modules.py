import requests
import sys
import json
import os
import time
from operator import itemgetter
from bs4 import BeautifulSoup
import pyowm
from textblob import TextBlob

import spacy
nlp = spacy.load('en')

current_headlines = []
final_obj = {}


def get_weather():
    owm = pyowm.OWM('e5bbd595ccad62117e1da86f24394b2c')
    observation = owm.weather_at_place('New York, NY')
    w = observation.get_weather()

    temp = w.get_temperature('fahrenheit')['temp']
    rain = w.get_rain()
    snow = w.get_snow()

    if temp <= 33 or temp >= 90:
        weather_rating = -0.5
    elif temp > 33 and temp <= 45 or temp < 90 and temp >= 80:
        weather_rating = -0.25
    elif temp > 45 and temp <= 55:
        weather_rating = 0
    elif temp > 55 and temp <= 65:
        weather_rating = 0.25
    elif temp > 65 and temp <= 80:
        weather_rating = 0.5

    if not rain or not snow:
        weather_rating = weather_rating
    else:
        weather_rating = weather_rating - 0.25

    status = w.get_detailed_status()
    return weather_rating, status




def get_horoscope():
    html = requests.get("http://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=3").text
    time.sleep(1)
    soup = BeautifulSoup(html, "html.parser")
    div = soup.select("div.horoscope-content")
    raw = div[0].text
    split = raw.split("-")
    horoscope = split[1][1:].strip()
    blob = TextBlob(horoscope)
    horoscope_rating = blob.sentiment.polarity
    return horoscope_rating

def count_trump_tweets():
    date = time.strftime("%Y-%m-%d")
    url = "https://twitter.com/search?l=&q=from%3Arealdonaldtrump%20since%3A"+ str(date)
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    tweets = soup.select("div.tweet.js-stream-tweet")

    if not tweets:
        tweet_num = 0
    else:
        tweet_num = len(tweets)

    if tweet_num >= 8:
        trump_tweet_rating = -0.5
    elif tweet_num < 8 and tweet_num >= 4:
        trump_tweet_rating = -0.25
    elif tweet_num < 4 and tweet_num >= 1:
        trump_tweet_rating = 0
    elif tweet_num == 0:
        trump_tweet_rating = 0.5
    return trump_tweet_rating

def get_all_nouns(dir):
    jsons = [file for file in os.listdir(dir) if file.endswith(".json")]
    unprocessed_nouns = []

    for j in jsons:
        f = open(dir + j).read()
        data = json.loads(f)
        items = data["data"]
        for item in items:
            unprocessed_nouns.append(item.lower())
    processed_nouns = [process_noun_chunks(noun).strip() for noun in unprocessed_nouns]
    return processed_nouns


def select_word(path, key):
    source = open(path).read()
    data = json.loads(source)
    choice = random.choice(data[key])
    if isinstance(choice, basestring):
        return choice.encode('utf-8').strip()
    else:
        return choice

def get_words(path, key):
    source = open(path).read()
    data = json.loads(source)
    words = data[key]
    return words

def pick_file(dir):
    jsons = [file for file in os.listdir(dir) if file.endswith(".json")]
    return random.choice(jsons)


# FIXME: jesus
def process_noun_chunks(chunk):
    dont_add_a = ['phys', 'your', 'data', 'choc']
    if chunk[-1] != "s" or chunk[-2:] == "us" or chunk[-2:] == "as" or chunk[-2:] == "is" or chunk[-2:] == "os":
        if chunk[0].lower() in ["a", "e", "i", "o", "u"] and chunk[1] not in [" ", "n"] and chunk[:3] not in ["our"]:
            chunk = "an " + chunk
        elif chunk[:2] == "a " or chunk[:2] == "an" or chunk[:4] == "the " or chunk[:4] in dont_add_a:
            chunk = chunk
        else:
            chunk = "a " + chunk
    elif chunk[-2:] == "ss":
        chunk = chunk
    return chunk.replace("|","").replace("\n", "").strip()


def get_headline_chunks():
    current_headlines = []
    nouns = []
    html = requests.get('https://news.google.com/').text
    soup = BeautifulSoup(html, "html.parser")
    headlines = soup.select("span.titletext")
    for headline in headlines:
        current_headlines.append(headline.text)
    docs = [ nlp(d) for d in current_headlines ]
    for doc in docs:
        for chunk in doc.noun_chunks:
            if len(chunk) > 0:
                # print chunk
                nouns.append(chunk.text)
    return nouns

def create_index():
    weather_num, weather_desc = get_weather()
    horo = get_horoscope()
    tweets = count_trump_tweets()
    return {
        "weather" : weather_num,
        "horoscope" : horo,
        "trump_tweets" : tweets
    }
# get_headline_chunks()
