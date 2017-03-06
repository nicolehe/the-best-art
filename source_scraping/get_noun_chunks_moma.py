import spacy
import sys
import json

nlp = spacy.load('en')


input_file = "moma_mediums.json"
output_file = "../data/noun_chunks/moma_noun_chunks.json"
desc_string = "moma mediums noun chunks"

data = json.loads(open(input_file).read())

blurbs = data["data"]

docs = [ nlp(d.replace("\r\n", "")) for d in blurbs if d is not None]

nouns = []
final_obj = {}

def get_chunks():
    for doc in docs:
        for chunk in doc.noun_chunks:
            if len(chunk) > 2:
                print chunk
                nouns.append(chunk.text)

def create_json():
    final_obj["description"] = desc_string
    final_obj["data"] = nouns

    with open(output_file, 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))

get_chunks()
create_json()
