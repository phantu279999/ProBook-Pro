import os
import sys
import re
import pandas as pd
import unicodedata
import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
link_file = path + r'/media/store_data/video_youtube.csv'


def normalize_vietnamese(text):
	return unicodedata.normalize('NFC', text)


def write_data_video_to_file_csv(list_video):
	try:
		df = pd.DataFrame(list_video)
		df.to_csv(link_file, index=False, encoding='utf-8')
	# with open(link_file,  "w", newline='', encoding='utf-8') as f:
	# 	writer = csv.writer(f)
	# 	writer.writerow(["Title", "Link", "View", "Date", "Thumb"])
	# 	for it in list_video:
	# 		writer.writerow([it['TitleVideo'], it['Link'], it['View'], it['Date'], it['Thumb']])
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
	title = title.lower()

	for viet_chars, ascii_char in mapping_chars.items():
		title = re.sub(r"[{}]+".format(viet_chars), ascii_char, title)
	title = re.sub(r"[^\w\d]+", "-", title)

	return title
