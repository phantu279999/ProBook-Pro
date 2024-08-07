from django.shortcuts import render

from . import models

from src.process_data.business import News, NewsDetail, NewsContent, Category, CategoryNews
from src.common import common


def home_news(request):
	data = News().get_news_detail()
	categories = Category().get_data()
	context = {
		'data': data,
		'categories': categories,
	}
	return render(request, 'news/news.html', context=context)


def detail_news(request, url):
	news_pk = common.get_pk_in_url_news(url)
	if news_pk == 'None':
		news_pk = models.News.objects.get(url=url).pk
	data = NewsDetail().get_data({'id': news_pk})
	body = NewsContent().get_data(news_pk)

	context = {
		'data': data,
		'body': body
	}
	return render(request, 'news/detail_news.html', context=context)


def news_category(request, pk):
	page = common.get_current_page(request)
	start, end = common.get_range_sorted_of_page(page)
	data = CategoryNews().get_data(cate_id=pk, start=start, end=end)
	current_cate = Category().get_specifically_data(cate_id=pk)
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

