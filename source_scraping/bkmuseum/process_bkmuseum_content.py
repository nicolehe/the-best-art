import sys
import json
import time


# file_name = "bkmuseum_titles_descs1.json"
#
# source = open(file_name).read()
# raw = json.loads(source)
# data = raw["data"]
#
#
# def get_descs():
#     descs = [artwork['description'].replace("\r\n", "") + '\n\n' for artwork in data if 'description' in artwork]
#     return " ".join(descs)
#
# results = get_descs().encode('utf-8')

f = open("descriptions.txt", 'a+')


for i in range(0, 10):
    print i
    file_name = "bkmuseum_titles_descs" + str(i) + ".json"
    source = open(file_name).read()
    raw = json.loads(source)
    data = raw["data"]

    descs = [artwork['description'].replace("\r", "").replace("\n","").strip() + '\n' for artwork in data if 'description' in artwork]
    joined = " ".join(descs)

    results = joined.encode('utf-8')

    f.write(results)
