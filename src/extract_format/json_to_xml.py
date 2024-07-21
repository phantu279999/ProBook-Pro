import json
from xml.etree import ElementTree as ET


def json_to_xml(json_file_path, root_tag="data"):
	with open(json_file_path, 'r') as json_file:
		data = json.load(json_file)

	root = ET.Element(root_tag)
	json_to_xml_recursive(data, root)

	return ET.tostring(root, encoding='utf-8')


def json_to_xml_recursive(data, parent_element):
	if isinstance(data, dict):
		for key, value in data.items():
			child = ET.SubElement(parent_element, key)
			json_to_xml_recursive(value, child)
	elif isinstance(data, list):
		for item in data:
			child = ET.SubElement(parent_element, "item")
			json_to_xml_recursive(item, child)
	else:
		parent_element.text = str(data)


# Example usage
json_file = "your_json_file.json"
xml_data = json_to_xml(json_file)

# Print or save the XML data
print(xml_data)

# You can also save it to a file
with open("output.xml", "wb") as f:
	f.write(xml_data)
