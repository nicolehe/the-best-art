import requests
import sys
import json
import time
from bs4 import BeautifulSoup

search_term = sys.argv[1]

base_url = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=" + str(search_term) + "+&FIELD1=TI&co1=AND&TERM2=&FIELD2=&d=PTXT&p="

titles = []
final_obj = {}

def get_pages(url, page):
    html = requests.get(url + str(page)).text
    soup = BeautifulSoup(html, "html.parser")
    soup.find_all('i')
    string = soup.find_all('i')[1]
    text = string.text
    split = text.split(" ")
    total_entries = int(split[-1].strip())
    pages = total_entries / 50
    return pages


def get_title(url, page):
    html = requests.get(url + str(page)).text
    soup = BeautifulSoup(html, "html.parser")
    trs = soup.find_all('tr')
    for tr in trs:
        contents = tr.contents
        for child in contents:
            if child.name == "td":
                if contents.index(child) == 6:
                    result = child.text
                    result = result.replace("\n", "")
                    result = " ".join(result.split())
                    titles.append(result)
                    print result


def create_json():
    final_obj[search_term] = titles
    final_obj["description"] = "US patents that contain the word " + search_term
    filename = search_term + "_patents.json"

    with open(filename, 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))

    print "************* saved to " + filename + " *************"


total_pages = get_pages(base_url, 1)
print "************* " + str(total_pages) + " pages total *************"

for page in range(1, total_pages):
    get_title(base_url, page)
    time.sleep(0.5)

create_json()
