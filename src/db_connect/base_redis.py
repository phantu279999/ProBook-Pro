import redis


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


if __name__ == '__main__':
	config = {
		"host": "127.0.0.1",
		"port": 6379,
		"db": 2,
		"username": "",
		"password": ""
	}
	rd = BaseRedis(config)

	print(rd.get_length_list("address"))
