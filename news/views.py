from django.shortcuts import render
from django.http import Http404

from . import models

from src.process import process_news
from src.process_data.business import News
from src.common.common import get_pk_in_url_news, get_range_sorted_of_page


def home_news(request):
	# data = process_news.get_lastest_news()
	data = News().get_news_detail()
	categories = process_news.get_categories()
	context = {
		'data': data,
		'categories': categories,
	}
	return render(request, 'news/news.html', context=context)


def detail_news(request, url):
	news_pk = get_pk_in_url_news(url)
	if news_pk == 'None':
		news_pk = models.News.objects.get(url=url).pk
	data = process_news.get_detail_news(news_pk)
	body = process_news.get_newscontent(news_pk)

	context = {
		'data': data,
		'body': body
	}
	return render(request, 'news/detail_news.html', context=context)


def news_category(request, pk):
	page = 1
	if 'page' in request.GET and request.GET['page']:
		try:
			page = int(request.GET['page'])
		except:
			raise Http404("Object does not exist")
	page = page if page >= 1 else 1
	start, end = get_range_sorted_of_page(page)
	data = process_news.get_news_in_category(pk, start, end)
	try:
		current_cate = models.Category.objects.get(pk=pk).name
	except:
		current_cate = "Not found Category"
	context = {
		'data': data,
		'category_name': current_cate,
		'prev_page': page - 1,
		'current_page': page,
		'next_page': page + 1,
		'pk': pk,
	}
	return render(request, 'news/list_news_category.html', context=context)

