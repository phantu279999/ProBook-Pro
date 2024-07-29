from django.shortcuts import render

from src.process import process_news
from src.common.common import get_pk_in_url_news


def home_news(request):
	data = process_news.get_lastest_news()
	return render(request, 'news/news.html', {'data': data})


def detail_news(request, url):
	news_pk = get_pk_in_url_news(url)
	data = process_news.get_detail_news(news_pk)
	body = process_news.get_newscontent(news_pk)

	context = {
		'data': data,
		'body': body
	}
	return render(request, 'news/detail_news.html', context=context)

