import os
import sys
import validators
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.config import config


class BaseSEO:

	def __init__(self):
		self.seo_tips = config.seo_tips

	def process_html(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		res = {}
		res['title'] = self.check_title(soup)
		res['meta_description'] = self.check_meta_desc(soup)
		print(self.process_external_link(soup))
		return res

	def check_title(self, soup):
		result = {}
		result['tip'] = self.seo_tips['title']
		text = soup.find('title')
		if not text:
			result['msg'] = "Your website is not title."
			result['status'] = False
		else:
			text = text.text
			if 10 < len(text) < 70:
				result['msg'] = "Your title is {} characters. It is optimal".format(len(text))
				result['status'] = True
			else:
				result['msg'] = "Title of your website is greater than 70 characters"
				result['status'] = False
			return result

	def check_meta_desc(self, soup):
		result = {}
		result['tip'] = self.seo_tips['title']
		text = soup.find('meta', attrs={'name': "description"})
		if not text:
			result['msg'] = "Your website is not tag 'Meta description'. Please check"
			result['status'] = False
		else:
			if 10 < len(text.attrs['content']) < 250:
				result['msg'] = "Your meta description is {} characters. It is optimal".format(len(text))
				result['status'] = True
			else:
				result['msg'] = "Title of your website is greater than 250 characters"
				result['status'] = False
		return result

	def process_url(self, soup, domain):
		result = {}
		result['tip'] = self.seo_tips['title']
		if '_' in domain:
			status = False
			msg = 'Trang web của bạn có chứa dấu gạch dưới \"_\"'
			print(msg)
		elif ' ' in domain:
			result['msg'] = "Your url is container \'space\'"
			result['status'] = False
		elif validators.url(domain) is False:
			result['msg'] = "Your url is not friendly"
			result['status'] = False
		else:
			result['msg'] = "Your url is friendly"
			result['status'] = True

		return result

	def process_canonical(self, soup):
		result = {}
		result['tip'] = self.seo_tips['title']
		check = soup.head.find("link", attrs={"rel": "canonical"})
		if not check:
			result['msg'] = "Tag Canonical is not found"
			result['status'] = False
		else:
			get_url = check.get("href", "")
			if not get_url:
				result['msg'] = "Tag Canonical is not attribute \'href\'"
				result['status'] = False
			elif 'http' not in get_url:
				result['msg'] = "Tag Canonical href is not contain link please add link start \'http\'"
				result['status'] = False
			else:
				result['msg'] = 'A canonical tag is set for this page and the link is working fine'
				result['status'] = True
		return result

	def process_meta_keywords(self, soup):
		result = {}
		result['tip'] = self.seo_tips['title']

		check = soup.head.find("meta", attrs={"name": "keywords"})
		if not check:
			result['msg'] = "Your website is not found Tag \'Meta:keywords\'"
			result['status'] = False
		else:
			content = check.get("content", "")
			if not content:
				result['msg'] = "Tag \'Meta:keywords\' is not attribute 'content'"
				result['status'] = False
			else:
				result['msg'] = "Tag \'Meta:keywords\' is passed"
				result['status'] = True
		return result

	def process_revisit_after(self, soup):
		result = {}
		result['tip'] = self.seo_tips['title']
		check = soup.head.find('meta', attrs={"name": 'revisit-after'})
		if check:
			content_revisit = check.get("content", "")
			if not content_revisit:
				result['msg'] = 'Your meta revisit-after has not attribute \'content\''
				result['status'] = False
			else:
				result['msg'] = 'Passed'
				result['status'] = True
		else:
			result['msg'] = "Not found tag meta revisit-after in your site"
			result['status'] = False
		return result

	def process_headings(self, soup):
		result = {}
		result['tip'] = self.seo_tips['title']
		list_h1 = soup.find_all("h1")
		list_h2 = soup.find_all("h2")
		list_h3 = soup.find_all("h3")
		list_h4 = soup.find_all("h4")
		list_h5 = soup.find_all("h5")
		list_h6 = soup.find_all("h6")

		if len(list_h1) == 0:
			result['msg'] = "Your website is not found tag h1"
			result['status'] = False
		elif len(list_h1) > 1:
			result['msg'] = "Your web site have greater than 1 tag h1. Optimal a page should contain only 1 tag h1"
			result['status'] = False
		else:
			result['msg'] = 'Your website had optimal tag h1'
			result['status'] = True

		return result

	def process_images(self, soup):
		result = {}
		result['tip'] = self.seo_tips['title']
		list_msg = []
		list_images = soup.body.find_all("img", src=True)
		for img in list_images:
			if not img.get("alt", ""):
				msg = f"Image({img['src']}) is have not attribute \'alt\'"
				list_msg.append(msg)

		if list_msg:
			result['msg'] = list_msg
			result['status'] = False
		else:
			result['msg'] = 'All images have ALT attribute.'
			result['status'] = True

		return result

	def process_frames(self, soup):
		result = {}
		result['tip'] = self.seo_tips['title']

		check = soup.find_all("iframe")
		if check:
			result[
				'msg'] = f"Your website have {len(check)} tag iframe. Usually this is not a problem for SEO if they are used properly."
			result['status'] = False
		else:
			result["msg"] = "Your site has no tags iframe."
			result["status"] = True

		return result

	def process_schema(self, soup):
		result = {}
		result['tip'] = self.seo_tips['schema']

		json_schema = soup.find('script', attrs={'type': 'application/ld+json'})
		if not json_schema:
			result['msg'] = "Your site has not tag script schema. Please check again"
			result['status'] = False
		else:
			result['msg'] = "Your site has script schema"
			result['status'] = True

		return result

	def process_open_graph(self, soup):
		result = {}
		result['tip'] = self.seo_tips['schema']

		open_graph = [
			[a["property"].replace("og:", ""), a.get("content", "")] for a in soup.select("meta[property^=og]")
		]
		if not open_graph:
			result['msg'] = "Your site has not tag Open Graph"
			result['status'] = False
		else:
			result['msg'] = "Your site has tag Open Graph"
			result['status'] = True

		return result

	def process_amp(self, soup):
		result = {}
		result['tip'] = self.seo_tips['AMP']

		check_doctype = ('<!doctype html>' in str(soup)) or ('<!DOCTYPE html>' in str(soup))

		check_head = (soup.find('head')) is not None
		check_body = (soup.find('body')) is not None

		check_charset = (soup.find('meta', attrs={'charset': True})) is not None

		check_amp = (soup.find('style', attrs={'amp-boilerplate': True})) is not None
		check_amp_2 = (soup.find('link', attrs={'rel': 'amphtml'})) is not None

		check_canonical = (soup.find('link', attrs={'rel': 'canonical'})) is not None
		check_viewport = (soup.find('meta', attrs={'name': 'viewport'})) is not None
		if all([
			check_doctype, check_head, check_body, check_charset, (check_amp or check_amp_2), check_canonical,
			check_viewport]
		):
			result['msg'] = "Your site is friendly with AMP"
			result['status'] = True
		else:
			result['msg'] = "Your site isn\'t friendly with AMP"
			result['status'] = False

		return result

	def process_meta_viewport(self, soup):
		result = {}
		result['tip'] = self.seo_tips['AMP']

		check = soup.find('meta', attrs={'name': 'viewport'})
		if not check:
			result['msg'] = "Your site has not tag meta viewport"
			result['status'] = False
		else:
			content = check.get("content", "")
			if content:
				result['msg'] = "Your tag viewport has not attribute content"
				result['status'] = False
			else:
				result['msg'] = "Your tag viewport is legal"
				result['status'] = True
		return result

	def process_robots_txt(self, soup, domain):
		result = {}
		result['tip'] = self.seo_tips['AMP']

		if urlparse(domain).path == "/" and requests.head(domain + '/robots.txt').status_code != 200:
			result['msg'] = 'Your site has not file robots.txt'
			result['status'] = False
		else:
			result['msg'] = "Your site has file robots.txt"
			result['status'] = True

		return result

	def process_xml_sitemaps(self, soup, domain):
		result = {}
		result['tip'] = self.seo_tips['AMP']

		url = domain.strip("/") + "/sitemap.xml"
		if urlparse(domain).path == "/" and requests.head(url).status_code != 200:
			result['msg'] = "Your site has not file sitemap.xml"
			result['status'] = False
		else:
			result['msg'] = "Your site has file sitemap.xml"
			result['status'] = True

		return result

	def process_lang(self, soup):
		result = {}
		result['tip'] = self.seo_tips['AMP']

		check = soup.find('html').get("lang", "")
		if not check:
			result['msg'] = "Your tag html has not attribute \'lang\'"
			result['status'] = False
		else:
			result['msg'] = "Your tag html has attribute \'lang\'"
			result['status'] = True

		return result

	def process_doctype(self, soup):
		result = {}
		result['tip'] = self.seo_tips['doctype']

		check_doctype = ('<!doctype html>' in str(soup)) or ('<!DOCTYPE html>' in str(soup))
		if not check_doctype:
			result['msg'] = "Not found tag <!DOCTYPE html> in your site"
			result['status'] = False
		else:
			result['msg'] = "Passed"
			result['status'] = True

		return result

	def process_favicon(self, soup):
		result = {}
		result['tip'] = self.seo_tips['favicon']

		for link in soup.head.find_all('link'):
			if 'icon' in link['rel']:
				result['msg'] = 'Your site has tag favicon'
				result['status'] = False
				break
		else:
			result['msg'] = 'Your site has not tag favicon'
			result['status'] = False

		return result

	def process_external_link(self, soup):
		links = soup.body.find_all("a", href=True)
		for link in links:
			print(link)