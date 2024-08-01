import os
import sys
import json
import time
import traceback

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.db_connect.base_redis import RedisQueue
from src.config.config import config_redis_queue
from src.process_data import business


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
		res = []
		if isinstance(item, bytes):
			item = json.loads(item.decode("UTF-8"))

		if item['action'] == 'update_news':
			res += self.update_news(item)
		elif item['action'] == 'update_newscontent':
			res += self.update_newscontent(item)
		elif item['action'] == 'update_category':
			res += self.update_category(item)
		elif item['action'] == 'update_categorynews':
			res += self.update_categorynews(item)
		elif item['action'] == 'update_tag':
			res += self.update_tag(item)
		elif item['action'] == 'update_tagnews':
			res += self.update_tagnews(item)
		elif item['action'] == 'update_topic':
			res += self.update_topic(item)
		elif item['action'] == 'update_topicnews':
			res += self.update_topicnews(item)

		return res

	def update_news(self, data):
		res = []
		obj = data['data']
		res += business.NewsDetail().init_by({"id": obj['pk']})
		_data = business.NewsDetail().get_data({"id": obj['pk']})
		res += business.News().push_data_to_redis(_data)
		return res

	def update_newscontent(self, data):
		res = []
		obj = data['data']
		res += business.NewsDetail().init_by({'newsid_id': obj['newsid']})
		return res

	def update_category(self, data):
		res = []
		res += business.Category().init_all()
		return res

	def update_categorynews(self, data):
		res = []
		obj = data['data']
		res += business.CategoryNews().init_by({"categoryid_id": obj['cate_id']})
		return res

	def update_tag(self, data):
		res = []

		return res

	def update_tagnews(self, data):
		res = []

		return res

	def update_topic(self, data):
		res = []

		return res

	def update_topicnews(self, data):
		res = []

		return res

	def push_action_to_queue(self, data):
		if isinstance(data, dict):
			data = json.dumps(data, ensure_ascii=False)
		self.db.enqueue(data)

	def app_run(self):
		while True:
			try:
				item = self.db.dequeue()
				if not item:
					time.sleep(10)
					continue
				print(item)
				res = self.process_action(item)
				print(res)
			except:
				print(traceback.format_exc())


if __name__ == '__main__':
	BaseAction().app_run()
