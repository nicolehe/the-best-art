import tracery
from tracery.modifiers import base_english
from modules import get_headline_chunks, create_index, process_noun_chunks, select_word, pick_file, get_words, get_all_nouns, get_weather, get_horoscope, get_date
import os
import json
import random
from textblob import TextBlob
from datetime import datetime

from spacy.en import English
parser = English()

art_nouns = get_all_nouns("./data/noun_chunks/")
technical_nouns = get_all_nouns("./data/hashtags/")
adjs = get_words("./data/corpora/data/words/adjs.json", "adjs")
adverbs = get_words("./data/corpora/data/words/adverbs.json", "adverbs")
moods = get_words("./data/corpora/data/humans/moods.json", "moods")
verbs_data = get_words("./data/corpora/data/words/verbs.json", "verbs")
simple_objects = get_all_nouns("./data/simple_objects/")
verbs_present = [item["present"] for item in verbs_data]

# headlines = get_headline_chunks()
# weather_rating, weather_status = get_weather()
# horoscope_rating, picked_sentence = get_horoscope()
# time_of_day, day, date = get_date()

def generate_projects():
    projects = {
        'project': [
            '#make# #simple_object# #about# #art_noun#.',
            '#make# #art_noun# #about# #simple_object#.',
            "#combine# #art_noun# and #simple_object# to #verb# #adverb#.",
            '#make# #technical_noun# that feels #mood#.',
            '#using# #any_noun#, #make# something that #verb.s#.',
            '#using# #any_noun# and #technical_noun#, #make# something #adjective#.',
            '#adverb# #combine# #any_noun# and #any_noun#.',
            '#make# art out of #simple_object# and #technical_noun#.',
            '#make# #any_noun# feel #mood#.',
            '#make# #any_noun# #about# #art_noun#.'
            # '#using# #headline#, #make# something #adjective#.',
            # 'make #headline# feel #mood#.',
            # '#make# #any_noun# #about# #headline#.'
        ],
        'art_noun': art_nouns,
        'any_noun': ['#simple_object#', '#technical_noun#', '#art_noun#'],
        'about': ['that evokes', 'about', 'that reminds me of', 'in response to', 'in contrast to', 'in opposition to'],
        'make': ['make', 'construct', 'produce', 'create', 'build', 'design'],
        'using': ['using', 'incorporating', 'with'],
        'combine': ['blend', 'merge', 'combine', 'conjoin'],
        'simple_object': simple_objects,
        # 'headline': headlines,
        'technical_noun': technical_nouns,
        'verb': verbs_present,
        'adjective': adjs,
        'mood': moods,
        'adverb': adverbs


    }

    generated_projects = []

    grammar = tracery.Grammar(projects)
    grammar.add_modifiers(base_english)
    for i in range(1000):
        sentence = grammar.flatten("#project#")
        generated_projects.append(sentence)

    return generated_projects

# def sort_projects(projects_list, todays_rating):
#     tupped = []
#     for r in projects_list:
#         blob = TextBlob(r)
#         tup = (r, blob.sentiment.polarity)
#         tupped.append(tup)
#     final_proj = min(tupped, key=lambda x: abs(float(x[1]) - float(todays_rating)))[0]
#     proj_rating_raw = min(tupped, key=lambda x: abs(float(x[1]) - float(todays_rating)))[1]
#     proj_rating = str(proj_rating_raw)
#     return final_proj, proj_rating
#
#
#
# def generate_assignment():
#     convo = {
#         'greeting' : [
#             "#date_now# \nGood #time#, human, #phrase#. \nToday's Art Index is #todays_rating_num# and I have calculated the best art for this moment in time. This project has an Art Index of #project_rating_num#. \n#execute.capitalize# the following: \n#proj.capitalize#"
#                 ],
#         'day' : day,
#         'execute' : ['execute', 'implement'],
#         'date_now' : date,
#         'proj' : final_proj,
#         'time': time_of_day,
#         'weather_status' : weather_status,
#         'todays_rating_num' : todays_rating,
#         'project_rating_num' : proj_rating,
#         'day_now' : day,
#         'horo' : picked_sentence.lower(),
#         'phrase' : ['#weather_status# #day#', '#horo#']
#     }
#
#     convo_grammar = tracery.Grammar(convo)
#     convo_grammar.add_modifiers(base_english)
#     res = convo_grammar.flatten("#greeting#")
#
#
#     return res
#
#
# todays_rating = create_index()
#
# projects_list = generate_projects()
# final_proj, proj_rating = sort_projects(projects_list, todays_rating)
# assignment = generate_assignment()
# print assignment
