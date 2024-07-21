import os
import sys

from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponseRedirect

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.process.process_seo import ProcessSEO
from src.crawl_video_youtube.process import GetVideoYoutube
from src.common.common import write_data_video_to_file_csv


def index(request):
	context = {}
	if request.method == 'POST' and 'your_domain' in request.POST:
		your_domain = request.POST['your_domain']
		res = ProcessSEO().process_single_link(your_domain)
		context['res'] = res
	elif request.method == 'POST' and 'channel_youtube' in request.POST:
		channel_ytb = request.POST['channel_youtube']
		redirect_url = reverse('video_youtube')
		redirect_url += '?channel_ytb={}'.format(channel_ytb)
		return HttpResponseRedirect(redirect_url)

	return render(request, 'index.html', context=context)


def crawl_video_youtube(request):
	context = {}
	channel_ytb = ""
	if request.method == 'POST':
		channel_ytb = request.POST['domain_channel']
	elif 'channel_ytb' in request.GET and request.GET['channel_ytb']:
		channel_ytb = request.GET['channel_ytb']

	if channel_ytb:
		list_video, status = get_list_video_ytb(channel_ytb)
		context['list_video'] = list_video
		context['status'] = status
		context['length'] = len(list_video)

	return render(request, 'video_youtube.html', context=context)


def extract_format(request):
	context = {}
	if request.method == 'POST':
		content_format = request.POST['content_format']
	return render(request, 'extract_format.html', context=context)


def get_list_video_ytb(link_channel):
	list_video = GetVideoYoutube().app_run(link_channel)
	res = write_data_video_to_file_csv(list_video)
	status = True
	if res == 'Error':
		print("Error when try write to file csv")
		status = False
	return list_video, status
