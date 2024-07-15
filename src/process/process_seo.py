import os
import sys

import requests
import traceback
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import base_seo


class ProcessSEO(base_seo.BaseSEO):
	def __init__(self):
		base_seo.BaseSEO.__init__(self)

	def process_link(self, link):
		self.process_single_link(link)

	def process_single_link(self, link):
		try:
			reponse = requests.get(link)
			if reponse.status_code == 200:
				return self.process_html(reponse.text)
		except:
			# print(traceback.format_exc())
			pass
		return {}


if __name__ == '__main__':
	process = ProcessSEO()
	process.process_link("https://kenh14.vn/")
