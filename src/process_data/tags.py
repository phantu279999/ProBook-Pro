import json

from src.process_data.base import Base
from src.process_data.news import NewsDetail


class Tag(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['Tag']

	def get_data_by_key(self, key):
		_data = self.db_redis.get_string(key)
		if not _data:
			return {}
		return json.loads(_data.decode("UTF-8"))

	def get_data_by_url(self, url, idx=1):
		key = self.config['key_redis'][idx]['key'][0].format(url.lower())
		_data = self.db_redis.get_string(key)
		if not _data:
			return {}
		return json.loads(_data.decode("UTF-8"))


class TagNews(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['TagNews']

	def get_data_by_newsid(self, newsid, idx=0):
		key = self.config['key_redis'][idx]['key'][0].format(newsid)
		res = []
		_data = self.db_redis.range_sorted_set(key)
		for item in _data:
			item = item.decode("UTF-8")
			data = Tag(self.config_it).get_data_by_key(item)
			if data: res.append(data)
		return res

	def get_data(self, tag_id, idx=0):
		key = self.config['key_redis'][idx]['key'][0].format(tag_id)
		res = []
		_data = self.db_redis.range_sorted_set(key)
		for item in _data:
			news_id = item.decode("UTF-8").replace("news:pk", "")
			data = NewsDetail(self.config_it).get_data({'id': news_id})
			if data: res.append(data)
		return res
