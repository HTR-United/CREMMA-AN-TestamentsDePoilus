# ToDo when we have a htr-united.yml file
import os
import json
from collections import defaultdict
import lxml.etree as ET
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

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
    print(currFunction)

# Those ints are used to order people contribution (Role then Alphabetically)
orders = {
    "support" : 4,
    "aligner" : 2,
    "transcriber" : 1,
    "quality-control" : 3,
    "project-manager": 0
}

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
        people.append({"name": name, "surname": " ".join(surname).split("(")[0].strip(), "roles": val})

    print(people[-1])


with open(os.path.join("..", "htr-united.yml")) as f:
    catalog = yaml.load(f, Loader=Loader)

for person in catalog["authors"]:
    broke, aidx = False, None

    match = [
        (idx, auto_person) for (idx, auto_person) in enumerate(people)
        if auto_person["surname"] == person["surname"] and auto_person.get("name") == person.get("name")
    ]
    if match:
        idx, auto_person = match[0]
        person["roles"] = sorted(list(set(person["roles"] + auto_person["roles"])))
        people.pop(idx)
     
catalog["authors"].extend(people)

managers = [u for u in catalog["authors"] if "project-manager" in u["roles"]]
not_project_managers = [u for u in catalog["authors"] if "project-manager" not in u["roles"]]

catalog["authors"] = managers + sorted(
    not_project_managers, 
    key=lambda x: str(min([orders[role] for role in x["roles"]])) + str(int("name" not in x)) + x["surname"]+ " "+x.get("name", "")
)

with open(os.path.join("..", "htr-united.yml"), "w") as f:
    yaml.dump(catalog, f, sort_keys=False, allow_unicode=True)
