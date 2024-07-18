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

	def process_html(self, html, link):
		soup = BeautifulSoup(html, 'html.parser')
		res = {}
		res['title'] = self.check_title(soup)
		res['meta_description'] = self.check_meta_desc(soup)
		res['url'] = self.process_url(link)
		res['canonical'] = self.process_canonical(soup)
		res['meta_keywords'] = self.process_meta_keywords(soup)
		res['revisit_after'] = self.process_revisit_after(soup)
		res['headings'] = self.process_headings(soup)
		res['images'] = self.process_images(soup)
		res['frames'] = self.process_frames(soup)
		res['schema'] = self.process_schema(soup)
		res['op'] = self.process_open_graph(soup)
		res['amp'] = self.process_amp(soup)
		res['viewport'] = self.process_meta_viewport(soup)
		res['robots_txt'] = self.process_robots_txt(link)
		res['sitemaps'] = self.process_xml_sitemaps(link)
		res['language'] = self.process_language(soup)
		res['doctype'] = self.process_doctype(soup)
		res['favicon'] = self.process_favicon(soup)
		res['external_link'] = self.process_external_link(soup)

		return res

	def check_title(self, soup):
		result = {}
		result['name'] = 'Title'
		result['tip'] = self.seo_tips['title']
		check = soup.find('title')
		if not check:
			result['msg'] = "Your website is not title."
			result['status'] = False
			result['data'] = ""
		else:
			text = check.text
			if 10 < len(text) < 70:
				result['msg'] = "Your title is {} characters. It is optimal".format(len(text))
				result['status'] = True
			else:
				result['msg'] = "Title of your website is greater than 70 characters"
				result['status'] = False
			result['data'] = text
		return result

	def check_meta_desc(self, soup):
		result = {}
		result['name'] = 'Meta Description'
		result['tip'] = self.seo_tips['meta_description']
		text = soup.find('meta', attrs={'name': "description"})
		if not text:
			result['msg'] = "Your website is not tag 'Meta description'. Please check"
			result['status'] = False
			result['data'] = ""
		else:
			content = text.attrs.get('content', "")
			if 10 < len(content) < 250:
				result['msg'] = "Your meta description is {} characters. It is optimal".format(len(text))
				result['status'] = True
			elif 'content' not in text.attrs:
				result['msg'] = "Meta description is not attribute content"
				result['status'] = False
			else:
				result['msg'] = "Meta description content is greater than 250 characters"
				result['status'] = False
			result['data'] = content
		return result

	def process_url(self, domain):
		result = {}
		result['name'] = 'URL'
		result['tip'] = self.seo_tips['url']
		if '_' in domain:
			result['msg'] = "Your site url has contain \'_\'"
			result['status'] = False
		elif ' ' in domain:
			result['msg'] = "Your url is contain \'space\'"
			result['status'] = False
		elif validators.url(domain) is False:
			result['msg'] = "Your url is not friendly"
			result['status'] = False
		else:
			result['msg'] = "Your url is friendly"
			result['status'] = True
		result['data'] = domain
		return result

	def process_canonical(self, soup):
		result = {}
		result['name'] = 'Canonical'
		result['tip'] = self.seo_tips['canonical']

		check = soup.head.find("link", attrs={"rel": "canonical"})
		if not check:
			result['msg'] = "Tag Canonical is not found"
			result['status'] = False
			result['data'] = ""
		else:
			get_url = check.get("href", "")
			result['data'] = get_url
			if not get_url:
				result['msg'] = "Tag Canonical is not attribute \'href\'"
				result['status'] = False
			elif 'http' not in get_url:
				result['msg'] = "Tag Canonical href is not contain link please add link start \'http\'(Full link)"
				result['status'] = False
			else:
				result['msg'] = 'A canonical tag is set for this page and the link is working fine'
				result['status'] = True
		return result

	def process_meta_keywords(self, soup):
		result = {}
		result['name'] = 'Meta Keywords'
		result['tip'] = self.seo_tips['meta_keywords']

		check = soup.head.find("meta", attrs={"name": "keywords"})
		if not check:
			result['msg'] = "Your website is not found Tag \'meta:keywords\'"
			result['status'] = False
			result['data'] = ""
		else:
			content = check.get("content", "")
			result['data'] = content
			if not content:
				result['msg'] = "Tag \'meta:keywords\' is not attribute 'content'"
				result['status'] = False
			else:
				result['msg'] = "Tag \'meta:keywords\' is passed"
				result['status'] = True
		return result

	def process_revisit_after(self, soup):
		result = {}
		result['name'] = 'Meta:Revisit After'
		result['tip'] = self.seo_tips['revisit_after']
		check = soup.head.find('meta', attrs={"name": 'revisit-after'})
		if check:
			content_revisit = check.get("content", "")
			result['data'] = content_revisit
			if not content_revisit:
				result['msg'] = 'Your meta revisit-after has not attribute \'content\''
				result['status'] = False
			else:
				result['msg'] = 'Passed'
				result['status'] = True
		else:
			result['msg'] = "Not found tag meta revisit-after in your site"
			result['status'] = False
			result['data'] = ""
		return result

	def process_headings(self, soup):
		result = {}
		result['name'] = 'Headings'
		result['type_data'] = 'dict'
		result['tip'] = self.seo_tips['headings']
		list_h1 = [it.text for it in soup.find_all("h1")]
		list_h2 = [it.text for it in soup.find_all("h2")]
		list_h3 = [it.text for it in soup.find_all("h3")]
		list_h4 = [it.text for it in soup.find_all("h4")]
		list_h5 = [it.text for it in soup.find_all("h5")]
		list_h6 = [it.text for it in soup.find_all("h6")]

		if len(list_h1) == 0:
			result['msg'] = "Your website is not found tag h1"
			result['status'] = False
		elif len(list_h1) > 1:
			result['msg'] = "Your web site have greater than 1 tag h1. Optimal a page should contain only 1 tag h1"
			result['status'] = False
		elif len(list_h2) == 0:
			result['msg'] = "Your website is not found tag h2"
			result['status'] = False
		else:
			result['msg'] = 'Your website had optimal tag h1'
			result['status'] = True
		result['data'] = {
			'h1': list_h1, 'h2': list_h2, 'h3': list_h3, 'h4': list_h4, 'h5': list_h5, 'h6': list_h6,
		}
		return result

	def process_images(self, soup):
		result = {}
		result['name'] = 'Images'
		result['type_msg'] = 'list'
		result['type_data'] = 'list'
		result['data'] = []
		result['tip'] = self.seo_tips['images']
		list_msg = []
		list_images = soup.body.find_all("img", src=True)
		for img in list_images:
			if not img.get("alt", ""):
				list_msg.append(f"Image({img['src']}) is have not attribute \'alt\'")
			result['data'].append(img['src'])

		if list_msg:
			result['msg'] = list_msg
			result['status'] = False
		else:
			result['msg'] = ['All images have \'alt\' attribute.']
			result['status'] = True

		return result

	def process_frames(self, soup):
		result = {}
		result['name'] = 'Iframe'
		result['data'] = ''
		result['tip'] = self.seo_tips['frames']

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
		result['name'] = 'Script:schema'
		result['data'] = ''
		result['tip'] = self.seo_tips['schema']

		json_schema = soup.find('script', attrs={'type': 'application/ld+json'})
		if not json_schema:
			result['msg'] = "Your site has not tag script schema."
			result['status'] = False
		else:
			result['msg'] = "Your site has script schema."
			result['status'] = True

		return result

	def process_open_graph(self, soup):
		result = {}
		result['name'] = 'Open Graph'
		result['type_data'] = 'list'
		result['tip'] = self.seo_tips['open_graph']

		open_graph = [
			[a["property"].replace("og:", ""), a.get("content", "")] for a in soup.select("meta[property^=og]")
		]
		if not open_graph:
			result['msg'] = "Your site has not tag Open Graph"
			result['status'] = False
		else:
			result['msg'] = "Your site has tag Open Graph"
			result['status'] = True
		result['data'] = open_graph
		return result

	def process_amp(self, soup):
		result = {}
		result['name'] = 'AMP'
		result['data'] = ''
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
		result['name'] = 'Meta Viewport'
		result['tip'] = self.seo_tips['viewport']

		check = soup.find('meta', attrs={'name': 'viewport'})
		if not check:
			result['msg'] = "Your site has not tag meta viewport"
			result['status'] = False
			result['data'] = ''
		else:
			content = check.get("content", "")
			if not content:
				result['msg'] = "Your tag viewport has not attribute content"
				result['status'] = False
			else:
				result['msg'] = "Your tag viewport is legal"
				result['status'] = True
			result['data'] = content
		return result

	def process_robots_txt(self, domain):
		result = {}
		result['name'] = 'Robots TXT'
		result['data'] = ''
		result['tip'] = self.seo_tips['robots_txt']

		if urlparse(domain).path == "/" and requests.head(domain + '/robots.txt').status_code != 200:
			result['msg'] = 'Your site has not file robots.txt'
			result['status'] = False
		else:
			result['msg'] = "Your site has file robots.txt"
			result['status'] = True

		return result

	def process_xml_sitemaps(self, domain):
		result = {}
		result['name'] = 'XML Sitemap'
		result['data'] = ""
		result['tip'] = self.seo_tips['xml_sitemaps']

		url = domain.strip("/") + "/sitemap.xml"
		if urlparse(domain).path == "/" and requests.head(url).status_code != 200:
			result['msg'] = "Your site has not file sitemap.xml"
			result['status'] = False
		else:
			result['msg'] = "Your site has file sitemap.xml"
			result['status'] = True

		return result

	def process_language(self, soup):
		result = {}
		result['name'] = 'Language'
		result['tip'] = self.seo_tips['language']

		check = soup.find('html').get("lang", "")
		if not check:
			result['msg'] = "Your tag html has not attribute \'lang\'"
			result['status'] = False
		else:
			result['msg'] = "Your tag html has attribute \'lang\'"
			result['status'] = True
		result['data'] = check
		return result

	def process_doctype(self, soup):
		result = {}
		result['name'] = 'Doctype'
		result['data'] = ""
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
		result['name'] = 'Icon favicon'
		result['tip'] = self.seo_tips['favicon']

		for link in soup.head.find_all('link'):
			if 'icon' in link['rel']:
				result['msg'] = 'Your site has tag favicon'
				result['status'] = True
				result['data'] = link.get('href', '')
				break
		else:
			result['msg'] = 'Your site has not tag favicon'
			result['status'] = False
			result['data'] = ""
		return result

	def process_external_link(self, soup):
		result = {}
		result['name'] = 'External Link'
		result['msg'] = 'Passed'
		result['type_data'] = 'list'
		result['status'] = True
		links = soup.body.find_all("a", href=True)

		list_external = []
		for link in links:
			if link['href'].startswith('http'):
				if link.get('rel', '') != 'nofollow':
					result['msg'] = 'Link external should has attribute rel=nofollow'
					result['status'] = False
				list_external.append(link['href'])
		result['data'] = list_external
		return result
