import requests
import sys
import json
import time
from bs4 import BeautifulSoup



base_url = "http://www.instructables.com/tag/type-id/?&offset="
results = []
final_obj = {}
total_pages = 500
offset = 0


def get_title(url, offset):
    html = requests.get(url + str(offset)).text
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.select("span.title")
    for title in titles:
        results.append(title.text)

def create_json():
    final_obj["description"] = "titles from instructables"
    final_obj["data"] = results

    with open("instructables_titles.json", 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))



for page in range(1, total_pages):
    print "getting page " + str(page)
    get_title(base_url, offset)
    offset += 59
    time.sleep(0.5)

create_json()
