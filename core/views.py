import os
import sys

from django.shortcuts import render
from django.http import HttpResponseBadRequest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.seo.analyzer.base import BaseSEO
from src.crawl_video_youtube.common import get_list_video_ytb
from src.extract_format.process import ExtractFile
from src.common.morse_code import MorseCode
from src.common.common import save_data_to_redis

from .forms import MorseCodeForm


def index(request):
	if request.method == 'POST':
		your_domain = request.POST.get('your_domain', '').strip()
		if not your_domain:
			return HttpResponseBadRequest("Domain is required.")

		try:
			res = BaseSEO().process_link(your_domain)
		except Exception as e:
			return HttpResponseBadRequest(f"Error processing the domain: {e}")
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
		save_data_to_redis("VideoChannelYoutube", channel_ytb, list_video)

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
