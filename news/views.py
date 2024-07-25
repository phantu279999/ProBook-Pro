from django.shortcuts import render
from django.core.cache import cache
from . import models


def home_news(request):
	if not cache.get('data'):
		# Fetch data from database or other source
		data = models.News.objects.all()
		cache.set('data', data, timeout=60 * 15)  # Cache for 15 minutes
	else:
		data = cache.get('data')
	return render(request, 'news.html', {'data': data})
