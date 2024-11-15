from src.crawl_video_youtube.process import GetVideoYoutube
from src.common.common import write_data_video_to_file_csv


def get_list_video_ytb(link_channel, number_of_video):
	try:
		list_video = GetVideoYoutube().app_run(link_channel, number_of_video=number_of_video)
		res = write_data_video_to_file_csv(list_video)
		status = res != 'Error'
		if not status:
			print("Error when trying to write to file csv")
		return list_video, status
	except Exception as e:
		print(f"Error fetching or processing videos: {str(e)}")
		return [], False
