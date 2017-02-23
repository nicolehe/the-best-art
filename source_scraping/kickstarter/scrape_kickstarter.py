import requests
import sys
import json
import time
from bs4 import BeautifulSoup


base_url = "https://www.kickstarter.com/discover/advanced?woe_id=0&sort=magic&seed=2479523&page="

page = 0
blurbs_list = []
final_obj = {}
total_pages = 50

def get_blurb(url, page):
    html = requests.get(url + str(page)).text
    soup = BeautifulSoup(html, "html.parser")
    blurbs = soup.select('p.project-blurb')
    for blurb in blurbs:
        result = blurb.text
        result = result.replace("\n", "")
        print result
        blurbs_list.append(result.encode("utf-8"))

def create_json():
    final_obj["description"] = "some project blurbs from Kickstarter"
    final_obj["data"] = blurbs_list

    with open("kickstarter_blurbs.json", 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))


for page in range(1, total_pages):
    print "getting page " + str(page)
    get_blurb(base_url, page)
    page += 1
    time.sleep(0.5)

create_json()
