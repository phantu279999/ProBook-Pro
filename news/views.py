from django.shortcuts import render

from . import models

from src.process import process_news
from src.common.common import get_pk_in_url_news


def home_news(request):
	data = process_news.get_lastest_news()
	categories = process_news.get_categories()
	context = {
		'data': data,
		'categories': categories,
	}
	return render(request, 'news/news.html', context=context)


def detail_news(request, url):
	news_pk = get_pk_in_url_news(url)
	data = process_news.get_detail_news(news_pk)
	body = process_news.get_newscontent(news_pk)

	context = {
		'data': data,
		'body': body
	}
	return render(request, 'news/detail_news.html', context=context)


def news_category(request, pk):
	data = models.CategoryNews.objects.filter(categoryid__pk=pk)
	context = {
		'data': [it.newsid for it in data],
		'category': data[0].categoryid,
	}
	print(data)
	return render(request, 'news/list_news_category.html', context=context)

