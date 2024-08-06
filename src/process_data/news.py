import json

from src.process_data.base import Base


class News(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['News']

	def get_news_detail(self):
		_data = self.get_data()
		if not _data:
			return []
		res = []
		for it in _data[::-1]:
			newsid = it.decode("UTF-8").replace("news:pk", "")
			_news = NewsDetail(self.config_it).get_data({'id': newsid})
			res.append(_news)
		return res

	def get_data(self, idx=0):
		key = self.config['key_redis'][idx]['key'][0]
		_data = self.db_redis.range_sorted_set(key)
		return _data


class NewsDetail(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['NewsDetail']

	def get_data(self, data, idx=0):
		key = self.config['key_redis'][idx]['key'][0].format(data['id'])
		# key = 'news:pk{}'.format(data['id'])
		_data = self.db_redis.get_string(key)
		return json.loads(_data.decode("UTF-8"))


class NewsContent(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['NewsContent']

	def get_data(self, news_id, idx=0):
		key = self.config['key_redis'][idx]['key'][0]
		field = 'news:pk{}'.format(news_id)
		_data = self.db_redis.get_hash(key, field)
		if not _data:
			return None
		return _data.decode("UTF-8")
