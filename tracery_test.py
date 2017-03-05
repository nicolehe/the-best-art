import tracery
from operator import itemgetter
from tracery.modifiers import base_english
from generator_test import process_noun_chunks, select_word, pick_file, get_words
import os
import json
from textblob import TextBlob



def get_all_nouns(dir):
    jsons = [file for file in os.listdir(dir) if file.endswith(".json")]
    unprocessed_nouns = []

    for j in jsons:
        f = open(dir + j).read()
        data = json.loads(f)
        items = data["data"]
        for item in items:
            unprocessed_nouns.append(item.lower())
    processed_nouns = [process_noun_chunks(noun) for noun in unprocessed_nouns]
    return processed_nouns



nouns = get_all_nouns("./data/noun_chunks/")
technical_nouns = get_all_nouns("./data/hashtags/")
adjs = get_words("./data/corpora/data/words/adjs.json", "adjs")
adverbs = get_words("./data/corpora/data/words/adverbs.json", "adverbs")
moods = get_words("./data/corpora/data/humans/moods.json", "moods")
verbs_data = get_words("./data/corpora/data/words/verbs.json", "verbs")
simple_objects = get_all_nouns("./data/simple_objects/")

verbs_present = [item["present"] for item in verbs_data]

rules = {
    # 'project': ['Using #noun_chunk#, make something that #verb.s# like #noun_chunk#.',
    #             'Make #noun_chunk# that makes me feel #mood#.',
    #             'With #noun_chunk# and #technical_noun#, construct something #adjective#.'],
    'project': ['Create #simple_object#, evoking #noun_chunk#.'],
    'noun_chunk': nouns,
    'simple_object': simple_objects,
    'technical_noun' : technical_nouns,
    'verb': verbs_present,
    'adjective' : adjs,
    'mood': moods,
    'adverb' : adverbs

}

results = []

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
for i in range(50):
    sentence = grammar.flatten("#project#")
    results.append(sentence)

tupped = []
for r in results:
    blob = TextBlob(r)
    tup = (blob.sentiment.polarity, r)
    tupped.append(tup)

sorted_list = sorted(tupped, key=itemgetter(0))
for item in sorted_list:
    print item[1], item[0]
