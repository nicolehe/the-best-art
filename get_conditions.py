import requests
import sys
import json
# import spacy
import time
from operator import itemgetter
from bs4 import BeautifulSoup
from textblob import TextBlob

# nlp = spacy.load('en')

current_headlines = []
final_obj = {}


def get_headlines(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    headlines = soup.select("span.titletext")
    for headline in headlines:
        current_headlines.append(headline.text)

def get_horoscope(url):
    html = requests.get(url).text
    time.sleep(1)
    soup = BeautifulSoup(html, "html.parser")
    div = soup.select("div.horoscope-content")
    raw = div[0].text
    split = raw.split("-")
    horoscope = split[1][1:].strip()
    blob = TextBlob(horoscope)
    sentiment = blob.sentiment.polarity
    return sentiment



get_horoscope("http://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=11")
# get_headlines("https://news.google.com/")
#
#
#
# docs = [ nlp(d) for d in current_headlines ]
#
# def get_headline_chunks():
#     nouns = []
#     for doc in docs:
#         for chunk in doc.noun_chunks:
#             if len(chunk) > 0:
#                 # print chunk
#                 nouns.append(chunk.text)
#     return nouns
# # get_headline_chunks()
