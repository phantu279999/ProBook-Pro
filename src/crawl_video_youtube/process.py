import os
import sys
import time
from typing import List, Dict
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.base_selenium.setup_driver import custome_chrome_headless
from src.crawl_video_youtube.config import config_xpath


class GetVideoYoutube:
    """A class to scrape YouTube videos from a given channel."""

    YOUTUBE_DOMAIN = "https://www.youtube.com"

    def __init__(self):
        self._driver = custome_chrome_headless()

    def app_run(self, channel_url: str, number_of_videos: int = 90) -> List[Dict[str, str]]:
        """Main function to get video details from a YouTube channel."""
        if not channel_url.endswith("/videos"):
            channel_url = channel_url.rstrip("/") + "/videos"

        self._driver.get(channel_url)
        self._scroll_to_end_page(number_of_videos)
        videos = self._extract_videos(number_of_videos)
        self._driver.quit()
        return videos

    def _scroll_to_end_page(self, number_of_videos: int) -> None:
        """Scrolls the YouTube page to load more videos."""
        previous_length = 0
        attempts = 0
        max_attempts = (number_of_videos - 30) // 30 if number_of_videos > 90 else 1

        while attempts < max_attempts:
            self._driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(1.5)

            page_length = len(self._driver.page_source)
            if page_length == previous_length:
                break  # Stop scrolling if no new content is loaded

            previous_length = page_length
            attempts += 1

    def _extract_videos(self, number_of_videos: int) -> List[Dict[str, str]]:
        """Extracts video details from the YouTube channel page."""
        videos = []
        try:
            body_video = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.XPATH, config_xpath["body_video"]["value"]))
            )
            soup = BeautifulSoup(body_video.get_attribute("innerHTML"), "html.parser")
            video_elements = soup.find_all("div", attrs={"id": config_xpath["object_video"]["value"]})

            for video in video_elements:
                title_element = video.find("a", attrs={"id": "video-title-link"})
                thumbnail_element = video.find("a", attrs={"id": "thumbnail"}).findNext("yt-image").findNext("img")
                meta_data = video.find_all("span", attrs={"class": config_xpath["view_date"]["value"]})

                if not title_element or len(meta_data) < 2:
                    continue  # Skip if essential data is missing

                videos.append({
                    "TitleVideo": title_element.get("title", ""),
                    "Link": f"{self.YOUTUBE_DOMAIN}{title_element.get('href', '')}",
                    "View": meta_data[0].get_text(strip=True),
                    "Date": meta_data[1].get_text(strip=True),
                    "Thumb": thumbnail_element.get("src", ""),
                })

                if len(videos) >= number_of_videos:
                    break
        except Exception as e:
            print(f"Error extracting videos: {e}")

        return videos


if __name__ == "__main__":
    scraper = GetVideoYoutube()
    video_list = scraper.app_run("https://www.youtube.com/@SofMM/videos")
    print(video_list)
