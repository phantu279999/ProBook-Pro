import json
import os
import sys

from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponseRedirect

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.process.process_seo import ProcessSEO
from src.crawl_video_youtube.process import GetVideoYoutube
from src.common.common import write_data_video_to_file_csv
from src.extract_format import json_to_xml, xml_to_json
from src.db_connect.base_redis import BaseRedis
from src.config.config import config_redis


def index(request):
	if request.method == 'POST':
		if 'your_domain' in request.POST:
			your_domain = request.POST['your_domain']
			res = ProcessSEO().process_single_link(your_domain)
			return render(request, 'index.html', context={'res': res})

		elif 'channel_youtube' in request.POST:
			channel_ytb = request.POST['channel_youtube']
			redirect_url = f"{reverse('video_youtube')}?channel_ytb={channel_ytb}"
			return HttpResponseRedirect(redirect_url)

	return render(request, 'index.html')


def crawl_video_youtube(request):
	context = {}
	channel_ytb = request.POST.get('domain_channel') or request.GET.get('channel_ytb')
	if channel_ytb:
		list_video, status = get_list_video_ytb(channel_ytb)
		context = {
			'list_video': list_video,
			'status': status,
			'length': len(list_video),
		}
		BaseRedis(config_redis).set_hash("VideoChannelYoutube", channel_ytb, json.dumps(list_video))

	return render(request, 'video_youtube.html', context=context)


def extract_format(request):
	context = {}
	context['message_error'] = ""
	if request.method == 'POST':
		content_format = request.POST.get('content_format', '')
		input_format = request.POST.get('input_format', '')
		output_format = request.POST.get('output_format', '')

		if not content_format:
			context['message_error'] = "Bạn chưa nhập nội dung dữ liệu."
		elif not input_format or not output_format:
			context["message_error"] = "Vui lòng nhập dạng data Input và Output."
		else:
			try:
				if input_format == 'JSON' and output_format == 'XML':
					res = json_to_xml.extract_json_to_xml(content_format)
				elif input_format == 'XML' and output_format == 'JSON':
					res = xml_to_json.extract_xml_to_json(content_format)
				else:
					res = False

				if res is False:
					context['message_error'] = "Invalid format conversion requested."
				else:
					# Not complete
					context['message_error'] = "Extract format sucessfully."
			except Exception as e:
				context['message_error'] = f"Error during format conversion: {str(e)}"

	return render(request, 'extract_format.html', context=context)


def get_list_video_ytb(link_channel):
	try:
		list_video = GetVideoYoutube().app_run(link_channel)
		res = write_data_video_to_file_csv(list_video)
		status = res != 'Error'
		if not status:
			print("Error when trying to write to file csv")
		return list_video, status
	except Exception as e:
		print(f"Error fetching or processing videos: {str(e)}")
		return [], False
