import xml.etree.ElementTree as ET
import json


def xml_to_json(xml_file_path):
	with open(xml_file_path, 'r') as xml_file:
		tree = ET.parse(xml_file)
		root = tree.getroot()

	return json.dumps(json_from_xml_recursive(root))


def json_from_xml_recursive(element):
	if (len(element) == 0 and not element.text):
		return None
	elif len(element) == 0:
		return element.text

	children = {}
	for child in element:
		tag = child.tag.lower()
		if children.get(tag) is None:
			children[tag] = json_from_xml_recursive(child)
		else:
			if not isinstance(children[tag], list):
				children[tag] = [children[tag]]
			children[tag].append(json_from_xml_recursive(child))

	if element.text:
		if children:
			children["text"] = element.text
		else:
			children = element.text

	return children


# Example usage
xml_file = "your_xml_file.xml"
json_data = xml_to_json(xml_file)

# Print or save the JSON data
print(json_data)

# You can also save it to a file
with open("output.json", "w") as f:
	f.write(json_data)
