import random
import os
import json
from textblob import TextBlob, Word

saved_file = open('saved.txt', "a+")

def select_word(path, key):
    source = open(path).read()
    data = json.loads(source)
    return random.choice(data[key])

def pick_file(dir):
    jsons = [file for file in os.listdir(dir) if file.endswith(".json")]
    return random.choice(jsons)


def test1():
    noun_file = pick_file("./data/noun_chunks")
    adj = select_word("./data/corpora/data/words/adjs.json", "adjs").encode('utf-8').strip()
    noun1 =  select_word("./data/noun_chunks/" + noun_file, "data").encode('utf-8').strip()
    verb1 = select_word("./data/corpora/data/words/verbs.json", "verbs")["present"].encode('utf-8').strip()
    adv = select_word("./data/corpora/data/words/adverbs.json", "adverbs").encode('utf-8').strip()
    verb2 = select_word("./data/corpora/data/words/verbs.json", "verbs")["present"].encode('utf-8').strip()
    hashtag = select_word("./data/hashtags/itp_thesis_keywords.json", "data").encode('utf-8').strip().replace(" ", "")
    result = "Human, " + verb1 + " something " + adj + " that will " + verb2 + " the " + noun1.lower() + " " + adv + " #" + hashtag + "\n"
    saved_file.write(result)





for i in range(10000):
    test1()
