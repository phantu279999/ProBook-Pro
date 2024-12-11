import json
import os
import sys
import traceback

from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponseRedirect

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
	number_of_videos = request.POST['number_of_video'] if 'number_of_video' in request.POST else 90

	if channel_ytb:
		list_video, status = get_list_video_ytb(channel_ytb, int(number_of_videos))
		context = {
			'list_video': list_video,
			'status': status,
			'length': len(list_video),
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
		except Exception as e:
			# print(traceback.format_exc())
			context['message_error'] = f"Error during format conversion: {str(e)}"

	return render(request, 'extract_format.html', context=context)


def morse_code_translator(request):
	if request.method == 'POST':
		form = MorseCodeForm(request.POST)
		if form.is_valid():
			output = MorseCode().to_english(request.POST['input'])
			form = MorseCodeForm(initial={'output': output})
	else:
		form = MorseCodeForm(initial={'output': ""})
	return render(request, 'morse_code_translator.html', {'form': form})
