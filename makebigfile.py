from tracery_test import generate_projects
import tracery
from tracery.modifiers import base_english
from modules import get_headline_chunks, create_index, process_noun_chunks, select_word, pick_file, get_words, get_all_nouns, get_weather, get_horoscope, get_date
import os
import json
import random
from textblob import TextBlob
from datetime import datetime

saved_file = open('3-5-17.txt', "a+")

projects_list = generate_projects()

for i in range(50):
    for p in projects_list:
        p = p + "\n"
        saved_file.write(p.encode('utf-8'))
