import os.path
import json
import os
import requests
import re
import lxml.etree as ET


main_file = os.path.join(os.path.dirname(__file__), "..", "used_data.json")
readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")

before_line = []
after_line = []

with open(readme_path, encoding="utf8") as f:
	start, after = False, False
	for line in f:
		if start == False:
			before_line.append(line.strip())
		elif after == True:
			after_line.append(line.strip())

		if "<!-- Start Table -->" in line:
			start = True
		elif "<!-- End Table -->" in line:
			after = True
			after_line.append(line.strip())

with open(main_file, encoding="utf8") as f:
	j = json.load(f)

table = [
	["Document", "Testataire", "Département de naissance", "Année de naissance", "Batch"],
	["--"]*5,
	*[
		[key, value["author"], value["birth_place"], str(value["birth_year"]), str(value["batch"])]
		for key, value in j.items()
	]
]


table = ["| " + " | ".join(row) + " |" for row in table]
#print()

with open(readme_path, "w", encoding="utf8") as f:
	f.write("\n".join([*before_line, *table, *after_line]))