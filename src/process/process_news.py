import json
from django.core import serializers
from news.models import News, NewsContent
from src.db_connect.base_redis import BaseRedis
from src.config.config import config_redis


def get_lastest_news():
	db = BaseRedis(config_redis)
	if db.is_exits('news'):
		return json.loads(db.get_string('news').decode("UTF-8"))
	else:
		data = News.objects.all().order_by("-date_create")
		return set_lastest_news(serializers.serialize("json", data))


def set_lastest_news(data):
	db = BaseRedis(config_redis)
	db.set_ex_string("news", data, seconds=60 * 15)  # set time 15 minutes
	_data = json.loads(data)
	for item in _data:
		key_detail = "news:pk{}".format(item['pk'])
		db.set_string(key_detail, json.dumps(item['fields']))
	return _data


def set_detail_news(pk):
	db = BaseRedis(config_redis)
	key_detail = "news:pk{}".format(pk)
	try:
		_data = News.objects.get(pk=pk)
	except:
		return {}
	_data = serializers.serialize("json", [_data])
	_data = json.loads(_data)[0]
	db.set_string(key_detail, json.dumps(_data['fields']))

	set_newscontent(pk)
	return _data


def get_detail_news(pk):
	db = BaseRedis(config_redis)
	key_detail = "news:pk{}".format(pk)
	if db.is_exits(key_detail):
		data = json.loads(db.get_string(key_detail).decode("UTF-8"))
		return data
	else:
		return set_detail_news(pk)


def set_newscontent(pk):
	db = BaseRedis(config_redis)
	key = "newscontent"
	key_detail = "news:pk{}".format(pk)
	try:
		_data = NewsContent.objects.get(newsid__pk=pk)
	except NewsContent.DoesNotExist:
		_data = None
	body = ""
	if _data:
		body = _data.body
	db.set_hash(key, key_detail, body)
	return body


def get_newscontent(pk):
	db = BaseRedis(config_redis)
	key = "newscontent"
	field = 'news:pk{}'.format(pk)
	if db.is_exits_hash(key, field):
		_data = db.get_hash(key, field)
		return _data.decode("UTF-8")
	else:
		return set_newscontent(pk)


if __name__ == '__main__':
	print(set_detail_news(1))
