import json

from src.process_data.base import Base
from src.process_data.news import NewsDetail


class Category(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['Category']

	def get_data(self, idx=0):
		key = self.config['key_redis'][idx]['key'][0]
		_data = self.db_redis.get_string(key)
		if not _data:
			return []
		return json.loads(_data.decode("UTF-8").replace("\'", "\""))

	def get_specifically_data(self, cate_id, idx=0):
		for it in self.get_data(idx):
			if it['id'] == cate_id:
				return it
		return None

class CategoryNews(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['CategoryNews']

	def get_data(self, cate_id, start=-10, end=-1, idx=0):
		key = self.config['key_redis'][idx]['key'][0].format(cate_id)

		_data = self.db_redis.range_sorted_set(key, start, end)
		list_news = []
		for it in _data:
			newsid = it.decode("UTF-8").replace("news:pk", "")
			_news = NewsDetail(self.config_it).get_data({'id': newsid})
			if not _news:
				continue
			list_news.append(_news)
		return list_news[::-1]
