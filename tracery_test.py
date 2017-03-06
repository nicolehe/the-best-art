import tracery
from tracery.modifiers import base_english
from modules import get_headline_chunks, create_index, process_noun_chunks, select_word, pick_file, get_words, get_all_nouns, get_weather
import os, json
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
headlines = get_headline_chunks()

# print todays_sentiment
# if todays_sentiment <= -0.5:
#     print "Very bad today."
# elif todays_sentiment > -0.5 and todays_sentiment <= -0.25:
#     print "Pretty bad today."
# elif todays_sentiment > -0.25 and todays_sentiment <=0:
#     print "Slightly bad today."
# elif todays_sentiment > 0 and todays_sentiment <= 0.25:
#     print "Okay today."
# elif todays_sentiment > 0.25 and todays_sentiment <= 0.5:
#     print "Pretty good today."
# else:
#     print "Great!"



rules = {
    'project': [
                '#make# #simple_object# #about# #art_noun#.',
                '#make# #art_noun# #about# #simple_object#.',
                "#combine# #art_noun# and #simple_object# to #verb# #adverb#.",
                '#make# #technical_noun# that feels #mood#.',
                '#using# #any_noun#, #make# something that #verb.s#.',
                '#using# #any_noun# and #technical_noun#, #make# something #adjective#.',
                '#adverb# #combine# #any_noun# and #any_noun#.',
                '#make# art out of #simple_object# and #technical_noun#.',
                '#using# #headline#, #make# something #adjective#.',
                'make #headline# feel #mood#.',
                '#make# #any_noun# #about# #headline#.'
                ],
    'art_noun': art_nouns,
    'any_noun' : ['#simple_object#', '#technical_noun#', '#art_noun#'],
    'about' : ['that evokes', 'about', 'that reminds me of', 'in response to', 'in contrast to', 'in opposition to'],
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
    results.append(sentence.upper())

tupped = []
for r in results:
    blob = TextBlob(r)
    tup = (r, blob.sentiment.polarity)
    tupped.append(tup)

weather_rating, weather_status = get_weather()
index = create_index()
tot = 0
for key in index:
    tot += index[key]
avg = tot/len(index)
# print avg

final_proj = min(tupped,key=lambda x: abs(float(x[1]) - avg))[0]

currentTime = datetime.now()
date = currentTime.strftime('%I:%M %p, %B %d, %Y')
if currentTime.hour < 12:
    time_of_day = "morning"
    day = "today"
elif 12 <= currentTime.hour < 18:
    time_of_day = "afternoon"
    day = "today"
else:
    time_of_day = "evening"
    day = "tonight"

print date.upper()
print "GOOD " + time_of_day.upper() + " HUMAN, " + weather_status.upper() + " " + day.upper() + "."
print "I HAVE CALCULATED THE BEST ART FOR THIS MOMENT. EXECUTE THE FOLLOWING:"
print final_proj
