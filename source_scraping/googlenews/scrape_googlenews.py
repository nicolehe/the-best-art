import requests
import sys
import json
import time
from bs4 import BeautifulSoup

base_url = "https://news.google.com/"

titles = []
final_obj = {}


def get_title(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    headlines = soup.select("span.titletext")
    for headline in headlines:
        titles.append(headline.text)




get_title(base_url)
