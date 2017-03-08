import requests
import random
import sys
import json
import os
import time
from operator import itemgetter
from bs4 import BeautifulSoup
import pyowm
from textblob import TextBlob
from datetime import datetime
from geopy.distance import vincenty

import spacy
nlp = spacy.load('en')

def map_val(x, in_min, in_max, out_min, out_max):
    return float((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def get_ISS():
    api = requests.get("http://api.open-notify.org/iss-now.json")
    data = api.json()
    iss = (data["iss_position"]["latitude"], data["iss_position"]["longitude"])
    home = (40.674974, -73.957325)
    dist = vincenty(iss, home).miles
    ISS_closeness = map_val(dist, 0.0, 12450.0, -1.0, 1.0)
    return -1.0 * ISS_closeness





def get_weather():
    owm = pyowm.OWM('e5bbd595ccad62117e1da86f24394b2c')
    observation = owm.weather_at_place('New York, NY')
    w = observation.get_weather()

    temp = w.get_temperature('fahrenheit')['temp']
    rain = w.get_rain()
    snow = w.get_snow()

    if temp <= 33 or temp >= 90:
        weather_rating = -0.6
    elif temp > 33 and temp <= 45 or temp < 90 and temp >= 80:
        weather_rating = -0.3
    elif temp > 45 and temp <= 55:
        weather_rating = 0
    elif temp > 55 and temp <= 65:
        weather_rating = 0.3
    elif temp > 65 and temp <= 80:
        weather_rating = 0.6

    if not rain or not snow:
        weather_rating = weather_rating
    else:
        weather_rating = weather_rating - 0.25

    status = w.get_detailed_status()
    return weather_rating, status

def get_date():
    currentTime = datetime.now()
    date = currentTime.strftime('%I:%M %p, %B %d, %Y')
    if 4 <= currentTime.hour < 12:
        time_of_day = "morning"
        day = "today"
    elif 12 <= currentTime.hour < 18:
        time_of_day = "afternoon"
        day = "today"
    else:
        time_of_day = "evening"
        day = "tonight"
    return time_of_day, day, date



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

    sentences = [sentence.replace("your", "my").replace("Gemini", "human") for sentence in blob.sentences if "you " not in sentence.lower()]

    picked_sentence = str(random.choice(sentences))

    return horoscope_rating, picked_sentence


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
        trump_tweet_rating = 0.0
    elif tweet_num == 0:
        trump_tweet_rating = 0.6
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
    total_index = 0.0
    ISS_closeness = get_ISS()
    weather_rating, weather_desc = get_weather()
    horoscope_rating, picked_sentence = get_horoscope()
    tweets = count_trump_tweets()
    todays_rating = (weather_rating + horoscope_rating + tweets + ISS_closeness) / 4
    return str(weather_rating), str(weather_desc), str(horoscope_rating), str(picked_sentence), str(tweets), str(ISS_closeness), str(todays_rating)
