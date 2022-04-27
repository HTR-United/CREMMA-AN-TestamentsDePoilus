# ToDo when we have a htr-united.yml file
import os
import json
from collections import defaultdict
import lxml.etree as ET
import yaml


with open("../used_data.json") as f:
    used_data = json.load(f)

DoneBatches = ["2"]
used_data = {file: used_data[file] for file in used_data if used_data[file]["batch"] in DoneBatches}

# Dict[PersonID, Set of roles]
details = defaultdict(set)

# Get for each "done" file the list of people who interved
for file, infos in used_data.items():
    with open(os.path.join("..", "TEI", "tei", infos["file"])) as f:
        xml = ET.parse(f)
        for resp in xml.findall("//{*}respStmt"):
            resp_type = resp.findall("./{*}resp")[0].text
            for pers in resp.findall(".//{*}persName"):
                details[pers.attrib.get("ref", pers.text)].add(resp_type)

# Normalize the details list
details_list = {key: sorted(list(val)) for key, val in details.items()}

persTEI = ET.parse(os.path.join("..", "TEI", "tei", "personnes.xml"))

# ID -> TEXT
persons = {
    person.attrib["ref"]: person.text.strip()
    for person in persTEI.findall("//{*}persName[@ref]")
}


def functionMap(currFunction):
    if currFunction == "Identification et description du testament":
        return "support"
    if currFunction == "Transcription":
        return "transcriber"
    if currFunction == "Validation":
        return "quality-control"
    if currFunction == "Corrections hors plate-forme et contrôle de qualité final":
        return "transcriber"


details = {
    persons.get(persName, persName): list(map(functionMap, functions))
    for persName, functions in details.items()
}

print(details)

people = []
for key, val in details.items():
    if key.startswith("#"):
        people.append({"surname": key.replace("#", ""), "roles": val})
    else:
        name, *surname = key.split()
        people.append({"name": name, "surname": " ".join(surname), "roles": val})

    print(people[-1])


with open(os.path.join("..", "htr-united.yml")) as f:
    catalog = yaml.load(f)

for person in catalog["authors"]:
    broke, aidx = False, None
    for aidx, auto_person in enumerate(people):
        broke = False
        if auto_person["surname"] == person["surname"] and auto_person.get("name") == person.get("surname"):
            person["roles"] = sorted(list(set(person["roles"] + auto_person["roles"])))
            broke = True
            break
    if broke:
        people.pop(aidx)

catalog["authors"].extend(people)

catalog["authors"] = sorted(catalog["authors"], key=lambda x: x["surname"]+" "+x.get("name", ""))

with open(os.path.join("..", "htr-united.yml"), "w") as f:
    yaml.dump(catalog, f, sort_keys=False, allow_unicode=True)
