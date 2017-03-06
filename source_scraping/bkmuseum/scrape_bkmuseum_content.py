import requests
import sys
import json
import time
from bs4 import BeautifulSoup

base_url = "https://www.brooklynmuseum.org/opencollection/objects/"
source = open('bkmuseum_artwork_ids_old.json').read()
data = json.loads(source)
final_obj = {}
ids = data["data"]

all_artwork = []

def scrape(art_id):
    artwork = {}

    url = base_url + str(art_id)
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # title
    title = soup.select("h1")
    if title != []:
        artwork["title"] = title[0].text.encode('utf-8').strip()

    # description
    desc = soup.select("div.item-description")
    if desc != []:
        artwork["description"] = desc[0].text.encode('utf-8').strip()

    all_artwork.append(artwork)
    time.sleep(0.3)

def create_json():
    final_obj["description"] = "brookyln museum open collection artwork titles and descriptions between 1917 and 1965"
    final_obj["data"] = all_artwork

    with open("bkmuseum_titles_old_descs7.json", 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))


for art_id in ids[14000:]:
    print str(ids.index(art_id)) + "/" + str(len(ids))
    scrape(art_id)

create_json()
