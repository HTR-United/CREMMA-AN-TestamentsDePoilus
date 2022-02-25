import lxml.etree as et
import re


normalizeSpace = re.compile(r"\s+")

main = et.parse("../TEI/tei/TestamentsDePoilus.xml")
main.xinclude()

places = {
	
}

def get_images(element):
	for facsimile in element.findall(".//{*}facsimile"):
		base = facsimile.attrib["{http://www.w3.org/XML/1998/namespace}base"]
		for image in facsimile.xpath("./t:surface/t:graphic/@url", namespaces={"t": "http://www.tei-c.org/ns/1.0"}):
			yield base, image

for testament in main.findall("//{*}TEI"):
	doc_id = testament.attrib["{http://www.w3.org/XML/1998/namespace}id"]
	author = testament.findall(".//{*}author")
	if not author:
		# print(testament.attrib["{http://www.w3.org/XML/1998/namespace}id"])
		# Basically lieux & unites
		continue
	author = author[0]
	author_name = author.findall(".//{*}persName")
	if not author_name :
		# print(testament.attrib["{http://www.w3.org/XML/1998/namespace}id"])
		# Basically personnes
		continue
	author_id = author_name[0].attrib["ref"][1:]
	author_text = normalizeSpace.sub(" ", author_name[0].text.strip())
	#print(author_id, author_text)
	for person in main.xpath(
			f".//t:person[@xml:id='{author_id}']",
			namespaces={
			"t": "http://www.tei-c.org/ns/1.0", 
			"xml": "http://www.w3.org/XML/1998/namespace"
			}
		):
		birth_date = (person.xpath(".//t:birth/t:date/@when", namespaces={"t": "http://www.tei-c.org/ns/1.0"}) or ["0000-00-00"])[0]
		birth_place_id = (person.xpath(".//t:birth/t:placeName/@ref", namespaces={"t": "http://www.tei-c.org/ns/1.0"}) or [""])[0]
		birth_year = int(birth_date.split("-")[0])
		if birth_place_id:
			birth_place_dept = main.xpath(
				f".//t:place[@xml:id='{birth_place_id[1:]}']/t:location/t:region/text()",
				namespaces={
					"t": "http://www.tei-c.org/ns/1.0", 
					"xml": "http://www.w3.org/XML/1998/namespace"
				}
			)
			lieux = (birth_place_dept or  main.xpath(
				f".//t:place[@xml:id='{birth_place_id[1:]}']/t:placeName/t:settlement/text()",
				namespaces={
					"t": "http://www.tei-c.org/ns/1.0", 
					"xml": "http://www.w3.org/XML/1998/namespace"
				}
			))[0]


		places[doc_id] = {
			"ID": doc_id,
			"file": doc_id.replace("TestamentsDePoilus_", "")+".xml",
			"author": author_text,
			"birth_year": birth_year,
			"birth_place": lieux,
			"treated": False,
			"images": [
				f"{base}{url}/full/full/0/default.jpg"
				for (base, url) in get_images(testament)
			]
		}

import json
with open("full_dump.json", "w") as f:
	json.dump(places, f)

for place in places.values():
	print(place)