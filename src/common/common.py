import os
import sys
import re
import json
import pandas as pd
import unicodedata
import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
link_file = path + r'/media/store_data/video_youtube.csv'

from src.config.config import config_redis
from src.db_connect.base_redis import BaseRedis


def normalize_vietnamese(text):
	return unicodedata.normalize('NFC', text)


def write_data_video_to_file_csv(list_video):
	try:
		df = pd.DataFrame(list_video)
		df.to_csv(link_file, index=False, encoding='utf-8')
	except Exception as ex:
		print("Error write csv", ex)
		return "Error"


def is_valid_datetime_format(datetime_str):
	regex = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
	return re.match(regex, datetime_str) is not None


def convert_datetime_to_float(data):
	if isinstance(data, datetime.datetime):
		return data.timestamp()
	elif isinstance(data, str) and is_valid_datetime_format(data):
		t = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
		return t.timestamp()
	else:
		return 0


def build_url_news(title):
	mapping_chars = {
		"àáảãạâầấẩẫậăằắẳẵặ": "a",
		"èéẻẽẹêềếểễệ": "e",
		"đ": "d",
		"ìíỉĩị": "i",
		"òóỏõọôồốổỗộơờớởỡợ": "o",
		"ùúủũụưừứửữự": "u",
		"ỳýỷỹỵ": "y"
	}
	title = title.strip().lower()

	for viet_chars, ascii_char in mapping_chars.items():
		title = re.sub(r"[{}]+".format(viet_chars), ascii_char, title)
	title = re.sub(r"[^\w\d]+", "-", title)

	return title


def get_pk_in_url_news(url):
	return url.split("-")[-1]


def get_current_page(request):
	page = 1
	if 'page' in request.GET and request.GET['page']:
		try:
			page = int(request.GET['page'])
		except:
			pass
	page = page if page >= 1 else 1
	return page


def get_range_sorted_of_page(page):
	if not isinstance(page, int):
		return -10, -1
	start = -(page * 10)
	end = start + 9
	return start, end


def check_password(password, password_2):
	if password != password_2:
		return False

	# Basic password strength checks (add more as needed)
	if len(password) < 8:
		return False
	if not any(char.isdigit() for char in password):
		print("Digit")
		return False
	if not any(char.isupper() for char in password):
		print("isupper")
		return False
	if not any(char.islower() for char in password):
		print("islower")
		return False
	return True


def save_data_to_redis(key, channel_ytb, datas):
	return BaseRedis(config_redis).set_hash(key, channel_ytb, json.dumps(datas))


if __name__ == '__main__':
	...
