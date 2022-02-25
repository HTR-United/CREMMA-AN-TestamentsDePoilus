import os.path
import json
import os
import requests


main_file = os.path.join(os.path.dirname(__file__), "..", "used_data.json")

def get_batch_dir(batch_id):
	return os.path.join(os.path.dirname(__file__), "..", "data", f"batch-{batch_id}")

def get_image_name(batch_dir, xml_id, image_numb):
	return os.path.join(batch_dir, f"{xml_id}-{image_numb}.jpg")

def download(url, dest):
	response = requests.get(url)
	file = open(dest, "wb")
	file.write(response.content)
	file.close()

with open(main_file) as f:
	j_main = json.load(f)

for key, value in j_main.items():
	batch_dir = get_batch_dir(value["batch"])
	for image_numb, image in enumerate(value["images"]):
		img_name = get_image_name(batch_dir, key, image_numb)
		if os.path.exists(img_name):
			print(f"[ X ] {img_name} exists already, passing")
		else:
			print(f"[...] Downloading {img_name}")
			download(image, img_name)
