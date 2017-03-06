import json

f = open("../data/Artworks.json").read()
data = json.loads(f)



def create_json():
    final_obj = {}
    final_obj["description"] = "moma mediums"
    final_obj["data"] = l

    with open("moma_mediums.json", 'wt') as out:
        json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))


mediums = set()

for artwork in data:
    mediums.add(artwork["Medium"])

l = list(mediums)
create_json()
