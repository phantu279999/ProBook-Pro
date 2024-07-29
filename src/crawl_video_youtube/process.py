import os
import sys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.base_selenium.setup_driver import custome_chrome_headless
from src.crawl_video_youtube.config import config_xpath


class GetVideoYoutube:

	def __init__(self):
		self._driver = custome_chrome_headless()
		self.domain_youtube = "https://www.youtube.com"
		self.number_scroll = {
			1: 90,
			2: 120,
			3: 150,
			4: 180,
			5: 210,
		}

	def app_run(self, domain):
		if not domain.endswith('videos'):
			domain = domain.strip("/") + '/videos'
		self.get_channel(domain)
		self.scroll_to_end_page()
		list_video = self.get_video()
		return list_video

	def get_channel(self, domain):
		self._driver.get(domain)

	def scroll_to_end_page(self):
		base_source = ""
		source_code = self._driver.page_source
		c = 0  # this is number of video want to get # self.number_scroll
		while len(base_source) != len(source_code):
			base_source = source_code
			self._driver.find_element("tag name", "body").send_keys(Keys.END)
			time.sleep(1)
			source_code = self._driver.page_source
			c += 1
			if c > 1:
				break

	def get_video(self):
		videos = []
		body_video = self._driver.find_element("xpath", config_xpath['body_video']['value'])
		html = body_video.get_attribute("innerHTML")
		soup = BeautifulSoup(html, "html.parser")
		list_video = soup.find_all("div", attrs={'id': config_xpath['object_video']['value']})
		for video in list_video:
			object_video = video.find("a", attrs={"id": "video-title-link"})
			thumb = video.find('a', attrs={'id': "thumbnail"}).findNext('yt-image').findNext('img')
			title = object_video["title"]
			url_ytb = self.domain_youtube + object_video["href"]
			meta_data = video.find_all('span', attrs={'class': config_xpath['view_date']['value']})
			views, date = meta_data[0], meta_data[1]
			# print(title)
			# print(url_ytb)
			# print(views.getText())
			# print(date.getText())
			# print(thumb.get("src", ""))
			# print("===========================================")
			videos.append({
				"TitleVideo": title,
				"Link": url_ytb,
				"View": views.getText(),
				"Date": date.getText(),
				"Thumb": thumb.get("src", ""),
			})

		return videos

	def get_info_video(self, url_video):
		self._driver.get(url_video)
		title = self._driver.find_element(
			"xpath", "//div[@id='title']//yt-formatted-string[@class='style-scope ytd-watch-metadata']").text
		view = self._driver.find_element("xpath", "//span[@class='style-scope yt-formatted-string bold'][1]").text
		date_create = self._driver.find_element("xpath", "//span[@class='style-scope yt-formatted-string bold'][3]").text

		print(title)
		print(view)
		print(date_create)
		print("*" * 100)


if __name__ == '__main__':
	app_run = GetVideoYoutube()
	list_video = app_run.app_run("https://www.youtube.com/@SofMM/videos")
	# print(list_video)
	# from src.common.common import write_data_video_to_file_csv
	# write_data_video_to_file_csv(list_video)
