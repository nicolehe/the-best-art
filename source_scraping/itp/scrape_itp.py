from selenium import webdriver
import time
import json


driver = webdriver.Firefox()

venue_nums = [48, 31, 8, 4, 131]

urls = []
all_keywords = []
final_obj = {}

def login():
    login_info = open("./login.txt").read()
    login_info = login_info.strip()
    base_url = 'https://' + login_info + '@itp.nyu.edu/projects/thesisProjects.php?list=quick&venue_id='
    driver.get(base_url)
    alert = driver.switch_to_alert()
    alert.accept()

def get_urls(venue):
    time.sleep(0.3)
    year_page = 'https://itp.nyu.edu/projects/thesisProjects.php?list=quick&venue_id=' + str(venue)
    driver.get(year_page)
    links = driver.find_elements_by_css_selector("a")
    for link in links:
        if "project_id" in link.get_attribute('href'):
            urls.append(link.get_attribute('href'))


def get_keywords(url):
    print url
    time.sleep(0.5)
    driver.get(url)
    descriptions = driver.find_elements_by_id("description")
    keywords = descriptions[1].text
    if keywords != "":
        keywords_split = keywords.split(",")
        for word in keywords_split:
            word = word.strip()
            print word
            all_keywords.append(word)

def create_json():
    final_obj["description"] = "itp thesis keywords"
    final_obj["data"] = all_keywords

    with open("itp_thesis_keywords2.json", 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))


login()
for year in venue_nums:
    urls = []
    get_urls(year)
    for page in urls[3:]:
        get_keywords(page)

create_json()

driver.quit()
