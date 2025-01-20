import json
import os
import sys

from django.shortcuts import render

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.config.config import config_redis
from src.db_connect.base_redis import BaseRedis

from src.process.process_seo import ProcessSEO
from src.crawl_video_youtube.common import get_list_video_ytb
from src.extract_format.process import ExtractFile
from src.common.morse_code import MorseCode

from .forms import MorseCodeForm


def index(request):
	if request.method == 'POST':
		your_domain = request.POST['your_domain']
		res = ProcessSEO().process_single_link(your_domain)
		return render(request, 'index.html', context={'res': res})

	return render(request, 'index.html')


def crawl_video_youtube(request):
	context = {}
	if request.method == 'POST':
		channel_ytb = request.POST.get('domain_channel', '')
		number_of_videos = request.POST.get('number_of_video', 90)

		list_video, status = get_list_video_ytb(channel_ytb, int(number_of_videos))
		context = {
			'list_video': list_video,
			'status': status,
			'length': len(list_video)
		}
		BaseRedis(config_redis).set_hash("VideoChannelYoutube", channel_ytb, json.dumps(list_video))

	return render(request, 'video_youtube.html', context=context)


def extract_format(request):
	context = {
		'message_error': ''
	}
	if request.method == 'POST':
		input_format = request.POST.get('input_format', '')
		output_format = request.POST.get('output_format', '')
		file_extract = request.FILES.get('file_extract', None)
		data = request.POST.get('content_format', '')
		if file_extract:
			data = file_extract.read().decode("UTF-8")

		try:
			res = ExtractFile().process_file(data, input_format, output_format)
			if res:
				context['message_error'] = "Extract file success"
			else:
				context['message_error'] = "Extract file fail"
		except Exception as ex:
			context['message_error'] = f"Error during format conversion: {str(ex)}"

	return render(request, 'extract_format.html', context=context)


def morse_code_translator_view(request):
	if request.method == 'POST':
		form = MorseCodeForm(request.POST)
		if form.is_valid():
			output = MorseCode().to_english(request.POST['morse_code'])
			form = MorseCodeForm(initial={'text': output})
	else:
		form = MorseCodeForm(initial={'text': ""})
	return render(request, 'morse_code_translator.html', {'form': form})
