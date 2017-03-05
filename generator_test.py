import random
import os
import json
from textblob import TextBlob, Word

saved_file = open('test2.txt', "a+")

def select_word(path, key):
    source = open(path).read()
    data = json.loads(source)
    choice = random.choice(data[key])
    if isinstance(choice, basestring):
        return choice.encode('utf-8').strip()
    else:
        return choice

def get_words(path, key):
    source = open(path).read()
    data = json.loads(source)
    words = data[key]
    return words

def pick_file(dir):
    jsons = [file for file in os.listdir(dir) if file.endswith(".json")]
    return random.choice(jsons)


dont_add_a = ['phys', 'your', 'data', 'choc']
# FIXME: jesus
def process_noun_chunks(chunk):
    if chunk[-1] != "s" or chunk[-2:] == "us" or chunk[-2:] == "as" or chunk[-2:] == "is" or chunk[-2:] == "os":
        if chunk[0].lower() in ["a", "e", "i", "o", "u"] and chunk[1] not in [" ", "n"] and chunk[:3] not in ["our"]:
            chunk = "an " + chunk
        elif chunk[:2] == "a " or chunk[:2] == "an" or chunk[:4] == "the " or chunk[:4] in dont_add_a:
            chunk = chunk
        else:
            chunk = "a " + chunk
    elif chunk[-2:] == "ss":
        chunk = chunk
    return chunk.replace("|","").replace("\n", "").strip()



def test1():
    noun_file = pick_file("./data/noun_chunks")
    adj = select_word("./data/corpora/data/words/adjs.json", "adjs")
    noun_chunk =  select_word("./data/noun_chunks/" + noun_file, "data").lower()
    noun = process_noun_chunks(noun_chunk)
    verb1 = select_word("./data/corpora/data/words/verbs.json", "verbs")["present"].encode('utf-8').strip()
    adv = select_word("./data/corpora/data/words/adverbs.json", "adverbs")
    verb2 = select_word("./data/corpora/data/words/verbs.json", "verbs")["present"].encode('utf-8').strip()
    hashtag = select_word("./data/hashtags/itp_thesis_keywords.json", "data").replace(" ", "")

    result = "Human, " + verb1 + " something " + adj + " that will " + adv + " " + verb2 + " "+ noun +  " #" + hashtag + "\n"
    # saved_file.write(result)
    return result

def test2():
    noun_file = pick_file("./data/noun_chunks")
    noun_chunk =  select_word("./data/noun_chunks/" + noun_file, "data").lower()
    noun = process_noun_chunks(noun_chunk)
    adj = select_word("./data/corpora/data/words/adjs.json", "adjs")
    mood = select_word("./data/corpora/data/humans/moods.json", "moods")
    hashtag = select_word("./data/hashtags/itp_thesis_keywords.json", "data").replace(" ", "")


    result = "Human, construct " + noun + " that makes me feel " + mood + ". " + " #" + hashtag + "\n"

    # saved_file.write(result)
    return result


# for i in range(5):
#     print test1()
#
# for i in range(5):
#     print test2()
