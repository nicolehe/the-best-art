import tracery
from tracery.modifiers import base_english
from modules import get_headline_chunks, create_index, process_noun_chunks, select_word, pick_file, get_words, get_all_nouns, get_weather, get_horoscope, get_date
import os
import json
import sys
import time
import random
from textblob import TextBlob
from datetime import datetime
import socket

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


def generate_projects():
    headlines = get_headline_chunks()
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
            'make #any_noun# feel #mood#.',
            '#make# #any_noun# #about# #art_noun#.',
            '#using# #headline#, #make# something #adjective#.',
            'make #headline# feel #mood#.',
            '#make# #any_noun# #about# #headline#.'
        ],
        'art_noun': art_nouns,
        'any_noun': ['#simple_object#', '#technical_noun#', '#art_noun#'],
        'about': ['that evokes', 'about', 'that reminds me of', 'in response to', 'in contrast to', 'in opposition to'],
        'make': ['make', 'construct', 'produce', 'create', 'build', 'design'],
        'using': ['using', 'incorporating', 'with'],
        'combine': ['blend', 'merge', 'combine', 'conjoin'],
        'simple_object': simple_objects,
        'headline': headlines,
        'technical_noun': technical_nouns,
        'verb': verbs_present,
        'adjective': adjs,
        'mood': moods,
        'adverb': adverbs,


    }

    generated_projects = []

    grammar = tracery.Grammar(projects)
    grammar.add_modifiers(base_english)
    for i in range(1000):
        sentence = grammar.flatten("#project#")
        generated_projects.append(sentence)

    return generated_projects


def sort_projects(projects_list, todays_rating):
    tupped = []
    for r in projects_list:
        blob = TextBlob(r)
        tup = (r, blob.sentiment.polarity)
        tupped.append(tup)
    final_proj = min(tupped, key=lambda x: abs(
        float(x[1]) - float(todays_rating)))[0]
    proj_rating_raw = min(tupped, key=lambda x: abs(
        float(x[1]) - float(todays_rating)))[1]
    proj_rating = str(proj_rating_raw)
    return final_proj, proj_rating


def generate_message(border):
    timestamp = int(time.time())
    weather_rating, weather_desc, horoscope_rating, picked_sentence, tweets, ISS_closeness, todays_rating = create_index()
    time_of_day, day, date = get_date()
    projects_list = generate_projects()
    final_proj, proj_rating = sort_projects(projects_list, todays_rating)
    convo = {
        'greeting': [
            "#date_now##border#Good #time#, human, #phrase##border##art_index##border##execute.capitalize# the following:#border##title#: #proj.capitalize##border#"
        ],
        'art_index': [
            "Given the current Art Index of #todays_rating_num#, I have #calculated# the best art for #moment#, with a rating of #project_rating_num#.",
            "#variable# has #impacted# the current Art Index, totalling #todays_rating_num#. I have #calculated# the best art for #moment#, with a rating of #project_rating_num#.",
            "I have #calculated# the best art for #moment#. Today's Art Index is #todays_rating_num#, and this project has a very close rating of #project_rating_num#.",

        ],
        'math': ["\nWeather: #weather_rating#\nHoroscope: #horoscope_rating#\nTrump Rating: #trump_rating#\nHow Close the ISS Is: #ISS_rating#"],
        'calculated': ['computed', 'calculated', 'determined'],
        'impacted' : ['impacted', 'affected'],
        'moment': ['this moment in time', 'the current state of the world'],
        'day': day,
        'variable' : [
            "The current Trump Tweet rating of #trump_rating#",
            "The current proximity of the International Space Station is (rating #ISS_rating#)",
            "My current horoscope, which I have rated #horoscope_rating#,"
        ],
        'title' : str(timestamp),
        'border': [border],
        'execute': ['execute', 'implement'],
        'date_now': date,
        'proj': final_proj,
        'time': time_of_day,
        'weather_status': weather_desc,
        'weather_rating': float(weather_rating),
        'horoscope_rating': horoscope_rating,
        'trump_rating': tweets,
        'ISS_rating': ISS_closeness,
        'todays_rating_num': todays_rating,
        'project_rating_num': proj_rating,
        'day_now': day,
        'horo': picked_sentence.lower(),
        'phrase': ['#weather_status# #day#.', '#horo#']
    }

    convo_grammar = tracery.Grammar(convo)
    convo_grammar.add_modifiers(base_english)
    message = convo_grammar.flatten("#greeting#")

    return message




if __name__ == "__main__":
    open("to_print.txt", 'w').close()
    for i in range(int(sys.argv[1])):
        message = generate_message("$$$$")
        print message.replace("$$$$", "\n\n")
        with open("to_print.txt", "a") as f:
            f.write(message)
            f.write("***")
            print "***"
