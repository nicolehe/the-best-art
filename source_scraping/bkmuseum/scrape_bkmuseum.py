import requests
import sys
import json
import time
from bs4 import BeautifulSoup



base_url = "https://www.brooklynmuseum.org/opencollection/objects?&limit=30&object_year_begin=1917&object_year_end=1966&offset="

art_ids = set()
final_obj = {}
offset_limit = 15330
offset = 0

def get_urls(url, offset):
    html = requests.get(url + str(offset)).text
    soup = BeautifulSoup(html, "html.parser")
    urls = soup.find_all("a", href=True)
    for a in urls:
        if "opencollection/objects" in a['href'] and "limit" not in a['href']:
            split = a['href'].split('/')
            art_ids.add(split[-1])

def create_json():
    final_obj["description"] = "brookyln museum open collection artwork IDs between 1917 and 1966"
    final_obj["data"] = results

    with open("bkmuseum_artwork_ids_old.json", 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))



while offset < offset_limit:
    print "getting offset " + str(offset)
    get_urls(base_url, offset)
    offset += 30
    time.sleep(0.3)

results = list(art_ids)
create_json()
