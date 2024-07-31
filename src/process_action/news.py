from src.db_connect.base_mysql import BaseMySQL
from src.db_connect.base_redis import BaseRedis

class News:
	def __init__(self, config):
		self.config = config.action['News']
		self.db_redis = BaseRedis(config.config_redis)
		self.db_mysql = BaseMySQL(config.config_mysql)

	def _process_redis(self, data):
		key_redis = self.config['key_redis']
		for it in key_redis:
			if it['type'] == 'string':
				...
			elif it['type'] == 'hash':
				...
			elif it['type'] == 'sorted':
				...

	def push_data_to_redis(self, data):
		...

	def build_data(self):
		query = self.config['query']
		if query[1]:
			...

	def init_all(self):
		...
