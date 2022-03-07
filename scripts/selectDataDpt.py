import os.path
import json
import random
import os

main_file = os.path.join(os.path.dirname(__file__), "..", "used_data.json")
dump_file = os.path.join(os.path.dirname(__file__), "full_dump.json")
batch_id = "2"

with open(main_file) as f:
	j_main = json.load(f)

with open(dump_file) as f:
	j_dump = json.load(f)


elements = list(j_dump.items())
random.shuffle(elements)

# Target Departments first
usedDpt = []
for key, value in elements:
	if value["birth_place"] not in usedDpt and key not in j_main:
		value["batch"] = batch_id
		value["treated"] = True
		j_main[key] = value
		usedDpt.append(value["birth_place"])

print(f"New data: {len(usedDpt)}")
batch_dir = os.path.join(os.path.dirname(__file__), "..", "data", f"batch-{batch_id}")
os.makedirs(batch_dir, exist_ok=True)


with open(main_file, "w") as f:
	j_main = json.dump(j_main, f)