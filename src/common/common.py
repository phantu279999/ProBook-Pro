import os
import sys
import csv
import pandas as pd
import unicodedata

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
