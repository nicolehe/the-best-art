import spacy
import sys
import json

nlp = spacy.load('en')

input_search = sys.argv[1]
# output_file = sys.argv[2]
# desc_string = sys.argv[3]
input_file = "./patents/data/" + input_search + "_patents.json"
output_file = "../data/noun_chunks/" + input_search + "_patents_noun_chunks.json"
desc_string = input_search + " patents noun chunks"

data = json.loads(open(input_file).read())

blurbs = data["data"]

docs = [ nlp(d) for d in blurbs ]

nouns = []
final_obj = {}

def get_chunks():
    for doc in docs:
        for chunk in doc.noun_chunks:
            if len(chunk) > 0:
                print chunk
                nouns.append(chunk.text)

def create_json():
    final_obj["description"] = desc_string
    final_obj["data"] = nouns

    with open(output_file, 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))

get_chunks()
create_json()
