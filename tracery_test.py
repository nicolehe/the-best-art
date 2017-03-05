import tracery
from operator import itemgetter
from tracery.modifiers import base_english
from generator_test import process_noun_chunks, select_word, pick_file, get_words
from get_conditions import get_headline_chunks
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
    processed_nouns = [process_noun_chunks(noun).strip() for noun in unprocessed_nouns]
    return processed_nouns



art_nouns = get_all_nouns("./data/noun_chunks/")
technical_nouns = get_all_nouns("./data/hashtags/")
adjs = get_words("./data/corpora/data/words/adjs.json", "adjs")
adverbs = get_words("./data/corpora/data/words/adverbs.json", "adverbs")
moods = get_words("./data/corpora/data/humans/moods.json", "moods")
verbs_data = get_words("./data/corpora/data/words/verbs.json", "verbs")
simple_objects = get_all_nouns("./data/simple_objects/")

verbs_present = [item["present"] for item in verbs_data]
headlines = get_headline_chunks()


rules = {
    # 'project': ['#make# #simple_object# #evoking# #any_noun#.',
    #             '#make# #art_noun# #evoking# #simple_object#.',
    #             "#combine# #art_noun# and #simple_object# to #verb# #adverb#.",
    #             '#make# #technical_noun# that feels #mood#.',
    #             '#using# #any_noun#, #make# something that #verb.s#.',
    #             '#using# #any_noun# and #technical_noun#, #make# something #adjective#.',
    #             '#adverb# #combine# #any_noun# and #any_noun#.',
    #             '#make# art out of #simple_object# and #technical_noun#.'],
    'project' : ['#make# #any_noun# #evoking# #headline#.'],
    'art_noun': art_nouns,
    'any_noun' : ['#simple_object#', '#technical_noun#', '#art_noun#'],
    'evoking' : ['that evokes', 'that reminds me of', 'in contrast to', 'in opposition to'],
    'make': ['make', 'construct', 'produce', 'create', 'build', 'design'],
    'using': ['using', 'incorporating', 'with'],
    'combine': ['blend', 'merge', 'combine', 'conjoin'],
    'simple_object': simple_objects,
    'headline': headlines,
    'technical_noun' : technical_nouns,
    'verb': verbs_present,
    'adjective' : adjs,
    'mood': moods,
    'adverb' : adverbs

}

results = []

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
for i in range(500):
    sentence = grammar.flatten("#project#")
    results.append("HUMAN, " + sentence.upper())

tupped = []
for r in results:
    blob = TextBlob(r)
    tup = (blob.sentiment.polarity, r)
    tupped.append(tup)

sorted_list = sorted(tupped, key=itemgetter(0))
for item in sorted_list:
    print item[1], item[0]
