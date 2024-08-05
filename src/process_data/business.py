from src.process_data import config, news, category


class News(news.News):
	def __init__(self):
		news.News.__init__(self, config)


class NewsDetail(news.NewsDetail):
	def __init__(self):
		news.NewsDetail.__init__(self, config)


class NewsContent(news.NewsContent):
	def __init__(self):
		news.NewsContent.__init__(self, config)


class Category(category.Category):
	def __init__(self):
		category.Category.__init__(self, config)


class CategoryNews(category.CategoryNews):
	def __init__(self):
		category.CategoryNews.__init__(self, config)


if __name__ == '__main__':
	# print(NewsDetail().init_by({'id': 3}))
	# print(News().get_news_detail())
	print(Category().get_data())
	# print(NewsDetail().get_data({'id': 1}))
	# print(NewsContent(config).init_by({'newsid_id': 2}))