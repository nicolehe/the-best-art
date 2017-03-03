import tracery
from tracery.modifiers import base_english
from generator_test import process_noun_chunks, select_word, pick_file
import os
import json



def get_all_nouns(dir):
    jsons = [file for file in os.listdir(dir) if file.endswith(".json")]
    all_nouns = []
    for j in jsons:
        f = open(dir + j).read()
        data = json.loads(f)
        items = data["data"]
        for item in items:
            all_nouns.append(item.lower())
    return all_nouns

nouns = get_all_nouns("./data/noun_chunks/")
adjs = select_word("./data/corpora/data/words/adjs.json", "adjs")
adverbs = select_word("./data/corpora/data/words/adverbs.json", "adverbs")

rules = {
    'origin': 'Using #noun_chunk#, make something that like a #noun_chunk# #adverb#!',
    'noun_chunk': nouns,
    'adjective' : adjs,
    'adverb' : adverbs

}

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
print grammar.flatten("#origin#")
