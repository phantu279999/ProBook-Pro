from django.shortcuts import render

from . import models

from src.process_data import business
from src.common import common


def home_news(request):
	data = business.News().get_news_detail()
	categories = business.Category().get_data()
	context = {
		'data': data,
		'categories': categories,
	}
	return render(request, 'news/news.html', context=context)


def detail_news(request, url):
	news_pk = common.get_pk_in_url_news(url)
	if news_pk == 'None':
		news_pk = models.News.objects.get(url=url).pk
	data = business.NewsDetail().get_data({'id': news_pk})
	body = business.NewsContent().get_data(news_pk)
	tags = business.TagNews().get_data_by_newsid(news_pk, 1)
	context = {
		'data': data,
		'body': body,
		'tags': tags
	}
	return render(request, 'news/detail_news.html', context=context)


def news_category(request, pk):
	page = common.get_current_page(request)
	start, end = common.get_range_sorted_of_page(page)
	data = business.CategoryNews().get_data(cate_id=pk, start=start, end=end)
	current_cate = business.Category().get_specifically_data(cate_id=pk)
	if not current_cate:
		current_cate = "Not found Category"
	else:
		current_cate = current_cate['name']
	context = {
		'data': data,
		'category_name': current_cate,
		'prev_page': page - 1,
		'current_page': page,
		'next_page': page + 1,
		'pk': pk,
	}
	return render(request, 'news/list_news_category.html', context=context)


def news_in_tags_view(request, url):
	_tag = business.Tag().get_data_by_url(url)
	_news = business.TagNews().get_data(_tag['id'])
	context = {
		"tag": _tag,
		'data': _news
	}
	return render(request, 'news/news_in_tags.html', context=context)


def news_in_topic_view(request, url):
	_topic = business.Topic().get_data_by_url(url)
	_news = business.TopicNews().get_data(_topic['id'])
	context = {
		"topic": _topic,
		'data': _news
	}
	return render(request, 'news/news_in_topic.html', context=context)
