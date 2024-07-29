import json

from django.shortcuts import render
from django.core import serializers
from . import models

from src.db_connect.base_redis import BaseRedis
from src.config.config import config_redis


def home_news(request):
	data = models.News.objects.all().order_by("-date_create")
	data = serializers.serialize("json", data)
	for it in json.loads(data):
		print("------------", it.keys())
		print("------------", it.values())
	BaseRedis(config_redis).set_ex_string("news", data, seconds=60 * 15)
	return render(request, 'news/news.html', {'data': json.loads(data)})


def detail_news(request, url):
	data = models.News.objects.get(url=url)
	return render(request, 'news/detail_news.html', {'data': data})