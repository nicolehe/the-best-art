import spacy
import sys
import json

nlp = spacy.load('en')

input_num = sys.argv[1]
# output_file = sys.argv[2]
# desc_string = sys.argv[3]
input_file = "./bkmuseum/bkmuseum_titles_old_descs" + input_num + ".json"
output_file = "../data/noun_chunks/bkmuseum_old_descs" + input_num + ".json"
desc_string = "bkmuseum desc noun chunks file " + input_num

data = json.loads(open(input_file).read())


artworks = data["data"]


blurbs = [artwork["description"].replace("\r\n", "") for artwork in artworks if "description" in artwork]


docs = [ nlp(d) for d in blurbs ]

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
