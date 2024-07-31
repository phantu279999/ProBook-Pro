import os
import sys
import json
import time

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.db_connect.base_redis import RedisQueue
from src.config.config import config_redis_queue


class BaseAction:

	def __init__(self):
		self.db = RedisQueue('queue_action', config_db=config_redis_queue)
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

	def process_action(self, item):
		if isinstance(item, bytes):
			item = json.loads(item.decode("UTF-8"))

		if item['action'] == 'update_news':
			...
		elif item['action'] == 'update_newscontent':
			...
		elif item['action'] == 'update_category':
			...
		elif item['action'] == 'update_categorynews':
			...
		elif item['action'] == 'update_tag':
			...
		elif item['action'] == 'update_tagnews':
			...
		elif item['action'] == 'update_topic':
			...
		elif item['action'] == 'update_topicnews':
			...

	def update_news(self):
		...

	def update_newscontent(self):
		...

	def update_category(self):
		...

	def update_categorynews(self):
		...

	def update_tag(self):
		...

	def update_tagnews(self):
		...

	def update_topic(self):
		...

	def update_topicnews(self):
		...

	def push_action_to_queue(self, data):
		if isinstance(data, dict):
			data = json.dumps(data, ensure_ascii=False)
		self.db.enqueue(data)

	def app_run(self):
		while True:
			item = self.db.dequeue()
			if not item:
				time.sleep(10)
				continue
			print(item)
			self.process_action(item)


if __name__ == '__main__':
	# import sqlite3
	# conn = sqlite3.connect('G:\Py\ProBook\db.sqlite3')
	# cur = conn.cursor()
	# cur.execute('''SELECT * FROM news_news''')
	# for it in cur:
	# 	print(it)
	...