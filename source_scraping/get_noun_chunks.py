import spacy
import sys
import json

nlp = spacy.load('en')

input_file = sys.argv[1]
output_file = sys.argv[2]
desc_string = sys.argv[3]

data = json.loads(open(input_file).read())

blurbs = data["data"]

docs = [ nlp(d) for d in blurbs ]

nouns = []
final_obj = {}

# TODO: figure out why it's only printing a part of it
def get_chunks():
    for doc in docs:
        for chunk in doc.noun_chunks:
            if len(chunk) > 3:
                print chunk
                nouns.append(chunk.text)

def create_json():
    final_obj["description"] = desc_string
    final_obj["data"] = nouns

    with open(output_file, 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))

get_chunks()
create_json()
