from src.db_connect.base_redis import BaseRedis
from src.config.config import config_redis_queue


class BaseAction:

	def __init__(self):
		self.db = BaseRedis(config_redis_queue)
		self.list_action = [
			'update_news',
			'update_newscontent',
			'update_category',
			'update_categorynews',
			'update_tag',
			'update_tagnews',
			'update_topic',
			'update_topicnews',
		]

	def reformat_news(self, data):
		...

	def push_action_to_queue(self, data):
		...

	def app_run(self):
		while True:
			...

