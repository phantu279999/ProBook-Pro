import json

from src.process_data.base import Base


class Category(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['Category']

	def get_data(self):
		key = self.config['key_redis'][0]['key'][0]
		_data = self.db_redis.get_string(key)
		if not _data:
			return []
		return json.loads(_data.decode("UTF-8").replace("\'", "\""))


class CategoryNews(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['CategoryNews']


