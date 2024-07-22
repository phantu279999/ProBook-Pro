import json

import redis

from src.config.config import config_redis
from src.common.common import convert_datetime_to_float

class BaseRedis:

	def __init__(self, config_db):
		self._db = redis.Redis(
			host=config_db.get("host", ""),
			port=config_db.get("port", ""),
			db=config_db.get("db", ""),
			username=config_db.get("username", ""),
			password=config_db.get("password", ""),
		)

	# =============== EVENT STRING ========================
	def get_string(self, key):
		return self._db.get(key)

	def get_del_string(self, key):
		value = self.get_string(key)
		self.delete(key)
		return value

	def get_set_string(self, key, value):
		return self._db.getset(key, value)

	def get_ex_string(self, key):
		return self._db.getex(key)

	def get_range_string(self, key, start=0, end=-1):
		return self._db.getrange(key, start, end)

	def set_string(self, key, value):
		return self._db.set(key, value)

	def set_ex_string(self, key, value, seconds=60):
		self._db.setex(key, seconds, value)

	def set_multi(self, keys):
		if not isinstance(keys, dict):
			return "Please enter parameter is dict"
		return self._db.mset(mapping=keys)

	def append_string(self, key, value):
		return self._db.append(key, value)

	def decr_number_string(self, key, amount=1):
		return self._db.decrby(key, amount)

	def get_length_string(self, key):
		return self._db.strlen(key)

	def delete(self, key):
		return self._db.delete(key)

	def is_exits(self, key):
		return self._db.exists(key)

	def get_time_expire(self, key):
		return self._db.ttl(key)

	# =============== EVENT LIST ========================
	def get_length_list(self, key):
		return self._db.llen(key)

	def get_index_list(self, key, idx):
		try:
			idx = int(idx)
		except:
			return "Please enter param is integer"
		return self._db.lindex(key, idx)

	def append_list(self, key, value):
		return self._db.rpush(key, value)

	def push_first_list(self, key, value):
		return self._db.lpush(key, value)

	def pop_last_list(self, key):
		return self._db.rpop(key)

	def pop_first_list(self, key):
		return self._db.lpop(key)

	def range_list(self, key, start=0, end=-1):
		return self._db.lrange(key, start, end)

	def remove_list(self, key, value, count=1):
		return self._db.lrem(name=key, count=count, value=value)

	# =============== EVENT SORTED SET ========================
	def add_sorted_set(self, key, value):
		if not isinstance(value, dict):
			return "Please enter param value is dict value:score"
		return self._db.zadd(key, value)

	def range_sorted_set(self, key, start=0, end=-1, with_scores=False):
		return self._db.zrange(name=key, start=start, end=end, withscores=with_scores)

	def range_by_score_sorted_set(self, key, from_score, to_score):
		return self._db.zrangebyscore(key, from_score, to_score)

	def remove_sorted_set(self, key, value):
		return self._db.zrem(key, value)

	def diff_two_sorted_sets(self, set1, set2, with_scores=False):
		return self._db.zdiff([set1, set2], withscores=with_scores)

	def length_sorted_set(self, key):
		return self._db.zcount(key, "-inf", "+inf")

	# =============== EVENT HASH ========================
	def set_hash(self, key, field, value):
		return self._db.hset(key, field, value)

	def get_all_hash(self, key):
		return self._db.hgetall(key)

	def get_values_hash(self, key):
		return self._db.hvals(key)

	def get_keys_hash(self, key):
		return self._db.hkeys(key)

	def is_exits_hash(self, key, fields):
		return self._db.hexists(key, fields)


if __name__ == '__main__':
	rd = BaseRedis(config_redis)

	for k, v in rd.get_all_hash("VideoChannelYoutube").items():
		for it in (json.loads(v.decode("UTF-8"))):
			print(it)