import json

final_obj = {}
all_keywords = []

file1 = open("./itp_thesis_keywords_total.json").read()
data1 = json.loads(file1)

for keyword in data1["data"]:
    if keyword != "":
        all_keywords.append(keyword)


final_obj["description"] = "itp thesis keywords"
final_obj["data"] = all_keywords

with open("itp_thesis_keywords_total2.json", 'wt') as out:
    json.dump(final_obj, out, sort_keys=True, indent=4, separators=(',', ': '))
