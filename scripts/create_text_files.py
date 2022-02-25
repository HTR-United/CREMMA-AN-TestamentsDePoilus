import os.path
import json
import os
import requests
import re
import lxml.etree as ET


main_file = os.path.join(os.path.dirname(__file__), "..", "used_data.json")
tei_dir = os.path.join(os.path.dirname(__file__), "..", "TEI", "tei")
xsl_path = os.path.join(os.path.dirname(__file__), "plain_text.xsl")


def spaces(context, a):
	return re.sub(r"\s+", " ", a[0])

ns = ET.FunctionNamespace("foo.bar/")
ns['spaces'] = spaces

xsl = ET.XSLT(ET.parse(xsl_path))

def get_batch_dir(batch_id):
	return os.path.join(os.path.dirname(__file__), "..", "data", f"batch-{batch_id}")

def get_txt_name(batch_dir, xml_id,):
	return os.path.join(batch_dir, f"{xml_id}.txt")

def convert_xml(xml_file_name, dest):
	xml = os.path.join(tei_dir, xml_file_name)
	text = str(xsl(ET.parse(xml)))
	text = "\n".join([line.strip() for line in text.split("\n") if line.strip()])
	with open(dest, "w") as f:
		f.write(text)

with open(main_file) as f:
	j_main = json.load(f)

FORCE = True
for key, value in j_main.items():
	batch_dir = get_batch_dir(value["batch"])
	text_file = get_txt_name(batch_dir, key)
	if os.path.exists(text_file) and not FORCE:
		print(f"[ X ] {text_file} exists already, passing")
	else:
		print(f"[...] Downloading {text_file}")
		convert_xml(value["file"], text_file)

