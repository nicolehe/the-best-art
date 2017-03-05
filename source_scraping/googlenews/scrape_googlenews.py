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


def create_json():
    final_obj["data"] = titles
    final_obj["description"] = "US patents that contain the word " + search_term
    filename = "./data/" + search_term + "_patents.json"

    with open(filename, 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))

get_title(base_url)
