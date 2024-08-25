import os
import sys
import json
import traceback
from xml.etree import ElementTree as ET


class ExtractFile:

	def __init__(self):
		...

	def json_to_xml(self, json_file_path, root_tag="data"):
		with open(json_file_path, 'r') as json_file:
			data = json.load(json_file)

		root = ET.Element(root_tag)
		self.json_to_xml_recursive(data, root)

		return ET.tostring(root, encoding='utf-8')

	def json_to_xml_recursive(self, data, parent_element):
		if isinstance(data, dict):
			for key, value in data.items():
				child = ET.SubElement(parent_element, key)
				self.json_to_xml_recursive(value, child)
		elif isinstance(data, list):
			for item in data:
				child = ET.SubElement(parent_element, "item")
				self.json_to_xml_recursive(item, child)
		else:
			parent_element.text = str(data)

	def xml_to_json(self, xml_file_path):
		with open(xml_file_path, 'r') as xml_file:
			tree = ET.parse(xml_file)
			root = tree.getroot()

		return json.dumps(self.json_from_xml_recursive(root))

	def json_from_xml_recursive(self, element):
		if (len(element) == 0) and (not element.text):
			return None
		elif len(element) == 0:
			return element.text

		children = {}
		for child in element:
			tag = child.tag.lower()
			if children.get(tag) is None:
				children[tag] = self.json_from_xml_recursive(child)
			else:
				if not isinstance(children[tag], list):
					children[tag] = [children[tag]]
				children[tag].append(self.json_from_xml_recursive(child))

		if element.text:
			if children:
				children["text"] = element.text
			else:
				children = element.text

		return children

	# def extract_xml_to_json(self, text_xml):
	# 	try:
	# 		path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
	# 		xml_file = path + "/media/store_data/output.xml"
	# 		with open("media/store_data/input.json", "w") as f:
	# 			f.write(text_xml)
	#
	# 		json_data = self.xml_to_json(xml_file)
	#
	# 		# Print or save the JSON data
	# 		print(json_data)
	#
	# 		# You can also save it to a file
	# 		with open("media/store_data/output.json", "w") as f:
	# 			f.write(json_data)
	# 		return True
	# 	except:
	# 		print(traceback.format_exc())
	# 		return False
	#
	# def extract_json_to_xml(self, text_json):
	# 	try:
	# 		# Example usage
	# 		with open("media/store_data/input.json", "w") as f:
	# 			f.write(text_json)
	# 		json_file = "media/store_data/input.json"
	# 		xml_data = self.json_to_xml(json_file)
	#
	# 		# You can also save it to a file
	# 		with open("media/store_data/output.xml", "wb") as f:
	# 			f.write(xml_data)
	# 		return True
	# 	except:
	# 		print(traceback.format_exc())
	# 		return False

	def process_file(self, data, type_input, type_output):
		if type_input == 'json':
			file_path = "media/store_data/input.json"
			with open(file_path, "w") as f:
				f.write(data)
			self.process_output(file_path, type_input, type_output, data)
			return True
		elif type_input == 'xml':
			file_path = "media/store_data/input.xml"
			with open(file_path, "w") as f:
				f.write(data)
			self.process_output(file_path, type_input, type_output, data)
			return True
		return False

	def process_output(self, file_path, type_input, type_output, data):
		if type_output == 'json':
			if type_input == 'xml':
				data = self.xml_to_json(file_path)
		elif type_output == 'xml':
			if type_input == 'json':
				data = self.json_to_xml(file_path)
		self.save_data(data, type_output)

	def save_data(self, data, type):
		if isinstance(data, str):
			data = data.encode("UTF-8")
		with open("media/store_data/output.{}".format(type), "wb") as f:
			f.write(data)
