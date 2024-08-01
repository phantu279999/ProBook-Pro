import json

from src.process_action.base import Base


class News(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['News']

	def get_data(self, data):
		key = 'news'
		_data = self.db_redis.range_sorted_set(key)
		return _data


class NewsDetail(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['NewsDetail']

	def get_data(self, data):
		key = 'news:pk{}'.format(data['id'])
		_data = self.db_redis.get_string(key)
		return json.loads(_data.decode("UTF-8"))


class NewsContent(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['NewsContent']


