import spacy
import json

nlp = spacy.load('en')

data = json.loads(open('./kickstarter/kickstarter_blurbs.json').read())

blurbs = data["data"]

docs = [ nlp(d) for d in blurbs ]

nouns = []
final_obj = {}

# TODO: figure out why it's only printing a part of it
def get_chunks():
    for doc in docs:
        for chunk in doc.noun_chunks:
            if len(chunk) > 3:
                nouns.append(chunk.text)



def create_json():
    final_obj["description"] = "noun chunks from kickstarter blurbs"
    final_obj["data"] = nouns

    with open("./kickstarter/kickstarter_noun_chunks.json", 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))

get_chunks()
create_json()
