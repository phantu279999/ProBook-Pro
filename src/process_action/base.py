import datetime
import json
import re
import dateutil.parser

from src.db_connect.base_mysql import BaseMySQL
from src.db_connect.base_redis import BaseRedis
from src.common.common import convert_datetime_to_float

class Base:
	def __init__(self, config):
		self.config = None
		self.db_redis = BaseRedis(config.config_redis)
		self.db_mysql = BaseMySQL(config.config_mysql)

	@staticmethod
	def process_item_redis(data, config):
		if config[1]:
			fields = []
			for it in config[1]:
				fields.append(data[it])
			return config[0].format(*fields)
		if isinstance(data, dict):
			return json.dumps(data)
		return str(data)

	@staticmethod
	def process_key_redis(data, config):
		if isinstance(data, list):
			data = data[0]
		if config[1]:
			fields = []
			for it in config[1]:
				fields.append(data[it])
			return config[0].format(*fields)
		else:
			return config[0]

	@staticmethod
	def process_field_redis(data, config):
		if config[1]:
			fields = []
			for it in config[1]:
				fields.append(data[it])
			return config[0].format(*fields)
		else:
			return config[0]

	@staticmethod
	def process_score_redis(data, config):
		score = 0
		if config in data:
			score = data[config]
			if re.search('^[\d]{4}-[\d]{2}-[\d]{2}T[\d]{2}:[\d]{2}:[\d]{2}$', score):
				score = convert_datetime_to_float(dateutil.parser.parse(score))
		else:
			print("Not found field in score")
		return score

	def process_string_redis(self, data, config):
		res = []
		if not data:
			return res
		if isinstance(data, dict):
			data = [data]
		conf_key = config['key']
		conf_item = config['item']

		if config['obj'] == 'all':
			key_redis = self.process_key_redis(data, conf_key)
			item = self.process_item_redis(data, conf_item)
			resit = self.db_redis.set_string(key_redis, item)
			res += [{'key': key_redis, 'status': True if resit else False}]
		else:
			for _data in data:
				key_redis = self.process_key_redis(_data, conf_key)
				item = self.process_item_redis(_data, conf_item)
				resit = self.db_redis.set_string(key_redis, item)
				res += [{'key': key_redis, 'status': True if resit else False}]
		return res

	def process_hash_redis(self, data, config):
		res = []
		conf_key = config['key']
		conf_item = config['item']
		conf_field = config['field']
		if isinstance(data, dict):
			data = [data]

		if config['obj'] == 'all':
			key_redis = self.process_key_redis(data, conf_key)
			item = self.process_item_redis(data, conf_item)
			field = self.process_field_redis(data, conf_field)
			resit = self.db_redis.set_hash(key_redis, field, item)
			res += [{'key': key_redis, 'status': True if resit else False}]
		else:
			for _data in data:
				key_redis = self.process_key_redis(_data, conf_key)
				item = self.process_item_redis(_data, conf_item)
				field = self.process_field_redis(_data, conf_field)
				resit = self.db_redis.set_hash(key_redis, field, item)
				res += [{'key': key_redis, 'status': True if resit else False}]
		return res

	def process_sorted_redis(self, data, config):
		res = []
		conf_key = config['key']
		conf_item = config['item']
		conf_score = config['score']
		if isinstance(data, dict):
			data = [data]
		for _data in data:
			key_redis = self.process_key_redis(_data, conf_key)
			item = self.process_item_redis(_data, conf_item)
			score = self.process_score_redis(_data, conf_score)

			resit = self.db_redis.add_sorted_set(key_redis, {item: score})
			res += [{'key': key_redis, 'status': True if resit else False}]
		return res

	def process_list_redis(self, data, config):
		res = []
		conf_key = config['key']
		conf_item = config['item']

		return res

	def _process_redis(self, data):
		key_redis = self.config['key_redis']
		for it in key_redis:
			if it['type'] == 'string':
				return self.process_string_redis(data, it)
			elif it['type'] == 'hash':
				return self.process_hash_redis(data, it)
			elif it['type'] == 'sorted':
				return self.process_sorted_redis(data, it)
			elif it['type'] == 'list':
				return self.process_list_redis(data, it)

	def push_data_to_redis(self, data):
		return self._process_redis(data)

	def build_data(self, data):
		conf_query = self.config['query']
		if conf_query[1]:
			d = []
			for field in conf_query[1]:
				if field in data:
					d.append(data[field])
			query = conf_query[0].format(*d)
		else:
			query = conf_query[0]
		_data = self.db_mysql.query(query)
		return _data

	def init_by(self, data):
		_data = self.build_data(data)
		return self.push_data_to_redis(_data)

	def init_all(self):
		_data = self.build_data({})
		return self.push_data_to_redis(_data)

