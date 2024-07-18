import os
import sys

from django.shortcuts import render

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.process.process_seo import ProcessSEO
from src.crawl_video_youtube.process import GetVideoYoutube
from src.common.common import write_data_video_to_file_csv


def index(request):
	context = {}
	if request.method == 'POST':
		your_domain = request.POST['your_domain']
		res = ProcessSEO().process_single_link(your_domain)
		context['res'] = res
	return render(request, 'index.html', context=context)


def crawl_video_youtube(request):
	context = {}
	if request.method == 'POST':
		domain_channel = request.POST['domain_channel']
		list_video = GetVideoYoutube().app_run(domain_channel)
		res = write_data_video_to_file_csv(list_video)
		if res == 'Error':
			print("Error when try write to file csv")
		context['list_video'] = list_video
		context['length'] = len(list_video)
	return render(request, 'video_youtube.html', context=context)
